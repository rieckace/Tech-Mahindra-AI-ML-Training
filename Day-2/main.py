"""Command-line entry point for the text statistics tool."""
import argparse
import json
import sys
from pathlib import Path
from src.text_stats import analyze_file


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('must be a positive integer') from None
    if number < 1:
        raise argparse.ArgumentTypeError('must be a positive integer')
    return number


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Analyze word statistics in a UTF-8 text file.')
    parser.add_argument('file', type=Path, help='Path to the text file')
    parser.add_argument('--top', type=positive_int, default=5, help='Number of top words (default: 5)')
    parser.add_argument('--json', action='store_true', help='Print machine-readable JSON')
    args = parser.parse_args(argv)
    try:
        stats = analyze_file(args.file, args.top)
    except FileNotFoundError:
        print(f'Error: File not found: {args.file}', file=sys.stderr)
        return 1
    except UnicodeError:
        print('Error: File must contain valid UTF-8 text.', file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print('TEXT STATISTICS')
        print('---------------')
        print(f"Word count: {stats['word_count']}")
        print(f"Unique words: {stats['unique_words']}")
        print(f"Average word length: {stats['average_word_length']:.2f}")
        print('Top words:')
        for word, count in stats['top_words']:
            print(f'  {word}: {count}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
