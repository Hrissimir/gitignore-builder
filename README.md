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

```console
Usage: gitignore-builder {java|python} [out]

  Generate language-specific .gitignore contents and send them to output.

  Args:

      out: Output target. [default: print to stdout]

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.
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

#### Version 0.1.1
- Bugfix

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
