# Folder Report

A small Python utility that recursively scans a directory and creates a timestamped text report containing:

- the complete folder and file structure;
- the relative path of each folder and file;
- file sizes;
- last-modified timestamps;
- the contents of supported source code and text files;
- Git repository metadata, when available;
- Python and project version information; and
- a reference to the previous project snapshot, when available.

The output filename is generated automatically from the source folder name and the current date and time, 
making Folder Report particularly useful for creating a chronological series of project snapshots.

The resulting report provides a readable snapshot of a project or directory tree in a single `.txt` file.

This can be useful for:

- reviewing the structure of a software project;
- creating project snapshots for documentation;
- sharing a codebase with an AI assistant for analysis;
- preparing code reviews;
- auditing the contents of a directory; and
- creating a human-readable archive of project source files.

## Features

`folder_report.py` recursively walks through a source directory and all of its subdirectories.

For every directory, the report includes:

- the folder name; and
- its path relative to the source directory.

For every file, the report includes:

- the filename;
- its relative directory path;
- its size in human-readable units; and
- its last-modified timestamp.

For supported source and text files, the full contents of the file are also included in the report.

For the report itself, Folder Report also records:

- the date and time the report was generated, including the local UTC offset;
- the current Git branch, when the source folder is a Git repository root;
- the abbreviated Git commit hash;
- whether the Git working tree is clean or dirty;
- the Python version used to generate the report;
- the project name and version from `pyproject.toml`, when available; and
- the filename of the immediately preceding timestamped snapshot, when one can be identified.

Git metadata is only reported when the supplied source folder is itself the root of a Git repository. 
Otherwise, the Git-related fields are reported as `N/a`.

## Supported File Types

File contents are currently included for the following extensions:

| Extension | File type         |
|-----------|-------------------|
| `.py`     | Python            |
| `.ps1`    | PowerShell        |
| `.js`     | JavaScript        |
| `.ts`     | TypeScript        |
| `.sql`    | SQL               |
| `.json`   | JSON              |
| `.yaml`   | YAML              |
| `.yml`    | YAML              |
| `.md`     | Markdown          |
| `.sh`     | Shell script      |
| `.bash`   | Bash              |
| `.toml`   | TOML              |
| `.ini`    | INI configuration |

Other files are still listed in the directory report, but their contents are not included.

Empty supported files are listed but their contents are not emitted.

## Ignored Directories

To avoid including common development artefacts, caches, virtual environments, and IDE configuration, the following directories are ignored by default:

```text
.git
__pycache__
.pytest_cache
.ruff_cache
node_modules
.venv
venv
env
.idea
.vscode
```

These values can be changed by editing the `IGNORED_FOLDERS` set near the top of `folder_report.py`.

## Requirements

## Requirements

Folder Report uses only modules from the Python standard library.

No third-party Python packages are required.

Requirements:

- Python 3.11 or later; and
- Git installed and available on the system `PATH` if Git repository metadata is required.

The script can still generate reports when Git is not installed or when the source folder 
is not a Git repository. In those cases, the Git-specific report fields are shown as `N/a`.

## Installation

Clone the repository:

```bash
git clone https://github.com/ttarpd/Project-Folder-Report.git
```

Then change into the repository directory:

```bash
cd Project-Folder-Report
```

Alternatively, simply download `folder_report.py` and place it wherever you want to run it from.

## Usage

Folder Report requires two command-line arguments:

```text
python folder_report.py <source_folder> <output_directory>
```

Where:

- `<source_folder>` is the directory that you want to scan; and
- `<output_directory>` is the directory in which the generated report will be created.

The output filename is generated automatically using the following format:

```text
<source-folder-name>_Report_YYYYMMDD_HHMM.txt
```

Whitespace in the source folder name is replaced with underscores.

For example, a source folder named:

```text
My Python Project
```

will generate a filename similar to:

```text
My_Python_Project_Report_20260825_1144.txt
```

### Windows example

```powershell
python folder_report.py "C:\Projects\MyApp" "C:\Reports"
```

### Linux/macOS example

```bash
python3 folder_report.py "/home/user/projects/MyApp" "/home/user/reports"
```

Both the source folder and output directory must already exist.

If the source path does not exist, is not a directory, or the output directory does not exist, 
Folder Report exits with an explanatory error message.

## Example

Given a project structure such as:

```text
MyApp/
├── README.md
├── pyproject.toml
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── app.py
│       └── services/
│           └── database.py
└── tests/
    └── test_app.py
```

Running:

```powershell
python folder_report.py "C:\Projects\MyApp" "C:\Reports"
```

will create a timestamped report in `C:\Reports`, for example:

```text
MyApp_Report_20260825_1144.txt
```

The report will broadly resemble:

```text
# DIRECTORY CONTENT REPORT
====================================================================================================

Root folder:
C:\Projects\MyApp

Generated: 2026-08-25 11:44:01 +01:00
Branch: main
Commit: 79c4680
Working tree: clean
Python: 3.12.10
MyApp version: 1.2.0

Previous snapshot:
MyApp_Report_20260824_2056.txt

====================================================================================================

## FOLDER: MyApp
   PATH: .

- FILE: README.md
  PATH: .
  Size: 2.4 KB
  Modified: 2026-08-23 09:15:00

####################################################################################################
SOURCE CODE: README.md
####################################################################################################

# MyApp

...

####################################################################################################


    ## FOLDER: myapp
       PATH: src\myapp

    - FILE: app.py
      PATH: src\myapp
      Size: 4.8 KB
      Modified: 2026-08-23 08:45:12

####################################################################################################
SOURCE CODE: app.py
####################################################################################################

def main():
    print("Hello, world!")

####################################################################################################
```

