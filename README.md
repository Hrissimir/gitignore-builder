# gitignore-builder

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![CI - Test](https://github.com/Hrissimir/gitignore-builder/actions/workflows/test.yml/badge.svg)](https://github.com/Hrissimir/gitignore-builder/actions/workflows/test.yml)                                                                                                                                                                                                                                                                                                                                                                                 |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/gitignore-builder.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/gitignore-builder) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitignore-builder.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/gitignore-builder)                                                                                                                                                                                                                          |
| Meta    | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) |

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

#### Version 1.0.1

- Minor bugfix

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
