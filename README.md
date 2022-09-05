# gitignore-builder

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitignore-builder.svg)](https://pypi.org/project/gitignore-builder)
[![PyPI - Version](https://img.shields.io/pypi/v/gitignore-builder.svg)](https://pypi.org/project/gitignore-builder)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

-----

## Installation

```shell
# From PyPI
pip install gitignore-builder

# From TestPyPI
pip install --index-url https://test.pypi.org/simple/ gitignore-builder

# From TestPyPI when facing dependency resolution issues with previous command
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gitignore-builder

# From source
git clone git@github.com:Hrissimir/gitignore-builder.git
cd gitignore-builder
pip install .
```

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

## License

`gitignore-builder` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
