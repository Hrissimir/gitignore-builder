"""Unit-tests for the ``gitignore_builder.builder`` module"""
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from ddt import ddt, data

from gitignore_builder.builder import SEPARATOR_FILL_CHAR
from gitignore_builder.builder import SEPARATOR_LINE_LENGTH
from gitignore_builder.builder import append_line
from gitignore_builder.builder import append_section
from gitignore_builder.builder import append_separator_line
from gitignore_builder.builder import append_url
from gitignore_builder.builder import format_separator_line
from gitignore_builder.builder import should_append


@ddt
class ShouldAppendTestCase(TestCase):
    """Unit-tests for the ``builder.should_append`` method."""

    @data(
        ("comment", "comment", True),
        ("comment", "empty", True),
        ("comment", "non-comment", True),
        ("comment", "non-existing", True),
        ("duplicate", "comment", False),
        ("duplicate", "empty", False),
        ("duplicate", "non-comment", False),
        ("duplicate", "non-existing", False),
        ("empty", "comment", True),
        ("empty", "empty", False),
        ("empty", "non-comment", True),
        ("empty", "non-existing", False),
        ("unique", "comment", True),
        ("unique", "empty", True),
        ("unique", "non-comment", True),
        ("unique", "non-existing", True),
    )
    def test_scenario(self, scenario):
        current_line_type, last_line_type, expected = scenario
        if (current_line_type, last_line_type) == ("duplicate", "non-existing"):
            return  # impossible case
        line = self.generate_current_line(current_line_type)
        lines = self.generate_lines_list(last_line_type)
        actual = should_append(lines, line)
        self.assertEqual(expected, actual)

    @classmethod
    def generate_current_line(cls, current_line_type):
        if current_line_type == "comment":
            return "# crash-dumps"
        elif current_line_type == "empty":
            return ""
        elif current_line_type == "duplicate":
            return "*.log"
        elif current_line_type == "unique":
            return "*.tmp"
        else:
            raise ValueError(current_line_type)

    @classmethod
    def generate_lines_list(cls, last_line_type):
        if last_line_type == "non-existing":
            return []
        elif last_line_type == "empty":
            return ["*.log", ""]
        elif last_line_type == "comment":
            return ["*.log", "# temp-files"]
        elif last_line_type == "non-comment":
            return ["*.log"]
        else:
            raise ValueError(last_line_type)


class AppendLineTestCase(TestCase):
    """Unit-tests for the ``builder.append_line`` method."""

    def test_Given_comment_line_When_last_is_comment_Then_appended(self):
        line = "# A"
        lines = ["# B"]
        append_line(lines, line)
        self.assertListEqual(["# B", "# A"], lines)

    def test_Given_comment_line_When_last_is_empty_Then_appended(self):
        line = "# A"
        lines = [""]
        append_line(lines, line)
        self.assertListEqual(["", "# A"], lines)

    def test_Given_comment_line_When_last_is_non_empty_non_comment_Then_appended(self):
        line = "# A"
        lines = ["*.log"]
        append_line(lines, line)
        self.assertListEqual(["*.log", "# A"], lines)

    def test_Given_comment_line_When_list_is_empty_Then_appended(self):
        line = "#"
        lines = []
        append_line(lines, line)
        self.assertEqual(["#"], lines)

    def test_Given_empty_line_When_empty_lines_list_Then_not_appended(self):
        lines = []
        append_line(lines, "")
        self.assertListEqual([], lines)

    def test_Given_empty_line_When_last_is_empty_Then_not_appended(self):
        lines = [""]
        append_line(lines, "")
        self.assertListEqual([""], lines)

    def test_Given_empty_line_When_last_is_non_empty_Then_appended(self):
        lines = ["#"]
        append_line(lines, "")
        self.assertListEqual(["#", ""], lines)

    def test_Given_non_empty_non_comment_line_When_non_present_Then_appended(self):
        line = "*.log"
        lines = []
        append_line(lines, line)
        self.assertIn(line, lines)
        self.assertEqual(1, len(lines))

    def test_Given_non_empty_non_comment_line_When_already_present_Then_not_appended(self):
        line = "*.log"
        lines = [line]
        append_line(lines, line)
        self.assertIn(line, lines)
        self.assertEqual(1, len(lines))


