"""Show interpreter and key package versions without extra dependencies."""
import sys
from importlib.metadata import version, PackageNotFoundError

print('Python:', sys.version.split()[0])
print('Executable:', sys.executable)
print('Virtual environment:', 'active' if sys.prefix != sys.base_prefix else 'not active')
print('Runtime dependencies: Python standard library (no external packages)')
for package in ('pytest',):
    try:
        print(f'{package}: {version(package)} (optional; tests use unittest)')
    except PackageNotFoundError:
        print(f'{package}: not installed (not required)')
