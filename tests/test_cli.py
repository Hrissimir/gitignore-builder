"""Unit-tests for the main CLI entry point."""
import logging

from abstract_tests import CliCommandTestBase
from gitignore_builder import cli

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class CliTest(CliCommandTestBase):
    """Unit-tests for the ``gitignore_builder.cli`` package."""

    @property
    def command(self):
        return cli.gitignore_builder

    def test_help_option_call_short_name(self):
        self.invoke(["-h"])
        self.assertIn("Usage: gitignore-builder", self.result.output)

    def test_help_option_call_full_name(self):
        self.invoke(["--help"])
        self.assertIn("Usage: gitignore-builder", self.result.output)
