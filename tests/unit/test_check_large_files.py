import subprocess

import pytest

from scripts.check_large_files import main, new_blobs, oversized, unchanged_since_head

LIMIT = 1000


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "test@example.invalid")
    _git(tmp_path, "config", "user.name", "Test")
    _git(tmp_path, "config", "commit.gpgsign", "false")
    (tmp_path / "legacy_big.jsonl").write_bytes(b"x" * (LIMIT + 500))
    (tmp_path / "small.txt").write_bytes(b"ok")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "base")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_oversized_is_strictly_greater_than_the_limit():
    assert oversized([("a", LIMIT), ("b", LIMIT + 1)], LIMIT) == [("b", LIMIT + 1)]


def test_precommit_mode_skips_untouched_legacy_files(repo):
    # `pre-commit run --all-files` passes every tracked file: an existing large file nobody changed must pass.
    assert unchanged_since_head(["legacy_big.jsonl"]) == ["legacy_big.jsonl"]
    assert main(["legacy_big.jsonl", "small.txt", "--max-bytes", str(LIMIT)]) == 0


def test_precommit_mode_flags_a_modified_legacy_file(repo, capsys):
    with (repo / "legacy_big.jsonl").open("ab") as handle:
        handle.write(b"more")
    assert main(["legacy_big.jsonl", "--max-bytes", str(LIMIT)]) == 1
    assert "legacy_big.jsonl" in capsys.readouterr().err


def test_precommit_mode_flags_a_new_large_file(repo):
    (repo / "new_big.bin").write_bytes(b"y" * (LIMIT + 1))
    _git(repo, "add", "new_big.bin")
    assert main(["new_big.bin", "--max-bytes", str(LIMIT)]) == 1


def test_ci_mode_checks_only_files_added_or_modified_since_base(repo, capsys):
    _git(repo, "checkout", "-q", "-b", "feature")
    (repo / "small.txt").write_bytes(b"still small")
    _git(repo, "commit", "-qam", "touch small")
    assert [path for path, _ in new_blobs("main", "HEAD")] == ["small.txt"]
    assert main(["--base", "main", "--max-bytes", str(LIMIT)]) == 0

    (repo / "added_big.bin").write_bytes(b"z" * (LIMIT + 1))
    _git(repo, "add", "added_big.bin")
    _git(repo, "commit", "-qm", "add big")
    assert main(["--base", "main", "--max-bytes", str(LIMIT)]) == 1
    err = capsys.readouterr().err
    assert "added_big.bin" in err and "legacy_big.jsonl" not in err


def test_ci_mode_ignores_deleted_files(repo):
    _git(repo, "checkout", "-q", "-b", "cleanup")
    _git(repo, "rm", "-q", "legacy_big.jsonl")
    _git(repo, "commit", "-qm", "drop legacy")
    assert main(["--base", "main", "--max-bytes", str(LIMIT)]) == 0


def test_files_and_base_are_mutually_exclusive(repo):
    with pytest.raises(SystemExit):
        main(["small.txt", "--base", "main"])


def test_ci_mode_flags_a_large_blob_removed_by_a_later_commit(repo, capsys):
    # With merge commits, an intermediate commit's blob reaches main even if the PR's final tree drops it.
    _git(repo, "checkout", "-q", "-b", "oops")
    (repo / "dump.bin").write_bytes(b"d" * (LIMIT + 1))
    _git(repo, "add", "dump.bin")
    _git(repo, "commit", "-qm", "add dump")
    _git(repo, "rm", "-q", "dump.bin")
    _git(repo, "commit", "-qm", "remove dump")
    assert main(["--base", "main", "--max-bytes", str(LIMIT)]) == 1
    assert "dump.bin" in capsys.readouterr().err


def test_symlinks_are_not_followed(repo):
    (repo / "link").symlink_to("legacy_big.jsonl")
    assert main(["link", "--max-bytes", str(LIMIT)]) == 0
    _git(repo, "checkout", "-q", "-b", "with-link")
    _git(repo, "add", "link")
    _git(repo, "commit", "-qm", "add link")
    assert main(["--base", "main", "--max-bytes", str(LIMIT)]) == 0


def test_unknown_base_fails_with_a_readable_error(repo, capsys):
    assert main(["--base", "0" * 40, "--max-bytes", str(LIMIT)]) == 2
    assert "git failed" in capsys.readouterr().err
