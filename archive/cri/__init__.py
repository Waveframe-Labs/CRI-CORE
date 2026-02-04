try:
    from __init__ import __version__  # reuse root version if present
except Exception:
    __version__ = "0.1.0"
