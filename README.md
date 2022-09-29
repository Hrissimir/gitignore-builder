# gitignore-builder

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitignore-builder.svg)](https://pypi.org/project/gitignore-builder)
[![PyPI - Version](https://img.shields.io/pypi/v/gitignore-builder.svg)](https://pypi.org/project/gitignore-builder)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

-----

**Table of Contents**

- [Usage](#usage)
- [Installation](#installation)
- [Changelog](#changelog)
- [License](#license)

-----

## Usage

### CLI command's 'help' output:

```console
Usage: gitignore-builder [OPTIONS] {android|java|python} [OUTPUT]

  Generate .gitignore contents from recipe and write them to the output.

Options:
  -c, --config  Print the location of app config files.
  -h, --help    Show this message and exit.
```

### Sample CLI command invocations

```shell
# print the command help description
gitignore-builder --help

# print absolute paths to the app config files
gitignore-builder --config

# generate and print .gitignore file contents
gitignore-builder java

# generate and write the contents to '.gitignore' file in current dir
gitignore-builder python .gitignore
```

-----

## Installation

Installing with Pip

```shell
# from PyPI 
pip install gitignore-builder

# from source
git clone git@github.com:Hrissimir/gitignore-builder.git
cd gitignore-builder
pip install .
```

-----

## Changelog

#### Version 1.0.0

- Introduced the concepts of 'recipes' and 'templates'
- Implemented usage of recipes.yaml and templates.yaml
    - Created in per-user app-config dir upon first usage
    - Editable by the user to provide extra/custom values
- Implemented support for printing paths to the app data-files
- Improved of the bundled lists of templates and recipes
- Improved CLI command help-description.
- Better unit-tests coverage

#### Version 0.1.0

- Added basic implementation of the CLI command.
- Initial PyPI publication.

#### Version 0.0.1

- Generated project skeleton
- Added README.md
- Added CONTRIBUTING.md
- Configured the GitHub CI/CD pipeline.

-----

## License

`gitignore-builder` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
