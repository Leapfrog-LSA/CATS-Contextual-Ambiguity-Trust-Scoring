"""Refuse new or modified files larger than a size limit (default 2 MiB).

Why. Large files in git never leave its history: deleting them later needs a
history rewrite and a force-push. Most of this repository's size is RSS
snapshot text committed before the snapshots moved to ``cats-snapshots``
(see ``cats/calibration/fetch_snapshots.py``), and those texts belong to their
publishers (``DATA_LICENSE``). This check stops the next large blob at the
door instead of after the fact.

Scope. Only files that a commit **adds or modifies** are checked. Files
already in the repository that nobody touches are not flagged, so the
existing >2 MiB snapshots and ``data/labelled_sources.jsonl`` do not block
unrelated work. Changing one of them, however, does fail: that would add
another multi-megabyte copy to history. If such a change is really needed,
raise ``--max-bytes`` for that file's PR deliberately, in review.

Two ways to run it:

* **pre-commit** (``.pre-commit-config.yaml``) passes the staged file names::

      python scripts/check_large_files.py path/one path/two

  A file identical to its committed version in ``HEAD`` is skipped, so
  ``pre-commit run --all-files`` does not flag the existing large files.

* **CI** (``.github/workflows/ci.yml``) checks every blob that the commits in
  ``--base..--head`` introduce, using the sizes git records. That includes a
  large file added in one commit and deleted in a later one of the same PR:
  merge commits keep it in history all the same::

      python scripts/check_large_files.py --base origin/main --head HEAD

Symlinks are measured as git stores them (the link text), never followed.

Exit status: 0 if every checked file is within the limit, 1 if one is over it,
2 if git cannot compare the two refs.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from typing import List, Optional, Sequence, Tuple

DEFAULT_MAX_BYTES = 2 * 1024 * 1024  # 2 MiB, the same cap nginx puts on request bodies.


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def new_blobs(base: str, head: str) -> List[Tuple[str, int]]:
    """``(path, size)`` for every blob reachable from ``head`` but not from ``base``.

    Walks every commit in ``base..head``, not just the final tree, so a blob that
    an intermediate commit added and a later one removed is still reported.
    """
    objects = _git("rev-list", "--objects", f"{base}..{head}")
    batch = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objecttype) %(objectsize) %(rest)"],
        input=objects,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    blobs = []
    for line in batch.splitlines():
        parts = line.split(" ", 2)
        if len(parts) < 2 or parts[0] != "blob":
            continue
        blobs.append((parts[2] if len(parts) == 3 else "", int(parts[1])))
    return blobs


def unchanged_since_head(paths: Sequence[str]) -> List[str]:
    """The subset of ``paths`` that exist in ``HEAD`` with the same content as in the working tree.

    Outside a git repository, or before the first commit, nothing counts as unchanged.
    """
    if not paths:
        return []
    try:
        changed = set(_git("diff", "--name-only", "--no-renames", "-z", "HEAD", "--", *paths).split("\0"))
    except (OSError, subprocess.CalledProcessError):
        return []
    unchanged = []
    for path in paths:
        if path in changed:
            continue
        in_head = subprocess.run(["git", "cat-file", "-e", f"HEAD:{path}"], capture_output=True).returncode == 0
        if in_head:
            unchanged.append(path)
    return unchanged


def oversized(sizes: Sequence[Tuple[str, int]], max_bytes: int) -> List[Tuple[str, int]]:
    return [(path, size) for path, size in sizes if size > max_bytes]


def _format(size: int) -> str:
    return f"{size / (1024 * 1024):.2f} MiB ({size:,} bytes)"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="files to check in the working tree (pre-commit mode)")
    parser.add_argument("--base", help="git ref to compare against; checks the files added or modified since")
    parser.add_argument("--head", default="HEAD", help="git ref whose committed sizes are checked (with --base)")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="size limit in bytes")
    args = parser.parse_args(argv)

    if args.base:
        if args.files:
            parser.error("pass either file names or --base, not both")
        try:
            sizes = new_blobs(args.base, args.head)
        except subprocess.CalledProcessError as exc:
            sys.stderr.write(f"git failed comparing {args.base}..{args.head}: {exc.stderr.strip()}\n")
            return 2
    else:
        files = [path for path in args.files if os.path.isfile(path) and not os.path.islink(path)]
        big = [path for path in files if os.path.getsize(path) > args.max_bytes]
        skip = set(unchanged_since_head(big))
        sizes = [(path, os.path.getsize(path)) for path in big if path not in skip]

    too_big = oversized(sizes, args.max_bytes)
    for path, size in too_big:
        sys.stderr.write(f"{path}: {_format(size)} exceeds the limit of {_format(args.max_bytes)}\n")
    if too_big:
        sys.stderr.write(
            "Large files stay in git history for good. Keep data out of this repository "
            "(RSS snapshots belong in cats-snapshots); see scripts/check_large_files.py.\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
