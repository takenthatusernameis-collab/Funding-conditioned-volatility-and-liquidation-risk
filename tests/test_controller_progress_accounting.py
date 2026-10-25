import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "controller_progress.py"


def run_git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)


def make_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run_git(repo, "init", "-q")
    run_git(repo, "config", "user.email", "t@t.com")
    run_git(repo, "config", "user.name", "t")
    (repo / "README.md").write_text("x\n")
    run_git(repo, "add", "README.md")
    run_git(repo, "commit", "-q", "-m", "init")
    base = run_git(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, base


def run_script(repo, base, head, remote=None):
    cmd = [sys.executable, str(SCRIPT), "--base-sha", base, "--head-sha", head]
    if remote is not None:
        cmd += ["--verified-remote-sha", remote]
    return subprocess.run(cmd, cwd=repo, capture_output=True, text=True)


def test_no_change_not_credited(tmp_path):
    repo, base = make_repo(tmp_path)
    head = base
    r = run_script(repo, base, head)
    assert r.returncode != 0


def test_meaningful_change_credited(tmp_path):
    repo, base = make_repo(tmp_path)
    (repo / "src.py").write_text("y\n")
    run_git(repo, "add", "src.py")
    run_git(repo, "commit", "-q", "-m", "change")
    head = run_git(repo, "rev-parse", "HEAD").stdout.strip()
    r = run_script(repo, base, head)
    assert r.returncode == 0


def test_workflow_only_not_credited(tmp_path):
    repo, base = make_repo(tmp_path)
    (repo / ".github").mkdir(exist_ok=True)
    (repo / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (repo / ".github" / "workflows" / "x.yml").write_text("y\n")
    run_git(repo, "add", ".github/workflows/x.yml")
    run_git(repo, "commit", "-q", "-m", "wf")
    head = run_git(repo, "rev-parse", "HEAD").stdout.strip()
    r = run_script(repo, base, head)
    assert r.returncode != 0


def test_invalid_sha_fails_closed(tmp_path):
    repo, base = make_repo(tmp_path)
    r = run_script(repo, base, "deadbeef")
    assert r.returncode != 0
    r = run_script(repo, "deadbeef", base)
    assert r.returncode != 0


def test_verified_remote_must_match_head(tmp_path):
    repo, base = make_repo(tmp_path)
    (repo / "src.py").write_text("y\n")
    run_git(repo, "add", "src.py")
    run_git(repo, "commit", "-q", "-m", "change")
    head = run_git(repo, "rev-parse", "HEAD").stdout.strip()
    r = run_script(repo, base, head, remote=base)
    assert r.returncode != 0
    r = run_script(repo, base, head, remote=head)
    assert r.returncode == 0


def test_marker_only_commit_not_credited(tmp_path):
    repo, base = make_repo(tmp_path)
    (repo / "marker.txt").write_text("progress\n")
    run_git(repo, "add", "marker.txt")
    run_git(repo, "commit", "-q", "-m", "marker")
    (repo / "marker.txt").unlink()
    run_git(repo, "rm", "-q", "marker.txt")
    run_git(repo, "commit", "-q", "-m", "remove marker")
    head = run_git(repo, "rev-parse", "HEAD").stdout.strip()
    # net no change -> no meaningful
    r = run_script(repo, base, head)
    assert r.returncode != 0
