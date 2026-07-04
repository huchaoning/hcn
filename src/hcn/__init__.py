import os
import threading
import warnings
import socket
from importlib.metadata import version, PackageNotFoundError

__all__ = []


try:
    __version__ = version("hcn")
except PackageNotFoundError:
    __version__ = "unknown"


def _has_network(host="8.8.8.8", port=53):
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def _is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))


def _check_git_update(repo_path):
    try:
        import git

        repo = git.Repo(repo_path)

        if repo.is_dirty():
            warnings.warn("Local changes detected.")

        try:
            repo.remotes.origin.fetch(kill_after_timeout=5)
            active_branch = repo.active_branch
            remote_ref = repo.remotes.origin.refs[active_branch.name]
            behind = list(repo.iter_commits(f"{active_branch.name}..{remote_ref}"))
            if behind:
                warnings.warn(f"Remote update detected. {len(behind)} commits behind.")
        except Exception as git_err:
            warnings.warn(f"Remote check failed: {git_err}")

    except Exception as e:
        warnings.warn(f"Git check failed: {e}")


def _check_pypi_update():
    try:
        import requests
        from packaging.version import parse as parse_version

        current = __version__
        if current == "unknown":
            return

        url = "https://pypi.org/pypi/hcn/json"

        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            latest = data["info"]["version"]

        if parse_version(latest) > parse_version(current):
            warnings.warn(
                f"PyPI update available: {current} -> {latest}. Run `pip install --upgrade hcn` to upgrade."
            )
    except Exception as e:
        warnings.warn(f"PyPI version check failed: {e}")


def _check_update():
    if os.environ.get("HCN_NO_UPDATE_CHECK") == "1":
        return

    if "dev" in __version__.lower():
        warnings.warn(f"Running in development version: {__version__}")
    elif __version__ == "unknown":
        warnings.warn("Version unknown.")

    if not _has_network():
        warnings.warn("No network connection. Remote update check skipped.")
        return

    current_dir = os.path.dirname(__file__)
    repo_path = os.path.abspath(os.path.join(current_dir, "..", ".."))

    if _is_git_repo(repo_path):
        _check_git_update(repo_path)
    else:
        _check_pypi_update()


threading.Thread(target=_check_update, daemon=True).start()
