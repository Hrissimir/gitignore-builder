"""Unit-tests for the ``gitignore_builder.cli`` package."""
import logging
from unittest.mock import MagicMock
from unittest.mock import patch

from .abstract_tests import CliCommandTestBase
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

    @patch("gitignore_builder.datamodel.get_templates_file")
    @patch("gitignore_builder.datamodel.get_recipes_file")
    def test_config_prints_paths(
            self,
            mock_get_recipes_file: MagicMock,
            mock_get_templates_file: MagicMock
    ):
        mock_recipes_file = self.temp_dir / "recipes.yaml"
        mock_get_recipes_file.return_value = mock_recipes_file

        mock_templates_file = self.temp_dir / "templates.yaml"
        mock_get_templates_file.return_value = mock_templates_file

        self.invoke(["--config"])
        self.assertIn(str(mock_recipes_file), self.result.output)
        self.assertIn(str(mock_templates_file), self.result.output)

    def test_generate_contents_and_write_them_to_disk(self):
        file = self.temp_dir / ".gitignore"
        self.assertFalse(file.exists())

        self.invoke(["python", str(file)])
        self.assertTrue(file.exists())

        resulting_text = file.read_text(encoding="utf-8")
        self.assertGreaterEqual(len(resulting_text), 0)
