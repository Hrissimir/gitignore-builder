"""Unit-tests for the ``gitignore_builder.io_util`` module."""
from unittest import TestCase

import requests

from gitignore_builder import io_util


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
