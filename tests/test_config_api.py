"""Unit-tests for the ``gitignore_builder.config.api`` module."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from gitignore_builder.config import api
from gitignore_builder.config.api import ALL_RECIPES
from gitignore_builder.config.api import ALL_TEMPLATES
from gitignore_builder.config.api import APP_NAME
from gitignore_builder.config.api import RECIPES_FILENAME
from gitignore_builder.config.api import TEMPLATES_FILENAME
from gitignore_builder.config.api import get_config_dir
from gitignore_builder.config.api import get_recipes_file
from gitignore_builder.config.api import get_templates_file
from gitignore_builder.config.api import init_recipes_file
from gitignore_builder.config.api import init_templates_file
from gitignore_builder.config.api import load_recipes
from gitignore_builder.config.api import load_templates
from gitignore_builder.config.recipes import Recipes
from gitignore_builder.config.templates import Templates


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

    def test_init_templates_file(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            file = temp_dir_path / "templates.json"

            mock_save = MagicMock(spec=Templates.save)
            mock_templates = MagicMock(spec=ALL_TEMPLATES)
            mock_templates.attach_mock(mock_save, "save")

            with patch.object(api, "ALL_TEMPLATES", new=mock_templates):
                init_templates_file(file)

        expected_calls = [call(file)]
        actual_calls = mock_save.mock_calls
        self.assertListEqual(expected_calls, actual_calls)

    def test_init_recipes_file(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            file = temp_dir_path / "recipes.json"

            mock_save = MagicMock(spec=Recipes.save)
            mock_recipes = MagicMock(spec=ALL_RECIPES)
            mock_recipes.attach_mock(mock_save, "save")

            with patch.object(api, "ALL_RECIPES", new=mock_recipes):
                init_recipes_file(file)

        expected_calls = [call(file)]
        actual_calls = mock_save.mock_calls
        self.assertListEqual(expected_calls, actual_calls)

    @patch("gitignore_builder.config.api.get_templates_file", autospec=True)
    def test_load_templates_initializes_the_file_when_missing(
            self, mock_get_templates_file: MagicMock
    ):
        original_templates = ALL_TEMPLATES

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_file = temp_dir_path / "templates.json"
            self.assertFalse(temp_file.exists())

            mock_get_templates_file.return_value = temp_file
            loaded_templates = load_templates()
            self.assertTrue(temp_file.exists())

        self.assertEqual(original_templates, loaded_templates)

    @patch("gitignore_builder.config.api.get_recipes_file", autospec=True)
    def test_load_recipes_initializes_the_file_when_missing(
            self, mock_get_recipes_file: MagicMock,
    ):
        expected_recipes = ALL_RECIPES
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            temp_file = temp_dir_path / "recipes.json"
            self.assertFalse(temp_file.exists())

            mock_get_recipes_file.return_value = temp_file
            actual_recipes = load_recipes()
            self.assertTrue(temp_file.exists())

        self.assertEqual(expected_recipes, actual_recipes)

    @patch("gitignore_builder.config.api.get_templates_file", autospec=True)
    def test_load_templates_reads_the_file_when_existing(
            self, mock_get_templates_file: MagicMock
    ):
        expected_templates = Templates(list(ALL_TEMPLATES.templates[1:]))

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "templates.json"
            self.assertFalse(file.exists())

            expected_templates.save(file)
            self.assertTrue(file.exists())

            mock_get_templates_file.return_value = file
            actual_templates = load_templates()

        self.assertEqual(expected_templates, actual_templates)

    @patch("gitignore_builder.config.api.get_recipes_file", autospec=True)
    def test_load_recipes_reads_the_file_when_existing(
            self, mock_get_recipes_file: MagicMock
    ):
        expected_recipes = Recipes(list(ALL_RECIPES.recipes[1:]))

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "recipes.json"
            self.assertFalse(file.exists())

            expected_recipes.save(file)
            self.assertTrue(file.exists())

            mock_get_recipes_file.return_value = file
            actual_recipes = load_recipes()

        self.assertEqual(expected_recipes, actual_recipes)
