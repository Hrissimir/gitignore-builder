"""Unit-tests for the ``gitignore_builder.config`` module."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from gitignore_builder.config import APP_NAME
from gitignore_builder.config import RECIPES_FILENAME
from gitignore_builder.config import TEMPLATES_FILENAME
from gitignore_builder.config import get_config_dir
from gitignore_builder.config import get_recipes_file
from gitignore_builder.config import get_templates_file


class GetConfigDirTestCase(TestCase):
    """Unit-tests for the ``config.get_config_dir`` method."""

    @patch("platformdirs.user_config_path", autospec=True)
    def test_returns_user_config_path(
            self,
            mock_get_platform_dir: MagicMock
    ):
        mock_dir = MagicMock(spec=Path)
        mock_get_platform_dir.return_value = mock_dir
        expected = mock_dir
        actual = get_config_dir()
        self.assertEqual(expected, actual)

        expected_calls = [call(appname=APP_NAME)]
        actual_calls = mock_get_platform_dir.mock_calls
        self.assertListEqual(expected_calls, actual_calls)


class GetRecipesFileTestCase(TestCase):
    """Unit-tests for the ``config.get_recipes_file`` method."""

    @patch("gitignore_builder.config.get_config_dir", autospec=True)
    def test_returns_file_in_app_config_dir(
            self,
            mock_get_config_dir: MagicMock
    ):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            mock_get_config_dir.return_value = temp_dir_path

            expected = temp_dir_path / RECIPES_FILENAME
            actual = get_recipes_file()
        self.assertEqual(expected, actual)


class GetTemplatesFileTestCase(TestCase):
    """Unit-tests for the ``config.get_templates_file`` method."""

    @patch("gitignore_builder.config.get_config_dir", autospec=True)
    def test_returns_file_in_app_config_dir(
            self,
            mock_get_config_dir: MagicMock
    ):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            mock_get_config_dir.return_value = temp_dir_path

            expected = temp_dir_path / TEMPLATES_FILENAME
            actual = get_templates_file()
        self.assertEqual(expected, actual)
