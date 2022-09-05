import logging

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class BaseContentBuilder:
    """Helper for building the united the contents of several files into one."""

    def __init__(self):
        self._lines = []

    def __str__(self):
        return "\n".join(self._lines)

    def _is_last_line_empty(self) -> bool:
        """Returns True if the last added line is empty, False otherwise."""

        if not self._lines:
            return False
        return not self._lines[-1]

    def _append_line(self, line: str):
        """Append line to the internal list of resulting lines."""

        line = line.strip()
        if line:

            # always append comments or previously-unseen lines
            if line.startswith("#") or (line not in self._lines):
                self._lines.append(line)

            # never append non-comment line that was already present
            return

        # append empty line only if the previously-appended line was not empty
        if not self._is_last_line_empty():
            self._lines.append(line)

    def append_section(self, title: str, contents: str):
        """Append titled section of .gitignore contents to the final result."""

        # always append the section-border
        border = "# " + f" {title} ".center(117, "=") + "\n"
        self._lines.append(border)

        # the _append_line method decides if each line should be appended
        for line in contents.strip().split("\n"):
            self._append_line(line)

        # always append empty line after section
        self._lines.append("")
