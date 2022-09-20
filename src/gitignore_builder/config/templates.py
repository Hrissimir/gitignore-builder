"""This module defines the logic for dealing with different templates sources.

The project ships with 3 pre-defined templates groups: OS, IDE and LANG related.

Upon first usage, the contents of all bundled templates are collectively written
to a `templates.json` file inside the app configuration dir (per-user specific).

From this point on, the contents of the `templates.json` file are used as input,
when constructing the final result contents by following a `recipe` definition.

The recipes are defined in `recipes.json` file that resides in the same folder,
whose JSON nodes simply define the recipe-name and the list of templates-names.
"""

import json

from pathlib import Path
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union


class Template(NamedTuple):
    """Represents a named list of URLs pointing to template .gitignore contents.

    Each URL contained in the list is expected to point a plain-text resource,
    containing the sample contents of .gitignore file for a similar purpose."""

    name: str
    urls: List[str]

    def as_dict(self) -> Dict[str, Union[str, list]]:
        """Returns dict with the current Template details."""

        return self._asdict()

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, list]]) -> "Template":
        """Creates and returns a Template instance from dict data."""

        try:
            name, urls = data["name"], data["urls"]
        except KeyError as e:
            raise ValueError("data", data) from e

        if not isinstance(name, str):
            raise TypeError("name", str, type(name), name)

        if not isinstance(urls, list):
            raise TypeError("urls", list, type(urls), urls)

        for idx, url in enumerate(urls):
            if not isinstance(url, str):
                raise TypeError(f"urls[{idx}]", str, type(url), url)

        result_name = name.strip()
        if not result_name:
            raise ValueError("name", name)

        result_urls = [url.strip()
                       for url
                       in urls
                       if url.strip()]
        if not result_urls:
            raise ValueError("urls", urls)

        return cls(
            name=result_name,
            urls=result_urls
        )


class Templates(NamedTuple):
    """Represents list of all Templates used for generation during runtime."""

    templates: List[Template]

    def __add__(self, other):
        if isinstance(other, Templates):
            return Templates(self.templates + other.templates)
        raise TypeError(Templates, type(other), other)

    def as_dict(self) -> Dict[str, Union[str, list]]:
        """Returns the current instance data as dict."""

        return {
            "templates": [t.as_dict() for t in self.templates]
        }

    def as_json(self) -> str:
        """Returns the JSON representation of the current object's data."""

        return json.dumps(
            self.as_dict(),
            ensure_ascii=True,
            indent=4,
            sort_keys=False
        )

    def save(self, file: Path):
        """Formats the current instance data as JSON, and writes it to the file.
        """

        if not isinstance(file, Path):
            raise TypeError("file", Path, type(file), file)

        if file.exists() and (not file.is_file()):
            raise IsADirectoryError(file)

        folder = file.parent
        folder.mkdir(parents=True, exist_ok=True)

        text = self.as_json()
        file.write_text(text, encoding="ascii", errors="surrogateescape")

    @classmethod
    def from_dict(cls, data: Dict[str, list]) -> "Templates":
        """Creates Templates instance by parsing data from the given dict."""

        try:
            data_templates = data["templates"]
        except KeyError as e:
            raise ValueError("data", data) from e

        if not isinstance(data_templates, list):
            raise TypeError(
                "templates", list, type(data_templates), data_templates
            )

        result_templates = []

        for idx, data_template in enumerate(data_templates):
            if not isinstance(data_template, dict):
                raise TypeError(
                    f"templates[{idx}]",
                    dict,
                    type(data_template),
                    data_template
                )

            try:
                result_template = Template.from_dict(data_template)
                result_templates.append(result_template)
            except (TypeError, ValueError) as e:
                raise ValueError(f"templates[{idx}]", data_template) from e

        if not result_templates:
            raise ValueError("templates", data_templates)

        return cls(templates=result_templates)

    @classmethod
    def from_json(cls, text: str) -> "Templates":
        """Creates Templates instance by parsing string with JSON data."""

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError("text", text) from e

        return cls.from_dict(data)

    @classmethod
    def load(cls, file: Path) -> "Templates":
        """Loads definition of Templates from JSON file."""

        if not isinstance(file, Path):
            raise TypeError("file", Path, type(file), file)

        if not file.exists():
            raise FileNotFoundError(file)

        if not file.is_file():
            raise IsADirectoryError(file)

        text = file.read_text(encoding="ascii", errors="surrogateescape")
        return cls.from_json(text)


