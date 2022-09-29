"""Unit-tests for the ``gitignore_builder.io_util`` module."""
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import requests

from gitignore_builder import io_util


class FormatDataToYamlTest(TestCase):
    """Unit-tests for the ``io_util.format_data_to_yaml`` method."""

    def test_returns_none_on_error(self):
        class CustomType:
            pass

        bad_obj = CustomType()
        self.assertIsNone(io_util.format_data_to_yaml(bad_obj))  # noqa

    def test_returns_string_if_ok(self):
        data = {"a": [1, 2], "b": [3, 4]}
        expected = dedent("""\
            a:
            - 1
            - 2
            b:
            - 3
            - 4
            """)
        actual = io_util.format_data_to_yaml(data)
        self.assertEqual(expected, actual)


class ParseDataFromYamlTest(TestCase):
    """Unit-tests for the ``io_util.parse_data_from_yaml`` method."""

    def test_returns_none_on_error(self):
        self.assertIsNone(io_util.parse_data_from_yaml(None))  # noqa

    def test_returns_data_if_ok(self):
        text = dedent("""\
            a:
            - 1
            - 2
            b:
            - 3
            - 4
            """)
        expected = {"a": [1, 2], "b": [3, 4]}
        actual = io_util.parse_data_from_yaml(text)
        self.assertEqual(expected, actual)


class ReadFileAsTextTest(TestCase):
    """Unit-tests for the ``io_util.read_file_as_text`` method."""

    def test_returns_none_on_error(self):
        self.assertIsNone(io_util.read_file_as_text(None))  # noqa

    def test_returns_text_if_ok(self):
        expected_text = "1234"

        with TemporaryDirectory() as tmp_dir:
            tmp_dir_path = Path(tmp_dir)

            file = tmp_dir_path / "file.txt"
            self.assertFalse(file.exists())

            file.write_text(expected_text, encoding="utf-8")
            self.assertTrue(file.exists())

            actual_text = io_util.read_file_as_text(file)

        self.assertEqual(expected_text, actual_text)


class ReadFileAsDataTest(TestCase):
    """Unit-tests for the ``io_util.read_file_data`` method."""

    @patch("gitignore_builder.io_util.read_file_as_text", autospec=True)
    def test_returns_none_on_read_text_error(self, mock_read_text: MagicMock):
        mock_read_text.return_value = None
        self.assertIsNone(io_util.read_file_as_data(None))  # noqa

    @patch("gitignore_builder.io_util.parse_data_from_yaml", autospec=True)
    def test_returns_none_on_parse_data_error(self, mock_parse_data: MagicMock):
        mock_parse_data.return_value = None
        text = dedent("""\
                a:
                - 1
                - 2
                b:
                - 3
                - 4
                """)

        with TemporaryDirectory() as tmp_dir:
            tmp_dir_path = Path(tmp_dir)
            file = tmp_dir_path / "file.txt"
            file.write_text(text, encoding="utf-8")

            data = io_util.read_file_as_data(file)
        self.assertIsNone(data)

    def test_returns_data_if_ok(self):
        text = dedent("""\
                a:
                - 1
                - 2
                b:
                - 3
                - 4
                """)

        expected_data = {"a": [1, 2], "b": [3, 4]}

        with TemporaryDirectory() as tmp_dir:
            tmp_dir_path = Path(tmp_dir)
            file = tmp_dir_path / "file.txt"
            file.write_text(text, encoding="utf-8")
            actual_data = io_util.read_file_as_data(file)

        self.assertEqual(expected_data, actual_data)


class ReadUrlAsTextTest(TestCase):
    """Unit-tests for the ``io_util.read_url_as_text`` method."""

    def test_is_able_to_retrieve_contents(self):
        url = "https://github.com/github/gitignore/raw/main/Java.gitignore"
        with requests.get(url, allow_redirects=True, timeout=10) as resp:
            expected = resp.text
        actual = io_util.read_url_as_text(url)
        self.assertEqual(expected, actual)

    def test_returns_none_in_case_of_error(self):
        url = "http://localhost:12345"
        self.assertIsNone(io_util.read_url_as_text(url))
