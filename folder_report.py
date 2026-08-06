#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime


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


# =========================
# REPORT GENERATION
# =========================

def create_report(source_folder, output_file):

    source_folder = Path(source_folder)

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
            f"Created:\n{datetime.now()}\n\n"
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
                f"{indent}## FOLDER: {current.name}\n\n"
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

    python folder_report.py <source_folder> <output_file>

Example:

    python folder_report.py "C:\\Projects\\MyApp" "C:\\Reports\\MyApp_Report.txt"
            """
        )

        sys.exit(1)


    source = sys.argv[1]
    output = sys.argv[2]


    if not Path(source).exists():

        print(
            f"Folder does not exist:\n{source}"
        )

        sys.exit(1)


    create_report(
        source,
        output
    )


    print(
        "Report created successfully:"
    )

    print(output)


if __name__ == "__main__":
    main()
