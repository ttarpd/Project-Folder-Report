#!/usr/bin/env python3

import os
import platform
import re
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path


# =========================
# CONFIGURATION
# =========================

IGNORED_FOLDERS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
}

SOURCE_EXTENSIONS = {
    ".py",
    ".ps1",
    ".js",
    ".ts",
    ".sql",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".sh",
    ".bash",
    ".toml",
    ".ini",
}


# =========================
# HELPERS
# =========================

def human_size(size):
    """Convert bytes into readable units."""

    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def file_timestamp(path):
    """Return formatted modified date."""

    timestamp = os.path.getmtime(path)

    return datetime.fromtimestamp(
        timestamp
    ).strftime("%Y-%m-%d %H:%M:%S")


def read_text_file(path):
    """Safely read text files."""

    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()

    except UnicodeDecodeError:
        return "[Binary or non UTF-8 file]"

    except Exception as error:
        return f"[Unable to read file: {error}]"


def format_generated_timestamp():
    """Return the current local date/time with timezone offset."""

    now = datetime.now().astimezone()

    offset = now.strftime("%z")

    if offset:
        offset = f"{offset[:3]}:{offset[3:]}"

    return f"{now.strftime('%Y-%m-%d %H:%M:%S')} {offset}".rstrip()


def run_git_command(source_folder, *args):
    """Run a Git command and return its output, or None on failure."""

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(source_folder),
                *args,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    except FileNotFoundError:
        return None

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def git_repository_metadata(source_folder):
    """
    Return Git metadata when source_folder is the root of a Git repository.

    A subdirectory inside a repository is not treated as the repository root.
    """

    source_folder = Path(source_folder).resolve()

    repository_root = run_git_command(
        source_folder,
        "rev-parse",
        "--show-toplevel",
    )

    if repository_root is None:
        return {
            "branch": "N/a",
            "commit": "N/a",
            "working_tree": "N/a",
        }

    try:
        repository_root = Path(repository_root).resolve()

        if os.path.normcase(repository_root) != os.path.normcase(source_folder):
            return {
                "branch": "N/a",
                "commit": "N/a",
                "working_tree": "N/a",
            }

    except OSError:
        return {
            "branch": "N/a",
            "commit": "N/a",
            "working_tree": "N/a",
        }

    branch = run_git_command(
        source_folder,
        "branch",
        "--show-current",
    )

    commit = run_git_command(
        source_folder,
        "rev-parse",
        "--short=7",
        "HEAD",
    )

    status = run_git_command(
        source_folder,
        "status",
        "--porcelain",
    )

    if branch == "":
        branch = "(detached HEAD)"

    if status is None:
        working_tree = "N/a"
    elif status == "":
        working_tree = "clean"
    else:
        working_tree = "dirty"

    return {
        "branch": branch or "N/a",
        "commit": commit or "N/a",
        "working_tree": working_tree,
    }


def project_metadata(source_folder):
    """Read project name and version from pyproject.toml when available."""

    pyproject_file = Path(source_folder) / "pyproject.toml"

    if not pyproject_file.is_file():
        return {
            "name": "Project",
            "version": "N/a",
        }

    try:
        with open(pyproject_file, "rb") as file:
            data = tomllib.load(file)

    except (OSError, tomllib.TOMLDecodeError):
        return {
            "name": "Project",
            "version": "N/a",
        }

    project = data.get("project", {})

    name = project.get("name")
    version = project.get("version")

    # Optional fallback for Poetry-style pyproject.toml files.
    poetry = data.get("tool", {}).get("poetry", {})

    if not name:
        name = poetry.get("name")

    if not version:
        version = poetry.get("version")

    return {
        "name": name or "Project",
        "version": version or "N/a",
    }


def find_previous_snapshot(output_file):
    """
    Find the immediately preceding timestamped report.

    Expected filename format:

        <prefix>_YYYYMMDD_HHMM.txt

    Example:

        NorthStar_Report_20260824_2305.txt
        NorthStar_Report_20260824_2056.txt
    """

    output_file = Path(output_file)

    pattern = re.compile(
        r"^(?P<prefix>.+)_"
        r"(?P<date>\d{8})_"
        r"(?P<time>\d{4})"
        r"\.txt$",
        re.IGNORECASE,
    )

    current_match = pattern.match(output_file.name)

    if current_match is None:
        return "N/a"

    current_prefix = current_match.group("prefix")
    current_timestamp = (
        current_match.group("date")
        + current_match.group("time")
    )

    candidates = []

    try:
        files = output_file.parent.iterdir()

    except OSError:
        return "N/a"

    for candidate in files:

        if not candidate.is_file():
            continue

        match = pattern.match(candidate.name)

        if match is None:
            continue

        if match.group("prefix") != current_prefix:
            continue

        timestamp = (
            match.group("date")
            + match.group("time")
        )

        if timestamp < current_timestamp:
            candidates.append(
                (
                    timestamp,
                    candidate.name,
                )
            )

    if not candidates:
        return "N/a"

    candidates.sort(reverse=True)

    return candidates[0][1]


