import io
import tarfile
import zipfile
from collections.abc import Iterable
from pathlib import Path

import pytest

from scripts.inspect_distribution import (
    DistributionInspectionError,
    ExpectedMetadata,
    inspect_distributions,
)

EXPECTED = ExpectedMetadata(
    name="broute-j11",
    version="0.1.0",
    requires_python=">=3.11",
    license_expression="MIT",
)
DIST_INFO = "broute_j11-0.1.0.dist-info"
SDIST_ROOT = "broute_j11-0.1.0"


def write_wheel(
    path: Path,
    *,
    omit: Iterable[str] = (),
    metadata_name: str = "broute-j11",
) -> None:
    members = {
        "broute_j11/__init__.py": b'__version__ = "0.1.0"\n',
        "broute_j11/py.typed": b"PEP 561\n",
        f"{DIST_INFO}/licenses/LICENSE": b"MIT License\n",
        f"{DIST_INFO}/METADATA": (
            "Metadata-Version: 2.4\n"
            f"Name: {metadata_name}\n"
            "Version: 0.1.0\n"
            "Requires-Python: >=3.11\n"
            "License-Expression: MIT\n"
            "Description-Content-Type: text/markdown\n"
        ).encode(),
    }
    with zipfile.ZipFile(path, "w") as archive:
        for name, contents in members.items():
            if name not in omit:
                archive.writestr(name, contents)


def write_sdist(path: Path, *, omit: Iterable[str] = ()) -> None:
    members = {
        f"{SDIST_ROOT}/LICENSE": b"MIT License\n",
        f"{SDIST_ROOT}/README.md": b"# broute-j11\n",
        f"{SDIST_ROOT}/pyproject.toml": b'[project]\nname = "broute-j11"\n',
        f"{SDIST_ROOT}/src/broute_j11/__init__.py": b'__version__ = "0.1.0"\n',
        f"{SDIST_ROOT}/src/broute_j11/py.typed": b"PEP 561\n",
    }
    with tarfile.open(path, "w:gz") as archive:
        for name, contents in members.items():
            if name in omit:
                continue
            info = tarfile.TarInfo(name)
            info.size = len(contents)
            archive.addfile(info, io.BytesIO(contents))


def test_inspection_accepts_expected_artifacts(tmp_path: Path) -> None:
    wheel = tmp_path / "broute_j11-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "broute_j11-0.1.0.tar.gz"
    write_wheel(wheel)
    write_sdist(sdist)

    inspect_distributions(wheel, sdist, EXPECTED)


@pytest.mark.parametrize(
    "missing_member",
    [
        "broute_j11/__init__.py",
        "broute_j11/py.typed",
        f"{DIST_INFO}/licenses/LICENSE",
    ],
)
def test_inspection_rejects_missing_wheel_member(tmp_path: Path, missing_member: str) -> None:
    wheel = tmp_path / "broute_j11-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "broute_j11-0.1.0.tar.gz"
    write_wheel(wheel, omit=[missing_member])
    write_sdist(sdist)

    with pytest.raises(DistributionInspectionError, match="missing required files"):
        inspect_distributions(wheel, sdist, EXPECTED)


def test_inspection_rejects_incorrect_metadata(tmp_path: Path) -> None:
    wheel = tmp_path / "broute_j11-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "broute_j11-0.1.0.tar.gz"
    write_wheel(wheel, metadata_name="wrong-name")
    write_sdist(sdist)

    with pytest.raises(DistributionInspectionError, match="Name"):
        inspect_distributions(wheel, sdist, EXPECTED)


@pytest.mark.parametrize(
    "missing_member",
    [
        f"{SDIST_ROOT}/LICENSE",
        f"{SDIST_ROOT}/README.md",
        f"{SDIST_ROOT}/pyproject.toml",
        f"{SDIST_ROOT}/src/broute_j11/__init__.py",
        f"{SDIST_ROOT}/src/broute_j11/py.typed",
    ],
)
def test_inspection_rejects_missing_sdist_member(tmp_path: Path, missing_member: str) -> None:
    wheel = tmp_path / "broute_j11-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "broute_j11-0.1.0.tar.gz"
    write_wheel(wheel)
    write_sdist(sdist, omit=[missing_member])

    with pytest.raises(DistributionInspectionError, match="missing required files"):
        inspect_distributions(wheel, sdist, EXPECTED)
