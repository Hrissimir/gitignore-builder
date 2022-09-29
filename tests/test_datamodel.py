"""Unit-tests for the ``gitignore_builder.config.api`` module."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from gitignore_builder.datamodel import APP_NAME
from gitignore_builder.datamodel import RECIPES_FILENAME
from gitignore_builder.datamodel import TEMPLATES_FILENAME
from gitignore_builder.datamodel import _DEFAULT_RECIPES as DEFAULT_RECIPES
from gitignore_builder.datamodel import _DEFAULT_TEMPLATES as DEFAULT_TEMPLATES
from gitignore_builder.datamodel import get_config_dir
from gitignore_builder.datamodel import get_recipe_urls
from gitignore_builder.datamodel import get_recipes
from gitignore_builder.datamodel import get_recipes_file
from gitignore_builder.datamodel import get_templates
from gitignore_builder.datamodel import get_templates_file
from gitignore_builder.datamodel import init_recipes_file
from gitignore_builder.datamodel import init_templates_file
from gitignore_builder.datamodel import load_recipes
from gitignore_builder.datamodel import load_templates


class ConfigApiTest(TestCase):

    @patch("platformdirs.user_config_path", autospec=True)
    def test_get_config_dir(self, mock_get_user_config_path: MagicMock):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            mock_get_user_config_path.return_value = temp_dir_path
            expected_path = temp_dir_path
            actual_path = get_config_dir()

        expected_calls = [call(appname=APP_NAME)]
        actual_calls = mock_get_user_config_path.mock_calls
        self.assertListEqual(expected_calls, actual_calls)

        self.assertIsInstance(actual_path, Path)
        self.assertEqual(expected_path, actual_path)

    @patch("platformdirs.user_config_path", autospec=True)
    def test_get_templates_file(self, mock_get_user_config_path: MagicMock):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            expected = temp_dir_path / TEMPLATES_FILENAME

            mock_get_user_config_path.return_value = temp_dir_path
            actual = get_templates_file()

        self.assertEqual(expected, actual)

    @patch("platformdirs.user_config_path", autospec=True)
    def test_get_recipes_file(self, mock_get_user_config_path: MagicMock):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            expected = temp_dir_path / RECIPES_FILENAME

            mock_get_user_config_path.return_value = temp_dir_path
            actual = get_recipes_file()

        self.assertEqual(expected, actual)

    @patch("gitignore_builder.datamodel.get_templates_file", autospec=True)
    def test_load_templates_initializes_the_file_when_missing(
            self, mock_get_templates_file: MagicMock
    ):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_file = temp_dir_path / "templates.json"
            self.assertFalse(temp_file.exists())

            mock_get_templates_file.return_value = temp_file
            load_templates()
            self.assertTrue(temp_file.exists())

    @patch("gitignore_builder.datamodel.get_recipes_file", autospec=True)
    def test_load_recipes_initializes_the_file_when_missing(
            self, mock_get_recipes_file: MagicMock,
    ):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            temp_file = temp_dir_path / "recipes.json"
            self.assertFalse(temp_file.exists())

            mock_get_recipes_file.return_value = temp_file
            load_recipes()
            self.assertTrue(temp_file.exists())

    @patch("gitignore_builder.datamodel.get_templates_file", autospec=True)
    def test_load_templates_reads_the_file_when_existing(
            self, mock_get_templates_file: MagicMock
    ):
        expected_templates = DEFAULT_TEMPLATES

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "templates.json"
            self.assertFalse(file.exists())

            init_templates_file(file)
            self.assertTrue(file.exists())

            mock_get_templates_file.return_value = file
            load_templates()

            actual_templates = get_templates()

        self.assertEqual(expected_templates, actual_templates)

    @patch("gitignore_builder.datamodel.get_recipes_file", autospec=True)
    def test_load_recipes_reads_the_file_when_existing(
            self, mock_get_recipes_file: MagicMock
    ):
        expected_recipes = DEFAULT_RECIPES

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "recipes.json"
            self.assertFalse(file.exists())

            init_recipes_file(file)
            self.assertTrue(file.exists())

            mock_get_recipes_file.return_value = file
            load_recipes()
            actual_recipes = get_recipes()

        self.assertEqual(expected_recipes, actual_recipes)


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


class GetRecipeUrlsTest(TestCase):

    @patch("gitignore_builder.datamodel.get_templates")
    @patch("gitignore_builder.datamodel.get_recipes")
    def test_returns_urls_if_ok(
            self,
            mock_get_recipes: MagicMock,
            mock_get_templates: MagicMock
    ):
        mock_recipes = {
            "java": ["eclipse", "java-lang"]
        }

        mock_templates = {
            "eclipse": ["eclipse-URL"],
            "java-lang": ["java-lang-URL"]
        }

        mock_get_recipes.return_value = mock_recipes
        mock_get_templates.return_value = mock_templates

        expected = ["eclipse-URL", "java-lang-URL"]
        actual = get_recipe_urls("java")
        self.assertListEqual(expected, actual)


class GetRecipesFileTestCase(TestCase):
    """Unit-tests for the ``datamodel.get_recipes_file`` method."""

    @patch("gitignore_builder.datamodel.get_config_dir", autospec=True)
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
    """Unit-tests for the ``datamodel.get_templates_file`` method."""

    @patch("gitignore_builder.datamodel.get_config_dir", autospec=True)
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
