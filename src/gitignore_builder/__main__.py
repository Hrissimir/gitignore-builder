# pylint: disable=invalid-name,relative-beyond-top-level,missing-module-docstring
# SPDX-FileCopyrightText: 2022-present Hrissimir <hrisimir.dakov@gmail.com>
#
# SPDX-License-Identifier: MIT
import sys  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    from .cli import gitignore_builder

    sys.exit(gitignore_builder())  # pylint: disable=no-value-for-parameter
