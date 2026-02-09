from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('hcn')
except PackageNotFoundError:
    __version__ = 'unknown'