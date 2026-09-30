"""Download RSS snapshots from the separate ``cats-snapshots`` data repository.

Snapshots used to be committed to this repository under ``data/snapshots/``:
one ~2–4 MB file per collection day, which made them most of the repository's
size and most of its history. New snapshots live in a dedicated data
repository (``Leapfrog-LSA/cats-snapshots``); the files already on ``main``
stay where they are, because the published calibration and research results
cite them by path.

This module fetches the data repository's snapshots into a local directory
(``data/snapshots/`` by default, so every existing consumer —
``merge_snapshots``, ``research/*.py`` — keeps working unchanged) and verifies
each file against the repository's ``SHA256SUMS`` manifest.

Manifest format
---------------
Plain ``sha256sum`` output, one file per line, paths relative to the data
repository's root::

    <64 hex chars>  snapshots/labelled_sources_2026-09-24.jsonl

Entries whose path does not match that shape are rejected, so a manifest can
never make this module write outside ``--dest``.

Never losing data
-----------------
* A local file whose hash already matches is left alone (no download).
* A downloaded file is written to a temporary name and only renamed into place
  after its hash matches the manifest; a mismatch deletes it and fails.
* A local file whose hash **differs** from the manifest is **never
  overwritten**: the remote version is saved next to it as
  ``<name>.remote`` (outside the ``*.jsonl`` glob, so it is not picked up by
  accident) and the run exits non-zero. Union the two with
  :mod:`cats.calibration.merge_snapshots`, exactly as for a same-day collision.

Usage::

    python -m cats.calibration.fetch_snapshots            # or: make snapshots-download
    python -m cats.calibration.fetch_snapshots --dest /tmp/snaps --ref <commit-sha>
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import httpx
import structlog

logger = structlog.get_logger()

DEFAULT_REPO = "Leapfrog-LSA/cats-snapshots"
DEFAULT_REF = "main"
DEFAULT_DEST = Path("data/snapshots")
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_BYTES = 50_000_000
MANIFEST = "SHA256SUMS"
RAW_BASE = "https://raw.githubusercontent.com"

_REPO_RE = re.compile(r"^[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
_REF_RE = re.compile(r"^[A-Za-z0-9._/-]+$")
_ENTRY_RE = re.compile(r"^([0-9a-f]{64}) [ *](snapshots/labelled_sources_\d{4}-\d{2}-\d{2}\.jsonl)$")


class ManifestError(ValueError):
    """The manifest is missing, malformed, or names a file outside the allowed shape."""


@dataclass
class FetchStats:
    downloaded: List[str] = field(default_factory=list)
    unchanged: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)


def parse_manifest(text: str) -> List[Tuple[str, str]]:
    """Return ``[(sha256, filename), ...]`` from ``sha256sum`` output.

    ``filename`` is the bare basename; the ``snapshots/`` prefix is required in
    the manifest and stripped here.
    """
    entries: List[Tuple[str, str]] = []
    seen = set()
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        match = _ENTRY_RE.match(line)
        if not match:
            raise ManifestError(f"{MANIFEST} line {lineno} is not a valid snapshot entry: {line!r}")
        digest, relpath = match.groups()
        name = relpath.split("/", 1)[1]
        if name in seen:
            raise ManifestError(f"{MANIFEST} lists {name} twice")
        seen.add(name)
        entries.append((digest, name))
    if not entries:
        raise ManifestError(f"{MANIFEST} is empty")
    return entries


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _raw_url(repo: str, ref: str, path: str) -> str:
    return f"{RAW_BASE}/{repo}/{ref}/{path}"


def _get(client: httpx.Client, url: str, max_bytes: int) -> bytes:
    resp = client.get(url)
    resp.raise_for_status()
    if len(resp.content) > max_bytes:
        raise ValueError(f"{url} exceeds {max_bytes} bytes")
    return resp.content


def _write_verified(content: bytes, expected: str, target: Path) -> None:
    """Write ``content`` to ``target`` atomically, only if its hash is ``expected``."""
    actual = hashlib.sha256(content).hexdigest()
    if actual != expected:
        raise ValueError(f"hash mismatch for {target.name}: manifest {expected}, downloaded {actual}")
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".part")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.replace(tmp, target)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def fetch_snapshots(
    dest: Path = DEFAULT_DEST,
    *,
    repo: str = DEFAULT_REPO,
    ref: str = DEFAULT_REF,
    client: Optional[httpx.Client] = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    timeout: float = DEFAULT_TIMEOUT,
) -> FetchStats:
    """Mirror the data repository's snapshots into ``dest``; see the module docstring."""
    if not _REPO_RE.match(repo):
        raise ValueError(f"invalid repository {repo!r} (expected owner/name)")
    if not _REF_RE.match(ref) or ".." in ref:
        raise ValueError(f"invalid ref {ref!r}")

    own_client = client is None
    http = client or httpx.Client(timeout=timeout, follow_redirects=True)
    stats = FetchStats()
    try:
        try:
            manifest = _get(http, _raw_url(repo, ref, MANIFEST), max_bytes).decode("utf-8")
        except httpx.HTTPError as exc:
            raise ManifestError(f"could not fetch {MANIFEST} from {repo}@{ref}: {exc}") from exc
        entries = parse_manifest(manifest)
        dest.mkdir(parents=True, exist_ok=True)

        for expected, name in entries:
            target = dest / name
            if target.exists():
                if sha256_file(target) == expected:
                    stats.unchanged.append(name)
                    continue
                remote = target.with_name(name + ".remote")
                _write_verified(_get(http, _raw_url(repo, ref, f"snapshots/{name}"), max_bytes), expected, remote)
                stats.conflicts.append(name)
                logger.warning("snapshot_conflict_kept_local", file=name, remote_copy=str(remote))
                continue
            _write_verified(_get(http, _raw_url(repo, ref, f"snapshots/{name}"), max_bytes), expected, target)
            stats.downloaded.append(name)
            logger.info("snapshot_downloaded", file=name)
    finally:
        if own_client:
            http.close()
    return stats


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.fetch_snapshots",
        description="Download and hash-verify RSS snapshots from the cats-snapshots data repository.",
    )
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST, help="local snapshot directory")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="data repository (owner/name)")
    parser.add_argument(
        "--ref", default=DEFAULT_REF, help="branch, tag or commit to fetch (pin a commit for reproducibility)"
    )
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="per-request HTTP timeout in seconds")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="reject any file larger than this")
    args = parser.parse_args(argv)

    try:
        stats = fetch_snapshots(args.dest, repo=args.repo, ref=args.ref, max_bytes=args.max_bytes, timeout=args.timeout)
    except (ManifestError, ValueError, httpx.HTTPError) as exc:
        logger.error("fetch_snapshots_failed", error=str(exc))
        return 1

    logger.info(
        "fetch_snapshots_done",
        downloaded=len(stats.downloaded),
        unchanged=len(stats.unchanged),
        conflicts=len(stats.conflicts),
        dest=str(args.dest),
    )
    if stats.conflicts:
        logger.error(
            "fetch_snapshots_conflicts",
            files=stats.conflicts,
            hint="local files were kept; union each with its .remote copy via "
            "python -m cats.calibration.merge_snapshots --inputs <file> <file>.remote --out <file>",
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
