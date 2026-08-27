from pathlib import Path

from broute_j11 import __version__


def test_initial_version() -> None:
    assert __version__ == "0.1.0"


def test_package_declares_inline_types() -> None:
    assert Path("src/broute_j11/py.typed").is_file()
