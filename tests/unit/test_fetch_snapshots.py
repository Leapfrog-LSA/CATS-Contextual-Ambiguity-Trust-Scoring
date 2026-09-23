from __future__ import annotations

import hashlib
from typing import Dict

import httpx
import pytest

from cats.calibration import fetch_snapshots as fs

SNAP_A = b'{"source_id": "a", "messages": [{"timestamp": "2026-09-24T06:00:00Z", "text": "uno"}]}\n'
SNAP_B = b'{"source_id": "b", "messages": [{"timestamp": "2026-09-25T06:00:00Z", "text": "due"}]}\n'
NAME_A = "labelled_sources_2026-09-24.jsonl"
NAME_B = "labelled_sources_2026-09-25.jsonl"
BASE = "https://raw.githubusercontent.com/Leapfrog-LSA/cats-snapshots/main"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _manifest(files: Dict[str, bytes]) -> str:
    return "".join(f"{_sha(data)}  snapshots/{name}\n" for name, data in files.items())


def _client(routes: Dict[str, bytes], calls: list) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        body = routes.get(str(request.url))
        if body is None:
            return httpx.Response(404)
        return httpx.Response(200, content=body)

    return httpx.Client(transport=httpx.MockTransport(handler))


def _routes(files: Dict[str, bytes], manifest: str | None = None) -> Dict[str, bytes]:
    routes = {f"{BASE}/SHA256SUMS": (manifest if manifest is not None else _manifest(files)).encode()}
    routes.update({f"{BASE}/snapshots/{name}": data for name, data in files.items()})
    return routes


def test_parse_manifest_accepts_sha256sum_output_both_modes():
    text = f"{'a' * 64}  snapshots/{NAME_A}\n{'b' * 64} *snapshots/{NAME_B}\n\n"
    assert fs.parse_manifest(text) == [("a" * 64, NAME_A), ("b" * 64, NAME_B)]


@pytest.mark.parametrize(
    "line",
    [
        f"{'a' * 64}  ../etc/{NAME_A}",
        f"{'a' * 64}  snapshots/../../{NAME_A}",
        f"{'a' * 64}  /abs/{NAME_A}",
        f"{'a' * 64}  snapshots/other.jsonl",
        f"{'A' * 64}  snapshots/{NAME_A}",
        f"{'a' * 63}  snapshots/{NAME_A}",
    ],
)
def test_parse_manifest_rejects_unexpected_paths_and_hashes(line):
    with pytest.raises(fs.ManifestError):
        fs.parse_manifest(line + "\n")


def test_parse_manifest_rejects_empty_and_duplicates():
    with pytest.raises(fs.ManifestError):
        fs.parse_manifest("\n")
    with pytest.raises(fs.ManifestError):
        fs.parse_manifest(f"{'a' * 64}  snapshots/{NAME_A}\n{'b' * 64}  snapshots/{NAME_A}\n")


def test_downloads_missing_files_and_verifies_hashes(tmp_path):
    files = {NAME_A: SNAP_A, NAME_B: SNAP_B}
    calls: list = []
    stats = fs.fetch_snapshots(tmp_path, client=_client(_routes(files), calls))

    assert sorted(stats.downloaded) == [NAME_A, NAME_B]
    assert stats.unchanged == [] and stats.conflicts == []
    assert (tmp_path / NAME_A).read_bytes() == SNAP_A
    assert (tmp_path / NAME_B).read_bytes() == SNAP_B
    assert not list(tmp_path.glob("*.part"))


def test_matching_local_file_is_not_downloaded_again(tmp_path):
    (tmp_path / NAME_A).write_bytes(SNAP_A)
    files = {NAME_A: SNAP_A, NAME_B: SNAP_B}
    calls: list = []
    stats = fs.fetch_snapshots(tmp_path, client=_client(_routes(files), calls))

    assert stats.unchanged == [NAME_A]
    assert stats.downloaded == [NAME_B]
    assert f"{BASE}/snapshots/{NAME_A}" not in calls


def test_differing_local_file_is_never_overwritten(tmp_path):
    local = b'{"source_id": "a", "messages": [{"timestamp": "2026-09-24T07:00:00Z", "text": "solo locale"}]}\n'
    (tmp_path / NAME_A).write_bytes(local)
    stats = fs.fetch_snapshots(tmp_path, client=_client(_routes({NAME_A: SNAP_A}), []))

    assert stats.conflicts == [NAME_A]
    assert (tmp_path / NAME_A).read_bytes() == local
    assert (tmp_path / (NAME_A + ".remote")).read_bytes() == SNAP_A
    # The remote copy stays out of the *.jsonl glob consumers use.
    assert [p.name for p in tmp_path.glob("*.jsonl")] == [NAME_A]


def test_hash_mismatch_on_download_fails_and_leaves_nothing(tmp_path):
    routes = _routes({NAME_A: SNAP_A}, manifest=f"{'0' * 64}  snapshots/{NAME_A}\n")
    with pytest.raises(ValueError, match="hash mismatch"):
        fs.fetch_snapshots(tmp_path, client=_client(routes, []))
    assert list(tmp_path.iterdir()) == []


def test_missing_manifest_is_a_manifest_error(tmp_path):
    with pytest.raises(fs.ManifestError):
        fs.fetch_snapshots(tmp_path, client=_client({}, []))


def test_oversized_file_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="exceeds"):
        fs.fetch_snapshots(tmp_path, client=_client(_routes({NAME_A: SNAP_A}), []), max_bytes=len(SNAP_A) - 1)


@pytest.mark.parametrize("repo,ref", [("not-a-repo", "main"), ("a/b/c", "main"), ("a/b", "../main"), ("a/b", "ma in")])
def test_rejects_invalid_repo_and_ref(tmp_path, repo, ref):
    with pytest.raises(ValueError):
        fs.fetch_snapshots(tmp_path, repo=repo, ref=ref, client=_client({}, []))


def test_main_exit_codes(tmp_path, monkeypatch):
    files = {NAME_A: SNAP_A}
    real_client = httpx.Client
    mocked = _client(_routes(files), [])

    def fake_client(*args, **kwargs):
        return real_client(transport=mocked._transport)

    monkeypatch.setattr(fs.httpx, "Client", fake_client)
    assert fs.main(["--dest", str(tmp_path)]) == 0
    assert (tmp_path / NAME_A).read_bytes() == SNAP_A

    (tmp_path / NAME_A).write_bytes(b"diverso\n")
    assert fs.main(["--dest", str(tmp_path)]) == 1
    assert (tmp_path / NAME_A).read_bytes() == b"diverso\n"

    monkeypatch.setattr(fs.httpx, "Client", real_client)
    assert fs.main(["--dest", str(tmp_path), "--repo", "not-a-repo"]) == 1
