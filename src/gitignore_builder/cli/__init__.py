# SPDX-FileCopyrightText: 2022-present Hrissimir <hrisimir.dakov@gmail.com>
#
# SPDX-License-Identifier: MIT
import click
import requests

from ..__about__ import __version__
from ..builders.base_content_builder import BaseContentBuilder

# pylint: disable=line-too-long
SOURCES_BY_LANG = {
    "java": [
        "https://github.com/github/gitignore/raw/main/Java.gitignore",
        "https://github.com/github/gitignore/raw/main/Gradle.gitignore",
        "https://github.com/github/gitignore/raw/main/Global/Eclipse.gitignore",
        "https://github.com/github/gitignore/raw/main/Global/JetBrains.gitignore",
        "https://github.com/github/gitignore/raw/main/Global/JEnv.gitignore",
        "https://github.com/github/gitignore/raw/main/Android.gitignore",
        "https://github.com/github/gitignore/raw/main/Maven.gitignore",
    ],
    "python": [
        "https://github.com/github/gitignore/raw/main/Python.gitignore",
        "https://github.com/github/gitignore/raw/main/community/Python/JupyterNotebooks.gitignore",
        "https://github.com/github/gitignore/raw/main/community/Python/Nikola.gitignore",
        "https://github.com/github/gitignore/raw/main/Global/JetBrains.gitignore",
        "https://github.com/pyscaffold/pyscaffold/raw/master/src/pyscaffold/templates/gitignore.template",
    ],
}


@click.command(options_metavar="")
@click.version_option(version=__version__, prog_name='gitignore-builder')
@click.help_option("-h", "--help")
@click.argument("lang", type=click.Choice(["java", "python"]))
@click.argument("out", metavar="[out]", type=click.File("w"), default="-")
@click.pass_context
def gitignore_builder(ctx: click.Context, lang, out):
    """Generate language-specific .gitignore contents and send them to output.

    Args:

        out: Output target. [default: print to stdout]
    """

    click.echo('Hello world!')

    gitignore = BaseContentBuilder()

    with click.progressbar(SOURCES_BY_LANG[lang]) as source_urls:
        for src in source_urls:
            try:
                with requests.get(src) as resp:
                    contents = resp.text
            except Exception as ex:  # pylint: disable=broad-except
                click.echo(f"failed to get {src} due {ex}!", err=True)
                continue

            gitignore.append_section(src, contents)

    result = str(gitignore)
    click.echo(result, file=out)
