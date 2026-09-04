# Packaged CLI Diagnostics Tool

A small installable Python CLI that inspects a developer machine and produces deterministic human-readable and JSON reports.

## Task 2 coverage
- pyproject.toml package and console entry point
- isolated virtual-environment installation
- Python version, disk space, environment variables, and developer tools
- deterministic JSON and human-readable reports
- useful exit codes
- unit tests for success, missing dependency, and malformed configuration path
- sample reports and usage documentation

## Installation
```bash
python -m venv .venv
```
Windows:
```bash
.venv\Scripts\activate
```
macOS/Linux:
```bash
source .venv/bin/activate
```
Install:
```bash
python -m pip install -e .
python -m pip install pytest
```

## Usage
```bash
cli-diagnostics
cli-diagnostics --json
cli-diagnostics --path .
```

## Testing
```bash
python -m pytest -q
```

## Exit codes
- 0 = all diagnostics passed
- 1 = one or more diagnostics failed
- 2 = invalid command/configuration path

## Security
Only a small allow-list of environment variables is reported; secret/token variables are not collected.
