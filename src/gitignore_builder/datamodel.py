"""This module defines the API methods for the gitignore_builder.config package.
"""
import logging
from copy import deepcopy
from pathlib import Path
from typing import List
from typing import Optional

import platformdirs

from gitignore_builder import io_util

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

_DEFAULT_TEMPLATES = {
    "linux": [
        "https://github.com/github/gitignore/raw/main/Global/Linux.gitignore",
        "https://www.toptal.com/developers/gitignore/api/linux",
    ],
    "macos": [
        "https://github.com/github/gitignore/raw/main/Global/macOS.gitignore",
        "https://www.toptal.com/developers/gitignore/api/macos",
    ],
    "windows": [
        "https://github.com/github/gitignore/raw/main/Global/Windows.gitignore",
        "https://www.toptal.com/developers/gitignore/api/windows",
    ],
    "android-studio": [
        "https://github.com/github/gitignore/raw/main/Android.gitignore",
        "https://www.toptal.com/developers/gitignore/api/android,androidstudio",
    ],
    "eclipse": [
        "https://github.com/github/gitignore/raw/main/Global/Eclipse.gitignore",
        "https://www.toptal.com/developers/gitignore/api/eclipse",
    ],
    "netbeans": [
        "https://github.com/github/gitignore/raw/main/Global/NetBeans.gitignore",
        "https://www.toptal.com/developers/gitignore/api/netbeans",
    ],
    "intellij": [
        "https://github.com/github/gitignore/raw/main/Global/JetBrains.gitignore",
        "https://www.toptal.com/developers/gitignore/api/intellij,intellij+all,intellij+iml",
    ],
    "pycharm": [
        "https://github.com/github/gitignore/raw/main/Global/JetBrains.gitignore",
        "https://www.toptal.com/developers/gitignore/api/pycharm,pycharm+all,pycharm+iml,pydev",
    ],
    "jupyter-notebooks": [
        "https://github.com/github/gitignore/raw/main/community/Python/JupyterNotebooks.gitignore",
        "https://www.toptal.com/developers/gitignore/api/jupyternotebooks",
    ],
    "visual-studio": [
        "https://github.com/github/gitignore/raw/main/VisualStudio.gitignore",
        "https://www.toptal.com/developers/gitignore/api/visualstudio,visualstudiocode",
    ],
    "java-lang": [
        "https://github.com/github/gitignore/raw/main/Java.gitignore",
        "https://github.com/github/gitignore/raw/main/JBoss.gitignore",
        "https://github.com/github/gitignore/raw/main/Maven.gitignore",
        "https://github.com/github/gitignore/raw/main/Gradle.gitignore",
        "https://github.com/github/gitignore/raw/main/Global/JDeveloper.gitignore",
        "https://github.com/github/gitignore/raw/main/Global/JEnv.gitignore",
        "https://github.com/github/gitignore/raw/main/community/Java/JBoss4.gitignore",
        "https://github.com/github/gitignore/raw/main/community/Java/JBoss6.gitignore",
        "https://www.toptal.com/developers/gitignore/api/java,gradle,maven",
    ],
    "python-lang": [
        "https://github.com/github/gitignore/raw/main/Python.gitignore",
        "https://github.com/github/gitignore/raw/main/community/Python/Nikola.gitignore",
        "https://github.com/pyscaffold/pyscaffold/raw/master/src/pyscaffold/templates/gitignore.template",
        "https://www.toptal.com/developers/gitignore/api/python,pythonvanilla,django,flask",
    ]
}

_DEFAULT_RECIPES = {
    "android": [
        "linux",
        "macos",
        "windows",
        "android-studio",
        "eclipse",
        "netbeans",
        "intellij",
        "java-lang"
    ],
    "java": [
        "linux",
        "macos",
        "windows",
        "eclipse",
        "netbeans",
        "intellij",
        "java-lang"
    ],
    "python": [
        "linux",
        "macos",
        "windows",
        "pycharm",
        "jupyter-notebooks",
        "visual-studio",
        "python-lang"
    ]
}

_recipes: Optional[dict] = None

_templates: Optional[dict] = None

APP_NAME = "gitignore-builder"

RECIPES_FILENAME = "recipes.yaml"

TEMPLATES_FILENAME = "templates.yaml"


def get_config_dir() -> Path:
    """Returns path to folder for storing the app configuration."""

    return platformdirs.user_config_path(
        appname=APP_NAME,
    )