OS_TEMPLATES = Templates(
    [
        Template(
            name="linux",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/Linux.gitignore",
                "https://www.toptal.com/developers/gitignore/api/linux",
            ]
        ),
        Template(
            name="macos",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/macOS.gitignore",
                "https://www.toptal.com/developers/gitignore/api/macos",
            ]
        ),
        Template(
            name="windows",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/Windows.gitignore",
                "https://www.toptal.com/developers/gitignore/api/windows",
            ]
        )
    ]
)

IDE_TEMPLATES = Templates(
    [
        Template(
            name="android_studio",
            urls=[
                "https://github.com/github/gitignore/raw/main/Android.gitignore",
                "https://www.toptal.com/developers/gitignore/api/android,androidstudio",
            ]
        ),
        Template(
            name="eclipse",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/Eclipse.gitignore",
                "https://www.toptal.com/developers/gitignore/api/eclipse",
            ]
        ),
        Template(
            name="netbeans",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/NetBeans.gitignore",
                "https://www.toptal.com/developers/gitignore/api/netbeans",
            ]
        ),
        Template(
            name="intellij",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/JetBrains.gitignore",
                "https://www.toptal.com/developers/gitignore/api/intellij,intellij+all,intellij+iml",
            ]
        ),
        Template(
            name="pycharm",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/JetBrains.gitignore",
                "https://www.toptal.com/developers/gitignore/api/pycharm,pycharm+all,pycharm+iml,pydev",
            ]
        ),
        Template(
            name="jupyter_notebooks",
            urls=[
                "https://github.com/github/gitignore/raw/main/community/Python/JupyterNotebooks.gitignore",
                "https://www.toptal.com/developers/gitignore/api/jupyternotebooks",
            ]
        ),
        Template(
            name="visual_studio",
            urls=[
                "https://github.com/github/gitignore/raw/main/VisualStudio.gitignore",
                "https://www.toptal.com/developers/gitignore/api/visualstudio,visualstudiocode",
            ]
        ),
    ]
)

LANG_TEMPLATES = Templates(
    [
        Template(
            name="java",
            urls=[
                "https://github.com/github/gitignore/raw/main/Java.gitignore",
                "https://github.com/github/gitignore/raw/main/JBoss.gitignore",
                "https://github.com/github/gitignore/raw/main/Maven.gitignore",
                "https://github.com/github/gitignore/raw/main/Gradle.gitignore",
                "https://github.com/github/gitignore/raw/main/Global/JDeveloper.gitignore",
                "https://github.com/github/gitignore/raw/main/Global/JEnv.gitignore",
                "https://github.com/github/gitignore/raw/main/community/Java/JBoss4.gitignore",
                "https://github.com/github/gitignore/raw/main/community/Java/JBoss6.gitignore",
                "https://www.toptal.com/developers/gitignore/api/java,gradle,maven",
            ]
        ),
        Template(
            name="python",
            urls=[
                "https://github.com/github/gitignore/raw/main/Python.gitignore",
                "https://github.com/github/gitignore/raw/main/community/Python/Nikola.gitignore",
                "https://github.com/pyscaffold/pyscaffold/raw/master/src/pyscaffold/templates/gitignore.template",
                "https://www.toptal.com/developers/gitignore/api/python,pythonvanilla,django,flask",
            ]
        ),
    ]
)

ALL_TEMPLATES = OS_TEMPLATES + IDE_TEMPLATES + LANG_TEMPLATES
