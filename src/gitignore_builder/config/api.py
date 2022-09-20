"""This module defines the API methods for the gitignore_builder.config package.
"""
import logging
from pathlib import Path

import platformdirs

from gitignore_builder.config.recipes import ALL_RECIPES
from gitignore_builder.config.recipes import Recipes
from gitignore_builder.config.templates import ALL_TEMPLATES
from gitignore_builder.config.templates import Templates

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

APP_NAME = "gitignore-builder"

TEMPLATES_FILENAME = "templates.json"

RECIPES_FILENAME = "recipes.json"


def get_config_dir() -> Path:
    """Returns path to folder for storing user-specific app configuration."""

    return platformdirs.user_config_path(
        appname=APP_NAME,
    )


def get_templates_file() -> Path:
    """Returns path to the JSON file that holds all the templates definitions.
    """

    return get_config_dir() / TEMPLATES_FILENAME


def init_templates_file(file: Path):
    """Initializes sample data contents of `templates.json` file."""

    _log.info("initializing templates file at: '%s'", file)
    ALL_TEMPLATES.save(file)


def load_templates() -> Templates:
    file = get_templates_file()

    if not file.exists():
        init_templates_file(file)

    _log.info("loading templates from file: '%s'", file)
    templates = Templates.load(file)

    _log.info("...done! ( got [ %s ] templates )", len(templates.templates))
    return templates


def get_recipes_file() -> Path:
    """Returns path to the JSON file that holds all the recipes definitions."""

    return get_config_dir() / RECIPES_FILENAME


def init_recipes_file(file: Path):
    """Initializes sample data contents of `recipes.json` file."""

    _log.info("initializing recipes file at: '%s'", file)
    ALL_RECIPES.save(file)


def load_recipes() -> Recipes:
    file = get_recipes_file()

    if not file.exists():
        init_recipes_file(file)

    _log.info("loading recipes from file: '%s'", file)
    recipes = Recipes.load(file)

    _log.info("...done! ( got [ %s ] recipes )", len(recipes.recipes))
    return recipes
