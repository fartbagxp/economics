"""Update the auto-generated dashboard section in README.md."""

import re
from datetime import datetime, timezone
from pathlib import Path

from src.sparkline import build_dashboard

START_MARKER = "<!-- ECONOMIC-DATA-START -->"
END_MARKER = "<!-- ECONOMIC-DATA-END -->"
DATASET_COUNT_RE = re.compile(
    r"<!-- DATASET-COUNT -->.*?<!-- /DATASET-COUNT -->", re.DOTALL
)


def _dataset_count_badge(count: int) -> str:
    badge = f"https://img.shields.io/badge/datasets-{count}-blue?style=flat-square"
    return f"<!-- DATASET-COUNT -->\n![{count} datasets]({badge})\n<!-- /DATASET-COUNT -->"


def update_readme(readme_path: str = "README.md", data_dir: str = "data/raw"):
    path = Path(readme_path)
    content = path.read_text()

    if START_MARKER not in content or END_MARKER not in content:
        raise ValueError(
            f"README.md is missing sentinel markers:\n  {START_MARKER}\n  {END_MARKER}"
        )

    dataset_count = len(list(Path(data_dir).glob("*.csv")))
    content = DATASET_COUNT_RE.sub(_dataset_count_badge(dataset_count), content)

    dashboard = build_dashboard(data_dir)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    block = (
        f"{START_MARKER}\n"
        f"## Economic Dashboard\n\n"
        f"_Last updated: {now}_\n\n"
        f"{dashboard}"
        f"{END_MARKER}"
    )

    start = content.index(START_MARKER)
    end = content.index(END_MARKER) + len(END_MARKER)
    new_content = content[:start] + block + content[end:]
    path.write_text(new_content)
    print(f"README.md updated ({now}), {dataset_count} datasets")


if __name__ == "__main__":
    update_readme()
