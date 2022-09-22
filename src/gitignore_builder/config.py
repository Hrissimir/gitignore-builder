"""This module provides the means to access the project configuration."""
from pathlib import Path

import platformdirs

APP_NAME = "gitignore-builder"

RECIPES_FILENAME = "recipes.json"

TEMPLATES_FILENAME = "templates.json"


def get_config_dir() -> Path:
    """Returns path to folder for storing the app configuration."""

    return platformdirs.user_config_path(
        appname=APP_NAME,
    )


def get_recipes_file() -> Path:
    """Returns path to the JSON file that holds all the recipes definitions."""

    return get_config_dir() / RECIPES_FILENAME


def get_templates_file() -> Path:
    """Returns path to the JSON file that holds all the templates definitions.
    """

    return get_config_dir() / TEMPLATES_FILENAME
