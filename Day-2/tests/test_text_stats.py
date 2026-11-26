import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from main import main
from src.text_stats import analyze_text, analyze_file


class TextStatsTests(unittest.TestCase):
    def test_normal(self):
        result = analyze_text('Python makes coding simple. Python makes learning fun.')
        self.assertEqual(result['word_count'], 8)
        self.assertEqual(result['unique_words'], 6)
        self.assertAlmostEqual(result['average_word_length'], 5.625)
        self.assertEqual(result['top_words'][:2], [('makes', 2), ('python', 2)])

    def test_case_and_punctuation(self):
        self.assertEqual(analyze_text('Hello, HELLO! 123')['top_words'], [('hello', 2)])

    def test_empty(self):
        for value in ('', '   ', '123 !!!'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze_text(value)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            analyze_text(None)

    def test_invalid_top(self):
        for value in (0, -1, True, '2'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze_text('hello', value)

    def test_top_and_ties(self):
        self.assertEqual(analyze_text('zebra apple banana', 2)['top_words'], [('apple', 1), ('banana', 1)])

    def test_unicode_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'text.txt'
            path.write_text('café café', encoding='utf-8')
            self.assertEqual(analyze_file(path)['top_words'], [('café', 2)])

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(main([str(Path(folder) / 'missing.txt')]), 1)
            self.assertIn('File not found', err.getvalue())

    def test_empty_file_cli(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stderr(io.StringIO()) as err:
            path = Path(folder) / 'empty.txt'
            path.touch()
            self.assertEqual(main([str(path)]), 1)
            self.assertIn('no words', err.getvalue())

    def test_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stderr(io.StringIO()) as err:
            path = Path(folder) / 'bad.txt'
            path.write_bytes(b'\xff\xfe')
            self.assertEqual(main([str(path)]), 1)
            self.assertIn('UTF-8', err.getvalue())

    def test_invalid_cli_top(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
            main(['sample.txt', '--top', '0'])
        self.assertEqual(exc.exception.code, 2)

    def test_json_cli(self):
        import json
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()) as out:
            path = Path(folder) / 'text.txt'
            path.write_text('one two one', encoding='utf-8')
            self.assertEqual(main([str(path), '--json']), 0)
            self.assertEqual(json.loads(out.getvalue())['word_count'], 3)


if __name__ == '__main__':
    unittest.main()
