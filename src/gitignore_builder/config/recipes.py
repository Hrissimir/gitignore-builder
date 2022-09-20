"""This module defines the logic for dealing with different recipes.

A recipe is represented by a recipe-name and list of template-names.
"""
import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union


class Recipe(NamedTuple):
    """Represents a single, named recipe containing list of template-names."""

    name: str
    templates: List[str]

    def as_dict(self) -> Dict[str, Union[str, List[str]]]:
        """Returns dict with the current recipe data."""

        return {
            "name": self.name,
            "templates": self.templates
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Recipe":
        """Creates Recipe instance from dict data."""

        if not isinstance(data, dict):
            raise TypeError("data", dict, type(data), data)

        try:
            data_name, data_templates = data["name"], data["templates"]
        except KeyError as e:
            raise ValueError("data", data) from e

        if not isinstance(data_name, str):
            raise TypeError("name", str, type(data_name), data_name)

        result_name = data_name.strip()
        if not result_name:
            raise ValueError("name", data_name)

        if not isinstance(data_templates, list):
            raise TypeError(
                "templates", list, type(data_templates), data_templates
            )

        result_templates = []
        for idx, data_template in enumerate(data_templates):

            if not isinstance(data_template, str):
                raise TypeError(
                    f"templates[{idx}]", str, type(data_template), data_template
                )

            result_template = data_template.strip()
            if not result_template:
                raise ValueError(f"templates[{idx}]", data_template)

            result_templates.append(result_template)

        if not result_templates:
            raise ValueError("templates", data_templates)

        return cls(name=result_name, templates=result_templates)


class Recipes(NamedTuple):
    """Represents a list of recipes."""

    recipes: List[Recipe]

    def __add__(self, other):
        if isinstance(other, Recipes):
            return Recipes(self.recipes + other.recipes)
        raise TypeError("other", Recipes, type(other), other)

    def as_dict(self) -> Dict[str, List[dict]]:
        """Returns dict with the current Recipes instance data."""

        return {
            "recipes": [
                recipe.as_dict()
                for recipe
                in self.recipes
            ]
        }

    def as_json(self) -> str:
        """Returns string with the JSON representation of the current object."""

        data = self.as_dict()
        return json.dumps(
            data,
            ensure_ascii=True,
            indent=4,
            sort_keys=False
        )

    def save(self, file: Path):
        """Converts the current object data to JSON and writes it to the file."""

        if not isinstance(file, Path):
            raise TypeError("file", Path, type(file), file)

        if file.exists() and (not file.is_file()):
            raise IsADirectoryError("file", file)

        folder = file.parent
        folder.mkdir(parents=True, exist_ok=True)

        text = self.as_json()
        file.write_text(text, encoding="ascii", errors="surrogateescape")

    @classmethod
    def from_dict(cls, data: dict) -> "Recipes":
        """Creates Recipes object by parsing data from a dict."""

        if not isinstance(data, dict):
            raise TypeError("data", dict, type(data), data)

        try:
            data_recipes = data["recipes"]
        except KeyError as e:
            raise ValueError("data", data) from e

        if not isinstance(data_recipes, list):
            raise TypeError("recipes", list, type(data_recipes), data_recipes)

        result_recipes = []

        for idx, data_recipe in enumerate(data_recipes):

            if not isinstance(data_recipe, dict):
                raise TypeError(
                    f"recipes[{idx}]", dict, type(data_recipe), data_recipe
                )

            try:
                result_recipe = Recipe.from_dict(data_recipe)
            except (TypeError, ValueError) as e:
                raise ValueError(f"recipes[{idx}]", data_recipe) from e

            result_recipes.append(result_recipe)

        if not result_recipes:
            raise ValueError("recipes", data_recipes)

        return cls(recipes=result_recipes)

    @classmethod
    def from_json(cls, text: str) -> "Recipes":
        """Creates and returns Recipes instance by parsing JSON data string."""

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError("text", text) from e

        return cls.from_dict(data)

    @classmethod
    def load(cls, file: Path) -> "Recipes":
        """Loads Recipes data from JSON file."""

        if not isinstance(file, Path):
            raise TypeError("file", Path, type(file), file)

        if not file.exists():
            raise FileNotFoundError(file)

        if file.exists() and file.is_dir():
            raise IsADirectoryError(file)

        text = file.read_text(encoding="ascii", errors="surrogateescape")
        return cls.from_json(text)


ANDROID_RECIPE = Recipe(
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

JAVA_RECIPE = Recipe(
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

PYTHON_RECIPE = Recipe(
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

ALL_RECIPES = Recipes(
    [
        ANDROID_RECIPE,
        JAVA_RECIPE,
        PYTHON_RECIPE
    ]
)