class FormatSeparatorLineTestCase(TestCase):
    """Unit-tests for the ``builder.format_separator_line`` method."""

    def setUp(self):
        self.title = "Title"
        self.separator = format_separator_line(self.title)

    def test_line_contains_title(self):
        self.assertIn(self.title, self.separator)

    def test_line_length(self):
        self.assertEqual(SEPARATOR_LINE_LENGTH, len(self.separator))

    def test_line_fill_char(self):
        self.assertIn(SEPARATOR_FILL_CHAR, self.separator)
        extra_chars = "# " + f" {self.title} "
        expected_count = len(self.separator) - len(extra_chars)
        actual_count = self.separator.count(SEPARATOR_FILL_CHAR)
        self.assertEqual(expected_count, actual_count)


class AppendSeparatorLineTestCase(TestCase):
    """Unit-tests for the ``builder.append_separator_line`` method."""

    @patch("gitignore_builder.builder.append_line", autospec=True)
    @patch("gitignore_builder.builder.format_separator_line", autospec=True)
    def test_append_separator_line_calls_format_and_append(
            self,
            mock_format: MagicMock,
            mock_append: MagicMock
    ):
        mock_title = MagicMock(spec=str)
        mock_separator = MagicMock(spec=str)
        mock_format.return_value = mock_separator

        lines = []
        append_separator_line(lines, mock_title)

        expected_format_calls = [call(mock_title)]
        actual_format_calls = mock_format.mock_calls
        self.assertListEqual(expected_format_calls, actual_format_calls)

        expected_append_calls = [call(lines, mock_separator)]
        actual_append_calls = mock_append.mock_calls
        self.assertListEqual(expected_append_calls, actual_append_calls)


class AppendSectionTestCase(TestCase):
    """Unit-tests for the ``builder.append_section`` method."""

    @patch("gitignore_builder.builder.append_line", autospec=True)
    @patch("gitignore_builder.builder.append_separator_line", autospec=True)
    def test_append_section_appends_separator_with_title_and_all_text_lines(
            self,
            mock_append_separator: MagicMock,
            mock_append_line: MagicMock
    ):
        mock_lines = MagicMock(spec=list)
        mock_text = MagicMock(spec=str)
        mock_text_lines_count = 5
        mock_text_lines = [
            MagicMock(spec=str)
            for _
            in range(mock_text_lines_count)
        ]
        mock_text_stripped_lines = [
            MagicMock(spec=str)
            for _
            in range(mock_text_lines_count)
        ]
        mock_split = MagicMock(spec=str.split)
        mock_split.return_value = mock_text_lines
        mock_text.attach_mock(mock_split, "split")

        for mock_line, mock_stripped_line in zip(mock_text_lines,
                                                 mock_text_stripped_lines):
            mock_line.strip.return_value = mock_stripped_line

        mock_title = MagicMock(spec=str)
        append_section(mock_lines, mock_text, mock_title)

        expected_append_section_calls = [call(mock_lines, mock_title)]
        actual_append_section_calls = mock_append_separator.mock_calls
        self.assertListEqual(
            expected_append_section_calls, actual_append_section_calls
        )

        expected_append_line_calls = [call(mock_lines, line)
                                      for line
                                      in mock_text_stripped_lines]
        actual_append_line_calls = mock_append_line.mock_calls
        self.assertListEqual(
            expected_append_line_calls,
            actual_append_line_calls
        )


class AppendUrlTestCase(TestCase):
    """Unit-tests for the ``builder.append_url`` method."""

    @patch("gitignore_builder.builder.append_section", autospec=True)
    @patch("gitignore_builder.builder.url_to_text", autospec=True)
    def test_append_url_does_not_append_when_no_url_contents(
            self,
            mock_url_to_text: MagicMock,
            mock_append_section: MagicMock
    ):
        mock_url_to_text.return_value = None
        mock_url = MagicMock(spec=str)
        mock_title = MagicMock(spec=str)
        mock_lines = MagicMock(spec=list)
        append_url(mock_lines, mock_url, mock_title)
        expected_calls = []
        actual_calls = mock_append_section.mock_calls
        self.assertListEqual(expected_calls, actual_calls)

    @patch("gitignore_builder.builder.append_section", autospec=True)
    @patch("gitignore_builder.builder.url_to_text", autospec=True)
    def test_append_url_append_when_url_contents(
            self,
            mock_url_to_text: MagicMock,
            mock_append_section: MagicMock
    ):
        mock_url_contents = "# some text"
        mock_url_to_text.return_value = mock_url_contents
        mock_url = MagicMock(spec=str)
        mock_title = MagicMock(spec=str)
        mock_lines = MagicMock(spec=list)
        append_url(mock_lines, mock_url, mock_title)
        expected_calls = [call(mock_lines, mock_url_contents, mock_title)]
        actual_calls = mock_append_section.mock_calls
        self.assertListEqual(expected_calls, actual_calls)
