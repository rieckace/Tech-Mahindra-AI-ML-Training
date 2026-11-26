# Day 2 — Text Statistics Tool

A small, reproducible Python command-line application that counts words, ranks frequent words and calculates average word length. No external dependencies are needed.

## Setup on a clean computer
Install Python 3.10 or newer (tested with 3.13.5). Extract the project and open its root folder in VS Code or a terminal.

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python env_check.py
```
If PowerShell blocks activation, use Command Prompt with `.venv\Scripts\activate.bat`, or invoke `.venv\Scripts\python.exe` directly instead of `python`.

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python env_check.py
```
The requirements file is intentionally dependency-free: all runtime and test modules belong to the standard library. Their versions are determined by the Python interpreter. For matching the tested interpreter exactly, install Python 3.13.5.

## Run
```bash
python main.py samples/sample.txt --top 3
```
Actual output:
```text
TEXT STATISTICS
---------------
Word count: 8
Unique words: 6
Average word length: 5.62
Top words:
  makes: 2
  python: 2
  coding: 1
```
Other examples:
```bash
python main.py samples/sample.txt
python main.py samples/sample.txt --top 10 --json
python main.py --help
python main.py missing.txt
```
To save JSON: `python main.py samples/sample.txt --json > result.json`.
Missing files and files with no words produce clear messages on stderr and exit code 1. Invalid arguments exit with code 2. Success returns 0.

## Run tests
```bash
python -m unittest discover -s tests -v
```
Actual result on Python 3.13.5: 12 tests ran, OK. Tests cover normal input, case and punctuation, empty and invalid input, top limits and ties, Unicode, missing files, empty files, invalid encoding, CLI validation and JSON output. No test framework installation is needed.

## Design and limitations
`main.py` handles arguments, output and errors; `src/text_stats.py` contains reusable analysis logic. A Counter calculates frequencies; sorting by descending count and alphabetical word gives deterministic ties. Words are alphabetic runs as matched by Python's Unicode regex; digits and punctuation are excluded, contractions and hyphenated words split, and combining marks are not normalized. Average length uses all word occurrences, not just unique words. The file is read into memory, suitable for small text files. This is not a language-aware tokenizer or a PDF/Word reader.

## Files
- `main.py`: CLI entry point
- `src/text_stats.py`: core analysis
- `env_check.py`: interpreter and optional test-package version check
- `requirements.txt`: dependency manifest (zero external packages)
- `tests/`: assert-based unittest suite
- `samples/sample.txt`: reproducible sample
- `RESPONSIBLE_USE.md`: privacy and verification guidance
- `.gitignore`: excludes local environments, caches and secrets
