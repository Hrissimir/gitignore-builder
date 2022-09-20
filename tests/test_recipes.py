"""Unit-tests for the ``gitignore_builder.config.recipes`` module."""
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import List
from typing import Optional
from unittest import TestCase

from gitignore_builder.config.recipes import Recipe
from gitignore_builder.config.recipes import Recipes


class RecipeTests(TestCase):
    """Unit-tests for the Recipe class."""

    recipe_name: Optional[str]
    template_names: Optional[List[str]]
    recipe: Optional[Recipe]

    def __init__(self, methodName="runTest"):  # noqa
        super().__init__(methodName)
        self.recipe_name = None
        self.template_names = None
        self.recipe = None

    def setUp(self) -> None:
        self.recipe_name = "python"
        self.template_names = [
            "linux",
            "macos",
            "windows",
            "pycharm",
            "jupyter_notebooks",
            "visual_studio"
        ]
        self.recipe = Recipe(self.recipe_name, self.template_names)

    def tearDown(self) -> None:
        self.recipe = None
        self.template_names = None
        self.recipe_name = None

    def test_instance_creation(self):
        self.assertEqual(self.recipe_name, self.recipe.name)
        self.assertListEqual(self.template_names, self.recipe.templates)

    def test_as_dict(self):
        expected = {
            "name": self.recipe_name,
            "templates": self.template_names
        }
        actual = self.recipe.as_dict()
        self.assertIsInstance(actual, dict)
        self.assertDictEqual(expected, actual)

    def test_from_dict_data_with_bad_type(self):
        data = object()
        with self.assertRaises(TypeError) as ctx:
            Recipe.from_dict(data)  # noqa
        expected_args = ("data", dict, object, data)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_missing_name_key(self):
        data = dict(templates="")
        with self.assertRaises(ValueError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("data", data)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_missing_templates_key(self):
        data = dict(name="")
        with self.assertRaises(ValueError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("data", data)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_bad_name_type(self):
        name = object()
        templates = []
        data = dict(name=name, templates=templates)
        with self.assertRaises(TypeError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("name", str, object, name)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_bad_name_value(self):
        name = "\n\t"
        templates = []
        data = dict(name=name, templates=templates)
        with self.assertRaises(ValueError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("name", name)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_bad_templates_type(self):
        name = "Name"
        templates = object()
        data = dict(name=name, templates=templates)
        with self.assertRaises(TypeError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("templates", list, object, templates)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_empty_templates_list_value(self):
        name = "Name"
        templates = []
        data = dict(name=name, templates=templates)
        with self.assertRaises(ValueError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("templates", templates)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_bad_templates_item_type(self):
        name = "Name"
        template_item = object()
        templates = [template_item]
        data = dict(name=name, templates=templates)
        with self.assertRaises(TypeError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("templates[0]", str, object, template_item)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_bad_templates_item_value(self):
        name = "Name"
        template_item = "\n \t"
        templates = [template_item]
        data = dict(name=name, templates=templates)
        with self.assertRaises(ValueError) as ctx:
            Recipe.from_dict(data)
        expected_args = ("templates[0]", template_item)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_data_with_good_data(self):
        original = self.recipe
        data = original.as_dict()
        parsed = Recipe.from_dict(data)
        self.assertEqual(original, parsed)


class RecipesTests(TestCase):
    """Unit-tests for the Recipes class."""

    android_recipe: Optional[Recipe]
    java_recipe: Optional[Recipe]
    python_recipe: Optional[Recipe]
    recipes: Optional[Recipes]

    def __init__(self, methodName="runTest"):  # noqa
        super().__init__(methodName)
        self.android_recipe = None
        self.java_recipe = None
        self.python_recipe = None
        self.recipes = None

    def setUp(self) -> None:
        self.android_recipe = Recipe(
            name="android",
            templates=[
                "linux",
                "macos",
                "windows",
                "android-studio",
                "eclipse",
                "netbeans",
                "intellij",
                "java"
            ]
        )

        self.java_recipe = Recipe(
            name="java",
            templates=[
                "linux",
                "macos",
                "windows",
                "eclipse",
                "netbeans",
                "intellij",
                "java"
            ]
        )

        self.python_recipe = Recipe(
            name="python",
            templates=[
                "linux",
                "macos",
                "windows",
                "pycharm",
                "jupyter_notebooks",
                "visual_studio",
                "python"
            ]
        )

        self.recipes = Recipes(
            [self.android_recipe, self.java_recipe, self.python_recipe]
        )

    def test_instance_creation(self):
        expected = [self.android_recipe, self.java_recipe, self.python_recipe]
        actual = self.recipes.recipes
        self.assertIsInstance(actual, list)
        self.assertListEqual(expected, actual)

    def test_as_dict(self):
        expected = {
            "recipes": [
                self.android_recipe.as_dict(),
                self.java_recipe.as_dict(),
                self.python_recipe.as_dict()
            ]
        }
        actual = self.recipes.as_dict()
        self.assertIsInstance(actual, dict)
        self.assertDictEqual(expected, actual)

    def test_from_dict_with_data_of_bad_type(self):
        data = object()
        with self.assertRaises(TypeError) as ctx:
            Recipes.from_dict(data)  # noqa
        expected_args = ("data", dict, object, data)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_data_recipes_key_missing(self):
        data = {}
        with self.assertRaises(ValueError) as ctx:
            Recipes.from_dict(data)
        expected_args = ("data", data)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_data_recipes_of_bad_value(self):
        recipes = []
        data = {"recipes": recipes}
        with self.assertRaises(ValueError) as ctx:
            Recipes.from_dict(data)
        expected_args = ("recipes", recipes)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_data_recipes_of_bad_type(self):
        recipes = object()
        data = {"recipes": recipes}
        with self.assertRaises(TypeError) as ctx:
            Recipes.from_dict(data)
        expected_args = ("recipes", list, object, recipes)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_data_recipes_item_of_bad_value(self):
        recipe = {}
        recipes = [recipe, ]
        data = {"recipes": recipes}
        with self.assertRaises(ValueError) as ctx:
            Recipes.from_dict(data)
        expected_args = ("recipes[0]", recipe)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_data_recipes_item_of_bad_type(self):
        recipe = object()
        recipes = [recipe, ]
        data = {"recipes": recipes}
        with self.assertRaises(TypeError) as ctx:
            Recipes.from_dict(data)
        expected_args = ("recipes[0]", dict, object, recipe)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_good_data(self):
        original = self.recipes
        data = original.as_dict()
        parsed = Recipes.from_dict(data)
        self.assertEqual(original, parsed)

    def test_add_operator_when_other_object_has_bad_type(self):
        other = object()
        with self.assertRaises(TypeError) as ctx:
            # pylint: disable=pointless-statement
            self.recipes + other
        expected_args = ("other", Recipes, object, other)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_add_operator_when_other_object_has_good_value(self):
        current = Recipes([self.android_recipe])
        other = Recipes([self.java_recipe, self.python_recipe])
        expected = self.recipes
        actual = current + other
        self.assertEqual(expected, actual)

    def test_as_json(self):
        expected = dedent("""\
            {
                "recipes": [
                    {
                        "name": "android",
                        "templates": [
                            "linux",
                            "macos",
                            "windows",
                            "android-studio",
                            "eclipse",
                            "netbeans",
                            "intellij",
                            "java"
                        ]
                    },
                    {
                        "name": "java",
                        "templates": [
                            "linux",
                            "macos",
                            "windows",
                            "eclipse",
                            "netbeans",
                            "intellij",
                            "java"
                        ]
                    },
                    {
                        "name": "python",
                        "templates": [
                            "linux",
                            "macos",
                            "windows",
                            "pycharm",
                            "jupyter_notebooks",
                            "visual_studio",
                            "python"
                        ]
                    }
                ]
            }""")

        actual = self.recipes.as_json()
        self.assertEqual(expected, actual)

    def test_from_json_good_value(self):
        text = dedent("""\
            {
                "recipes": [
                    {
                        "name": "android",
                        "templates": [
                            "linux",
                            "macos",
                            "windows",
                            "android-studio",
                            "eclipse",
                            "netbeans",
                            "intellij",
                            "java"
                        ]
                    },
                    {
                        "name": "java",
                        "templates": [
                            "linux",
                            "macos",
                            "windows",
                            "eclipse",
                            "netbeans",
                            "intellij",
                            "java"
                        ]
                    },
                    {
                        "name": "python",
                        "templates": [
                            "linux",
                            "macos",
                            "windows",
                            "pycharm",
                            "jupyter_notebooks",
                            "visual_studio",
                            "python"
                        ]
                    }
                ]
            }""")
        expected = self.recipes
        actual = Recipes.from_json(text)
        self.assertEqual(expected, actual)

    def test_from_json_bad_value(self):
        text = "\t \n"
        with self.assertRaises(ValueError) as ctx:
            Recipes.from_json(text)
        expected = ("text", text)
        actual = ctx.exception.args
        self.assertTupleEqual(expected, actual)

    def test_save_with_file_of_bad_type(self):
        file = object()
        with self.assertRaises(TypeError) as ctx:
            self.recipes.save(file)  # noqa
        expected_args = ("file", Path, object, file)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_save_with_file_pointing_to_existing_dir(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            with self.assertRaises(IsADirectoryError) as ctx:
                self.recipes.save(temp_dir_path)

        expected_args = ("file", temp_dir_path)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_save_with_file_with_existing_parent_dir(self):
        recipes = self.recipes
        expected_contents = recipes.as_json()

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "recipes.json"
            self.assertTrue(file.parent.exists())
            self.assertFalse(file.exists())

            recipes.save(file)
            self.assertTrue(file.exists())

            actual_contents = file.read_text(
                encoding="ascii", errors="surrogateescape"
            )

        self.assertEqual(expected_contents, actual_contents)

    def test_save_with_file_with_nonexistent_parent_dir(self):
        recipes = self.recipes
        expected_contents = recipes.as_json()

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "my/recipes.json"
            self.assertFalse(file.parent.exists())
            self.assertFalse(file.exists())

            recipes.save(file)
            self.assertTrue(file.parent.exists())
            self.assertTrue(file.exists())

            actual_contents = file.read_text(
                encoding="ascii", errors="surrogateescape"
            )

        self.assertEqual(expected_contents, actual_contents)

    def test_load_with_file_of_bad_type(self):
        file = object()
        with self.assertRaises(TypeError) as ctx:
            Recipes.load(file)  # noqa

        expected_args = ("file", Path, object, file)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_load_with_file_pointing_nonexistent_location(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "recipes.json"
            self.assertFalse(file.exists())

            with self.assertRaises(FileNotFoundError) as ctx:
                Recipes.load(file)  # noqa

        expected_args = (file,)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_load_with_file_pointing_existing_folder_location(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path
            self.assertTrue(file.exists())
            self.assertTrue(file.is_dir())

            with self.assertRaises(IsADirectoryError) as ctx:
                Recipes.load(file)  # noqa

        expected_args = (file,)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_load_with_file_containing_good_data(self):
        original_recipes = self.recipes

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "recipes.json"
            self.assertFalse(file.exists())

            original_recipes.save(file)
            self.assertTrue(file.exists())

            parsed_recipes = Recipes.load(file)

        self.assertEqual(original_recipes, parsed_recipes)
