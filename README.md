# Folder Report

A small Python utility that recursively scans a directory and creates a single text file containing:

- the complete folder and file structure;
- the relative path of each folder and file;
- file sizes;
- last-modified timestamps; and
- the contents of supported source code and text files.

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

The script uses only modules from the Python standard library.

No third-party packages are required.

You need a working Python 3 installation.

## Installation

Clone the repository:

```bash
git clone https://github.com/ttarpd/Project-Folder-Report
```

Then change into the repository directory:

```bash
cd <repository-directory>
```

Alternatively, simply download `folder_report.py` and place it wherever you want to run it from.

## Usage

The script requires two command-line arguments:

```text
python folder_report.py <source_folder> <output_file>
```

Where:

- `<source_folder>` is the directory that you want to scan.
- `<output_file>` is the text file that will contain the generated report.

### Windows example

```powershell
python folder_report.py "C:\Projects\MyApp" "C:\Reports\MyApp_Report.txt"
```

### Linux/macOS example

```bash
python3 folder_report.py "/home/user/projects/MyApp" "/home/user/reports/MyApp_Report.txt"
```

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
python folder_report.py "C:\Projects\MyApp" "C:\Reports\MyApp_Report.txt"
```

will produce a report broadly resembling:

```text
# DIRECTORY CONTENT REPORT
====================================================================================================

Root folder:
C:\Projects\MyApp

Created:
2026-08-23 09:30:00

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

The indentation provides a visual indication of directory depth, while the `PATH` entry makes it easy to identify the exact location of a folder or file when viewing a large report.

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
- other supported project files.

For larger projects, consider the size of the generated report and the context or file-size limits of the AI service being used.

Also review the generated file before sharing it externally. Project directories can contain confidential information, credentials, API keys, configuration values, personal information, or other sensitive data.

## Limitations

Folder Report is intentionally simple.

In particular:

- ignored folders are matched by directory name;
- supported source files are identified by file extension;
- text files are expected to use UTF-8 encoding;
- there is currently no command-line option for changing exclusions or extensions;
- symbolic links and unusual filesystem structures are not handled specially; and
- very large source trees can produce very large output files.

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
- `.gitignore` integration; and
- summary statistics for files and directories.

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
