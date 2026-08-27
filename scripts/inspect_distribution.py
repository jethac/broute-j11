"""Validate built distributions before they are uploaded."""

from __future__ import annotations

import argparse
import email
import tarfile
import tomllib
import zipfile
from dataclasses import dataclass
from pathlib import Path


class DistributionInspectionError(ValueError):
    """Raised when a distribution does not satisfy the package contract."""


@dataclass(frozen=True)
class ExpectedMetadata:
    """Project metadata that built distributions must preserve."""

    name: str
    version: str
    requires_python: str
    license_expression: str

    @classmethod
    def from_pyproject(cls, path: Path) -> ExpectedMetadata:
        """Read expected values from PEP 621 project metadata."""
        with path.open("rb") as pyproject_file:
            project = tomllib.load(pyproject_file)["project"]
        return cls(
            name=project["name"],
            version=project["version"],
            requires_python=project["requires-python"],
            license_expression=project["license"],
        )


def require_members(archive_name: str, members: set[str], required: set[str]) -> None:
    """Reject an archive that omits required paths."""
    missing = required - members
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise DistributionInspectionError(f"{archive_name} is missing required files: {missing_list}")


def inspect_distributions(wheel: Path, sdist: Path, expected: ExpectedMetadata) -> None:
    """Assert that wheel and sdist contents match declared project metadata."""
    normalized_name = expected.name.replace("-", "_")
    dist_info = f"{normalized_name}-{expected.version}.dist-info"
    package_init = f"{normalized_name}/__init__.py"
    type_marker = f"{normalized_name}/py.typed"
    metadata_path = f"{dist_info}/METADATA"
    wheel_license = f"{dist_info}/licenses/LICENSE"

    with zipfile.ZipFile(wheel) as wheel_archive:
        wheel_members = set(wheel_archive.namelist())
        require_members(
            wheel.name,
            wheel_members,
            {package_init, type_marker, metadata_path, wheel_license},
        )
        if not wheel_archive.read(package_init).strip():
            raise DistributionInspectionError(f"{package_init} is empty")
        if not wheel_archive.read(wheel_license).strip():
            raise DistributionInspectionError(f"{wheel_license} is empty")
        metadata = email.message_from_bytes(wheel_archive.read(metadata_path))

    expected_headers = {
        "Name": expected.name,
        "Version": expected.version,
        "Requires-Python": expected.requires_python,
        "License-Expression": expected.license_expression,
        "Description-Content-Type": "text/markdown",
    }
    for header, expected_value in expected_headers.items():
        actual_value = metadata[header]
        if actual_value != expected_value:
            raise DistributionInspectionError(f"METADATA {header} is {actual_value!r}, expected {expected_value!r}")

    sdist_root = f"{normalized_name}-{expected.version}"
    required_sdist_members = {
        f"{sdist_root}/LICENSE",
        f"{sdist_root}/README.md",
        f"{sdist_root}/pyproject.toml",
        f"{sdist_root}/src/{package_init}",
        f"{sdist_root}/src/{type_marker}",
    }
    with tarfile.open(sdist, "r:gz") as sdist_archive:
        sdist_members = set(sdist_archive.getnames())
        require_members(sdist.name, sdist_members, required_sdist_members)
        for member in required_sdist_members:
            extracted = sdist_archive.extractfile(member)
            if extracted is None or not extracted.read().strip():
                raise DistributionInspectionError(f"{member} is empty")


def main() -> None:
    """Run distribution inspection from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("sdist", type=Path)
    parser.add_argument("--pyproject", type=Path, default=Path("pyproject.toml"))
    args = parser.parse_args()

    try:
        expected = ExpectedMetadata.from_pyproject(args.pyproject)
        inspect_distributions(args.wheel, args.sdist, expected)
    except (DistributionInspectionError, KeyError, OSError, tarfile.TarError, zipfile.BadZipFile) as error:
        parser.exit(1, f"distribution inspection failed: {error}\n")

    print(
        f"verified {args.wheel.name} and {args.sdist.name}: "
        f"{expected.name} {expected.version}, package files, metadata, README, and license"
    )


if __name__ == "__main__":
    main()