def set_recipes(recipes: dict):
    """Set the recipes data to be used by the module."""

    global _recipes
    _recipes = recipes


def set_templates(templates: dict):
    """Set the templates data to be used by the module."""

    global _templates
    _templates = templates


def get_recipes_file() -> Path:
    """Returns path to the recipes data file."""

    return get_config_dir() / RECIPES_FILENAME


def init_recipes_file(file: Path):
    """Initializes recipes data file with sample contents."""

    _log.warning("Initializing recipes data-file at: '%s'", file)
    io_util.write_data_to_file(_DEFAULT_RECIPES, file)
    _log.warning("...DONE!")


def load_recipes():
    """Loads recipes data from the app config file"""

    file = get_recipes_file()
    if not file.exists():
        init_recipes_file(file)

    try:
        _log.info("Loading recipes data from file: '%s'", file)
        recipes = io_util.read_file_as_data(file)
    except Exception as e:
        _log.warning("Error while loading recipes from file: '%s'", e)
        _log.warning("Using bundled recipes data as fallback value!")
        recipes = _DEFAULT_RECIPES

    set_recipes(recipes)
    _log.info("...DONE!")


def get_templates_file() -> Path:
    """Returns path to the templates data file."""

    return get_config_dir() / TEMPLATES_FILENAME


def init_templates_file(file: Path):
    """Initializes templates data file with sample contents."""

    _log.warning("Initializing templates data-file at: '%s'", file)
    io_util.write_data_to_file(_DEFAULT_TEMPLATES, file)
    _log.warning("...DONE!")


def load_templates():
    """Loads templates data from the app config file"""

    file = get_templates_file()
    if not file.exists():
        init_templates_file(file)

    try:
        _log.info("Loading templates data from file: '%s'", file)
        templates = io_util.read_file_as_data(file)
    except Exception as e:
        _log.warning("Error while loading templates from file: '%s'", e)
        _log.warning("Using bundled templates data as fallback value!")
        templates = _DEFAULT_TEMPLATES

    set_templates(templates)
    _log.info("...DONE!")


def init():
    """Call this to initialize the module before interaction."""

    load_recipes()
    load_templates()


def get_recipes() -> Optional[dict]:
    """Returns the currently available recipes."""

    global _recipes
    return _recipes if _recipes else deepcopy(_DEFAULT_RECIPES)


def get_recipe_names() -> List[str]:
    """Returns list with the names of currently available recipes."""

    recipes = get_recipes()
    if recipes:
        return list(recipes.keys())
    return []


def get_recipe_templates(name: str) -> Optional[List[str]]:
    """Call this to get list of template-names for a given recipe."""

    recipes = get_recipes()
    if not recipes:
        _log.warning("Got NO recipes data!")
        return None

    try:
        return recipes[name]
    except KeyError:
        _log.warning(
            "Bad recipe name: '%s'! Valid recipe names: '%s'",
            name,
            get_recipe_names()
        )
    except Exception as e:
        _log.error("Error while getting recipe templates! Details: %s", e)

    return None


def get_templates() -> Optional[dict]:
    """Returns the currently available templates."""

    global _templates
    return _templates if _templates else deepcopy(_DEFAULT_TEMPLATES)


def get_template_names() -> List[str]:
    """Returns list with the names of currently available templates."""

    templates = get_templates()
    if templates:
        return list(templates.keys())
    return []


def get_template_urls(name: str) -> Optional[List[str]]:
    """Call this to list of URLs defined by a given template."""

    templates = get_templates()
    if not templates:
        _log.warning("Got NO templates data!")
        return None

    try:
        return templates[name]
    except KeyError:
        _log.warning(
            "Bad template name: '%s'! Valid template names: '%s'",
            name,
            get_template_names()
        )
    except Exception as e:
        _log.error("Error while getting template URLs! Details: %s", e)

    return None


def get_recipe_urls(recipe_name: str) -> List[str]:
    """Call this to construct list of all template-urls for a given recipe."""

    recipe_templates = get_recipe_templates(recipe_name)
    if not recipe_templates:
        _log.warning("Got NO recipe template names!")
        return []

    result = []

    for template_name in recipe_templates:
        template_urls = get_template_urls(template_name)
        if not template_urls:
            continue
        result.extend(template_urls)

    return result