The indentation provides a visual indication of directory depth, while the `PATH` entry 
makes it easy to identify the exact location of a folder or file when viewing a large report.

## Report Metadata

Each generated report begins with metadata describing the environment and project 
state at the time the snapshot was created.

### Generated

Records the local date and time at which the report was generated, including the UTC offset.

Example:

```text
Generated: 2026-08-25 11:44:01 +01:00
```

### Git metadata

When the source folder is the root of a Git repository, Folder Report records:

```text
Branch: main
Commit: 79c4680
Working tree: clean
```

Working tree will normally be either:

- `clean` — there are no staged, modified, deleted or untracked changes; or
- `dirty` — the working tree contains changes.

If the source folder is not the root of a Git repository, or Git metadata cannot be obtained, 
these fields are reported as:

```text
Branch: N/a
Commit: N/a
Working tree: N/a
```

### Python version

The Python interpreter version used to generate the snapshot is recorded:

```text
Python: 3.12.10
```

### Project version

If the source directory contains a `pyproject.toml` file with project metadata, Folder Report 
attempts to read the project name and version.

For example:

```text
[project]
name = "MyApp"
version = "1.2.0"
```

will produce:

```text
MyApp version: 1.2.0
```

Poetry-style project metadata is also supported.

If no project version can be determined, the report contains:

```text
Project version: N/a
```

## Previous Snapshots

Folder Report attempts to identify the immediately preceding report for the same 
source project in the selected output directory.

Snapshot filenames use the format:

```text
<project>_Report_YYYYMMDD_HHMM.txt
```

For example, if the output directory contains:

```text
MyApp_Report_20260823_0915.txt
MyApp_Report_20260824_2056.txt
MyApp_Report_20260825_1144.txt
```

then the report generated as:

```text
MyApp_Report_20260825_1144.txt
```

will contain:

```text
Previous snapshot:
MyApp_Report_20260824_2056.txt
```

Snapshot ordering is determined from the timestamp embedded in the filename rather 
than the filesystem modification time.

If no earlier matching snapshot can be found, the report contains:

```text
Previous snapshot:
N/a
```

## Output File Naming

The report filename is derived automatically from the name of the source directory.

The format is:

```text
<source-folder-name>_Report_YYYYMMDD_HHMM.txt
```

Whitespace in the source folder name is replaced with underscores.

Examples:

| Source folder           | Example output filename                          |
|-------------------------|--------------------------------------------------|
| `NorthStar`             | `NorthStar_Report_20260825_1144.txt`             |
| `My Python Project`     | `My_Python_Project_Report_20260825_1144.txt`     |
| `Project Folder Report` | `Project_Folder_Report_Report_20260825_1144.txt` |

## Text File Handling

Supported files are read as UTF-8 text.

If a file cannot be decoded as UTF-8, the report contains:

```text
[Binary or non UTF-8 file]
```

If another error occurs while reading a file, the error is recorded in the generated report rather than terminating the entire report-generation process.

## Configuration

The two main configuration options are defined near the top of `folder_report.py`.

### Ignored folders

Add or remove directory names from:

```python
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
```

For example, to exclude a directory named `build`:

```python
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
    "build",
}
```

### Included source file types

To change which files have their contents embedded in the report, edit:

```python
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
```

For example, to include XML files:

```python
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
    ".xml",
}
```

## Using the Report with AI Assistants

One useful application of Folder Report is creating a single-file snapshot of a software project.

Instead of uploading many individual source files, the generated report can provide an AI assistant with:

- the project directory structure;
- source filenames;
- relative paths;
- source code;
- tests;
- Markdown documentation;
- TOML configuration; and
- other supported project files;
- the Git branch and commit represented by the snapshot;
- whether uncommitted changes were present;
- the Python and project versions; and
- the preceding snapshot filename for chronological comparison.

For larger projects, consider the size of the generated report and the context or file-size 
limits of the AI service being used.

Also review the generated file before sharing it externally. Project directories can contain 
confidential information, credentials, API keys, configuration values, personal information, 
or other sensitive data.

## Limitations

Folder Report is intentionally simple.

In particular:

- ignored folders are matched by directory name;
- supported source files are identified by file extension;
- text files are expected to use UTF-8 encoding;
- there is currently no command-line option for changing exclusions or extensions;
- symbolic links and unusual filesystem structures are not handled specially; and
- very large source trees can produce very large output files.
- Git metadata requires the source folder itself to be the Git repository root;
- Git must be installed and available on the system `PATH` for Git metadata to be collected;
- project name and version detection currently relies on `pyproject.toml`;
- previous-snapshot detection relies on the standard generated filename format; and
- report filenames have minute-level timestamp precision, so generating the same project report 
more than once within the same minute will target the same filename.

## Contributing

Contributions, suggestions, and bug reports are welcome.

If you would like to improve the script, fork the repository, make your changes, and submit a pull request.

Possible future enhancements include:

- command-line options for ignored folders;
- command-line options for included file extensions;
- configurable maximum file sizes;
- additional text encodings;
- optional Markdown output;
- optional line numbers for source code;
- include/exclude patterns;
- `.gitignore` integration;
- summary statistics for files and directories;
- Git remote repository information;
- configurable snapshot filename formats;
- second-level timestamp precision or collision-safe filenames;
- comparison/diff information against the previous snapshot; and
- configurable project metadata sources.

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
