"""This module defines the app CLI entry point."""
# SPDX-FileCopyrightText: 2022-present Hrissimir <hrisimir.dakov@gmail.com>
#
# SPDX-License-Identifier: MIT

import click

from gitignore_builder import builder
from gitignore_builder import datamodel
from ..__about__ import __version__  # pylint: disable=relative-beyond-top-level

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "show_default": True,
    "terminal_width": 160,
    "max_content_width": 160
}

datamodel.init()


def show_files(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"recipes file: {gitignore_builder.datamodel.get_recipes_file()}")
    click.echo(f"templates file: {gitignore_builder.datamodel.get_templates_file()}")
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.version_option(version=__version__, prog_name="gitignore-builder")
@click.option(
    "--files",
    is_flag=True,
    callback=show_files,
    expose_value=False,
    is_eager=True,
    help="Show paths to app data-files and exit."
)
@click.argument("recipe", type=click.Choice(datamodel.get_recipe_names()))
@click.argument("output", type=click.File("w"), default="-")
def gitignore_builder(recipe, output):
    """Build .gitignore contents from recipe URLs and write result to output."""

    click.echo(f"Building .gitignore contents using recipe: '{recipe}' ...")
    urls = datamodel.get_recipe_urls(recipe)
    text = builder.build_gitignore_contents(urls)
    click.echo("...done!")

    click.echo(f"Writing the result to: '{output}' ...")
    click.echo(text, file=output)
    click.echo("...all done!")
