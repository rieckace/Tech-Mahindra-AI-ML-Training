"""Pure text analysis functions, independent of the command line."""
import re
from collections import Counter
from pathlib import Path


def analyze_text(text: str, top_n: int = 5) -> dict:
    """Count Unicode alphabetic words; ignore punctuation, digits and case."""
    if not isinstance(text, str):
        raise TypeError('Text must be a string.')
    if type(top_n) is not int or top_n < 1:
        raise ValueError('Top word count must be a positive integer.')
    words = [word.lower() for word in re.findall(r'[^\W\d_]+', text)]
    if not words:
        raise ValueError('File contains no words (empty or punctuation-only text).')
    counts = Counter(words)
    # Alphabetical tie-breaking makes output reproducible.
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return {'word_count': len(words), 'unique_words': len(counts),
            'average_word_length': sum(map(len, words)) / len(words),
            'top_words': ranked[:top_n]}


def analyze_file(path: Path, top_n: int = 5) -> dict:
    """Read a UTF-8 file and analyze its content."""
    return analyze_text(Path(path).read_text(encoding='utf-8-sig'), top_n)
