from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parents[1]


def load_workflow(name: str) -> dict[str, Any]:
    with (ROOT / ".github" / "workflows" / name).open(encoding="utf-8") as workflow_file:
        return yaml.load(workflow_file, Loader=yaml.BaseLoader)  # type: ignore[no-any-return]


def test_tag_publish_requires_full_ci_and_a_tested_main_commit() -> None:
    ci = load_workflow("ci.yml")
    publish = load_workflow("publish.yml")

    assert "workflow_call" in ci["on"]
    assert publish["jobs"]["verify"] == {"uses": "./.github/workflows/ci.yml"}

    publish_job = publish["jobs"]["publish"]
    assert publish_job["needs"] == "verify"

    checkout = publish_job["steps"][0]
    assert checkout["uses"] == "actions/checkout@v7"
    assert checkout["with"]["fetch-depth"] == "0"

    commands = "\n".join(step.get("run", "") for step in publish_job["steps"])
    assert "git merge-base --is-ancestor" in commands
    assert "GITHUB_SHA" in commands
    assert "origin/main" in commands
    assert "GITHUB_REF_NAME" in commands
    assert "package_version" in commands


def test_ci_and_publish_inspect_the_built_distributions() -> None:
    ci = load_workflow("ci.yml")
    publish = load_workflow("publish.yml")

    ci_commands = "\n".join(step.get("run", "") for step in ci["jobs"]["package"]["steps"])
    publish_commands = "\n".join(step.get("run", "") for step in publish["jobs"]["publish"]["steps"])
    inspection_command = "python scripts/inspect_distribution.py dist/*.whl dist/*.tar.gz"

    assert inspection_command in ci_commands
    assert inspection_command in publish_commands
