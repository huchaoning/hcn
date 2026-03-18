import os, git, threading, warnings, socket
from importlib.metadata import version, PackageNotFoundError

__all__ = []


try:
    __version__ = version('hcn')
except PackageNotFoundError:
    __version__ = 'unknown'


def _has_network(host='8.8.8.8', port=53):
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def _check_update():
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.abspath(os.path.join(current_dir, '..', '..'))

    try:
        repo = git.Repo(repo_path)
        
        if repo.is_dirty():
            warnings.warn('Local changes detected.')

        if not _has_network():
            warnings.warn('No network connection. Remote update check skipped.')
        
        else:
            try:
                repo.remotes.origin.fetch(kill_after_timeout=5)
                active_branch = repo.active_branch
                remote_ref = repo.remotes.origin.refs[active_branch.name]
                
                behind = list(repo.iter_commits(f'{active_branch.name}..{remote_ref}'))
                if behind:
                    warnings.warn(f'Remote update detected. {len(behind)} commits behind.')
            except Exception as git_err:
                warnings.warn(f'Remote check failed: {git_err}')

    except Exception as e:
        warnings.warn(f'Git check failed: {e}')


threading.Thread(target=_check_update, daemon=True).start()

