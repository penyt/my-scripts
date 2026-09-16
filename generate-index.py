#!/usr/bin/env python3

from pathlib import Path
from html import escape
from datetime import datetime
from urllib.parse import quote

ROOT = Path("public")

# Files hidden from directory listings
HIDDEN_FILES = {
    "index.html",
    "_headers",
    "_redirects",
}

CSS = """
body {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
                 "Liberation Mono", "Courier New", monospace;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
    color: #222;
}

h1 {
    font-size: 1.4rem;
    font-weight: 600;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    text-align: left;
    padding: 6px 12px 6px 0;
    white-space: nowrap;
}

th {
    border-bottom: 1px solid #aaa;
}

.name {
    width: 60%;
}

.size {
    width: 15%;
}

.modified {
    width: 25%;
}

a {
    color: #0645ad;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

@media (max-width: 600px) {
    body {
        margin: 20px auto;
    }

    .modified {
        display: none;
    }
}
"""


def human_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.1f} {unit}"

        value /= 1024

    return f"{value:.1f} TB"


def format_time(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")


def should_hide(path: Path) -> bool:
    if path.name in HIDDEN_FILES:
        return True

    if path.name.startswith("."):
        return True

    return False


def generate_index(directory: Path) -> None:
    relative = directory.relative_to(ROOT)

    if relative == Path("."):
        url_path = "/"
    else:
        url_path = "/" + relative.as_posix() + "/"

    entries = []

    # Sort directories first, then sort entries alphabetically
    paths = sorted(
        directory.iterdir(),
        key=lambda p: (
            not p.is_dir(),
            p.name.lower(),
        ),
    )

    for path in paths:
        if should_hide(path):
            continue

        stat = path.stat()

        if path.is_dir():
            display_name = path.name + "/"
            href = quote(path.name) + "/"
            size = "-"
        else:
            display_name = path.name
            href = quote(path.name)
            size = human_size(stat.st_size)

        modified = format_time(stat.st_mtime)

        entries.append(
            f"""
            <tr>
                <td class="name">
                    <a href="{escape(href)}">{escape(display_name)}</a>
                </td>
                <td class="size">{escape(size)}</td>
                <td class="modified">{escape(modified)}</td>
            </tr>
            """
        )

    parent = ""

    if relative != Path("."):
        parent = """
            <tr>
                <td class="name">
                    <a href="../">../</a>
                </td>
                <td class="size">-</td>
                <td class="modified">-</td>
            </tr>
        """

    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Index of {escape(url_path)}</title>

    <style>
{CSS}
    </style>
</head>

<body>

    <h1>Index of {escape(url_path)}</h1>

    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Size</th>
                <th>Modified</th>
            </tr>
        </thead>

        <tbody>
            {parent}
            {"".join(entries)}
        </tbody>
    </table>

</body>
</html>
"""

    output = directory / "index.html"
    output.write_text(html, encoding="utf-8")

    print(f"Generated: {output}")


def main() -> None:
    if not ROOT.exists():
        raise SystemExit(f"Error: {ROOT}/ does not exist")

    if not ROOT.is_dir():
        raise SystemExit(f"Error: {ROOT}/ is not a directory")

    # Collect all directories before generating index files
    directories = [ROOT]

    directories.extend(
        path
        for path in ROOT.rglob("*")
        if path.is_dir() and not path.name.startswith(".")
    )

    for directory in directories:
        generate_index(directory)

    print(f"Generated {len(directories)} directory indexes.")


if __name__ == "__main__":
    main()
