import re


__version__ = "0.1.0"
version_info = tuple(
    int(p) for p in re.match(r"(\d+).(\d+).(\d+)", __version__).groups()
)