def create_output_file(source_folder, output_directory):
    """Create a timestamped report filename in the specified output directory."""

    source_folder = Path(source_folder)
    output_directory = Path(output_directory)

    project_name = re.sub(
        r"\s+",
        "_",
        source_folder.name.strip(),
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M"
    )

    filename = (
        f"{project_name}_Report_{timestamp}.txt"
    )

    return output_directory / filename


# =========================
# REPORT GENERATION
# =========================

def create_report(source_folder, output_file):

    source_folder = Path(source_folder)
    output_file = Path(output_file)

    generated = format_generated_timestamp()

    git_metadata = git_repository_metadata(
        source_folder
    )

    project = project_metadata(
        source_folder
    )

    previous_snapshot = find_previous_snapshot(
        output_file
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as report:

        report.write("# DIRECTORY CONTENT REPORT\n")
        report.write("=" * 100 + "\n\n")

        report.write(
            f"Root folder:\n{source_folder}\n\n"
        )

        report.write(
            f"Generated: {generated}\n"
        )

        report.write(
            f"Branch: {git_metadata['branch']}\n"
        )

        report.write(
            f"Commit: {git_metadata['commit']}\n"
        )

        report.write(
            f"Working tree: {git_metadata['working_tree']}\n"
        )

        report.write(
            f"Python: {platform.python_version()}\n"
        )

        report.write(
            f"{project['name']} version: {project['version']}\n\n"
        )

        report.write(
            "Previous snapshot:\n"
        )

        report.write(
            f"{previous_snapshot}\n\n"
        )

        report.write("=" * 100 + "\n\n")


        for root, dirs, files in os.walk(source_folder):

            # Remove ignored folders
            dirs[:] = [
                d for d in dirs
                if d not in IGNORED_FOLDERS
            ]

            current = Path(root)

            relative = current.relative_to(
                source_folder
            )

            depth = len(relative.parts)

            indent = "    " * depth


            report.write(
                f"{indent}## FOLDER: {current.name}\n"
            )

            report.write(
                f"{indent}   PATH: {relative}\n\n"
            )

            for filename in sorted(files):

                filepath = current / filename

                size = filepath.stat().st_size

                modified = file_timestamp(filepath)

                extension = filepath.suffix.lower()


                report.write(
                    f"{indent}- FILE: {filename}\n"
                )

                report.write(
                    f"{indent}  PATH: {relative}\n"
                )

                report.write(
                    f"{indent}  Size: {human_size(size)}\n"
                )

                report.write(
                    f"{indent}  Modified: {modified}\n"
                )


                if extension in SOURCE_EXTENSIONS and human_size(size) != "0.0 B":

                    report.write("\n")
                    report.write(
                        "#" * 100 + "\n"
                    )

                    report.write(
                        f"SOURCE CODE: {filename}\n"
                    )

                    report.write(
                        "#" * 100 + "\n\n"
                    )


                    report.write(
                        read_text_file(filepath)
                    )


                    report.write(
                        "\n\n"
                    )

                    report.write(
                        "#" * 100 + "\n\n"
                    )


                report.write("\n")


# =========================
# MAIN
# =========================

def main():

    if len(sys.argv) != 3:

        print(
            """
Usage:

    python folder_report.py <source_folder> <output_directory>

Example:

    python folder_report.py "C:\\Projects\\MyApp" "C:\\Reports"
            """
        )

        sys.exit(1)


    source = Path(sys.argv[1])
    output_directory = Path(sys.argv[2])


    if not source.exists():

        print(
            f"Source folder does not exist:\n{source}"
        )

        sys.exit(1)


    if not source.is_dir():

        print(
            f"Source is not a folder:\n{source}"
        )

        sys.exit(1)


    if not output_directory.exists():

        print(
            f"Output directory does not exist:\n{output_directory}"
        )

        sys.exit(1)


    if not output_directory.is_dir():

        print(
            f"Output location is not a directory:\n{output_directory}"
        )

        sys.exit(1)


    output = create_output_file(
        source,
        output_directory,
    )


    create_report(
        source,
        output,
    )


    print(
        "Report created successfully:"
    )

    print(output)


if __name__ == "__main__":
    main()
