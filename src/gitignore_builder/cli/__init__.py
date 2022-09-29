"""This module defines the app CLI entry point."""
# SPDX-FileCopyrightText: 2022-present Hrissimir <hrisimir.dakov@gmail.com>
#
# SPDX-License-Identifier: MIT

import click

from gitignore_builder import builder
from gitignore_builder import datamodel

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "show_default": True,
    "terminal_width": 160,
    "max_content_width": 160
}

datamodel.init()


def print_config(ctx, param, value):  # pylint: disable=unused-argument
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Recipes file: '{datamodel.get_recipes_file()}'")
    click.echo(f"Templates file: '{datamodel.get_templates_file()}'")
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option("-c", "--config",
              is_flag=True,
              callback=print_config,
              expose_value=False,
              is_eager=True,
              help="Print the location of app config files.")
@click.argument("recipe",
                type=click.Choice(datamodel.get_recipe_names()))
@click.argument("output",
                type=click.File("w"),
                default="-")
def gitignore_builder(recipe, output):
    """Generate .gitignore contents from recipe and write them to the output."""

    click.echo(f"Building .gitignore contents using recipe: '{recipe}' ...")

    lines = []

    urls = list(datamodel.get_recipe_urls(recipe))
    with click.progressbar(urls) as recipe_urls:
        for url in recipe_urls:
            title = f"source: {url}"
            builder.append_url(lines, url, title)

    text = "\n".join(lines)
    click.echo("...done!")

    click.echo(f"Writing the resulting .gitignore contents to: '{output}' ...")
    click.echo(text, file=output)
    click.echo("...done!")
