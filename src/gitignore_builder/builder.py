"""This module defines the logic for building the contents of a .gitignore file.
"""
from typing import List

import click

from gitignore_builder.io_util import read_url_as_text

SEPARATOR_LINE_LENGTH = 120
SEPARATOR_FILL_CHAR = "="


# pylint: disable=trailing-whitespace
def should_append(lines: List[str], line: str) -> bool:
    """Checks if the line should be appended according to rules.

    * If the line is empty - append it only if the last line is not empty.
    * If the line is non-empty/comment - append it only if not already present.
    * If the line is comment line - append it.

    Args:
        lines: Target list.
        line: Current line.

    Returns:
        True if the line should be appended, False otherwise."""

    if not lines:
        return bool(line)

    if line:
        if line.startswith("#") or line not in lines:
            return True
        return False

    if lines and lines[-1]:
        return True

    return False


def append_line(lines: List[str], line: str):
    """Processes and appends the line to the current list of lines.

    An "empty-comments-section" can appear while accumulating the contents
    of several .gitignore files into one. It happens when the non-commented
    lines of the currently appended file were already present in the list.
    This results in several comment-sections with only empty-lines between.
    Extra care is taken to avoid such situations while appending each line.
    """

    if should_append(lines, line):
        lines.append(line)


def format_separator_line(title: str) -> str:
    """Returns a commented, fixed-length line with the title centered."""

    return "# " + f" {title} ".center((SEPARATOR_LINE_LENGTH - 2), SEPARATOR_FILL_CHAR)


def append_separator_line(lines: List[str], title: str):
    """Creates and appends separator line to the list of lines."""

    line = format_separator_line(title)
    append_line(lines, line)


def append_section(lines: List[str], section_text: str, section_title=""):
    """Appends .gitignore text contents as titled section to the lines list.

    Args:
        lines: Target list of lines.
        section_text: Contents of a .gitignore file.
        section_title: Title used for generation of the separator-row.
    """

    append_separator_line(lines, section_title)
    for line in section_text.split("\n"):
        append_line(lines, line.strip())


def append_url(lines: List[str], url: str, section_title=""):
    """Retrieves text from the URL and appends it as section to the list."""

    section_text = read_url_as_text(url)
    if section_text:
        append_section(lines, section_text, section_title)


def build_gitignore_contents(urls: List[str]) -> str:
    """Build the contents of a single .gitignore file from several URLs."""

    lines = []

    with click.progressbar(urls) as urls_progress:
        for url in urls_progress:
            title = f"source: {url}"
            append_url(lines, url, title)

    return "\n".join(lines)
