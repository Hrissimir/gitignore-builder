from unittest import TestCase

import requests

from gitignore_builder.util import url_to_text


class UtilTest(TestCase):

    def test_url_to_text_is_able_to_retrieve_contents(self):
        url = "https://github.com/github/gitignore/raw/main/Java.gitignore"
        with requests.get(url, allow_redirects=True) as resp:
            expected = resp.text
        actual = url_to_text(url)
        self.assertEqual(expected, actual)

    def test_url_to_text_returns_none_in_case_of_error(self):
        url = "http://localhost:12345"
        self.assertIsNone(url_to_text(url))
