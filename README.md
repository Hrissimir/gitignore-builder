# gitignore-builder

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitignore-builder.svg)](https://pypi.org/project/gitignore-builder)
[![PyPI - Version](https://img.shields.io/pypi/v/gitignore-builder.svg)](https://pypi.org/project/gitignore-builder)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

-----

**Table of Contents**

- [Installation](#installation)
- [Contribution](#contribution)
- [License](#license)

## Installation

```console
pip install gitignore-builder
```

## Contribution

Install required packages:

```shell
pip install --upgrade virutalenv pipenv hatch
```

Get the project code:

```shell
git clone git@github.com:Hrissimir/gitignore-builder.git
```

Create and activate development environment:

```shell
cd gitignore-builder
pipenv install --dev
pipenv shell
```

**NOTE**:
**All further instructions assume commands are invoked inside active dev-env!**

Run the unit-tests with coverage:

```shell
hatch run cov
```

Build the project distributions:

```shell
# wheel only
hatch build -t wheel

# sdist only
hatch build -t stdist

# both
hatch build
```

Configure PyPI tokens:

```shell
# syntax: keyring set <private-repository URL> <private-repository username>
keyring set https://test.pypi.org/legacy/ __token__  # for Test-PyPI
keyring set https://upload.pypi.org/legacy/ __token__  # for Main-PyPI
```

Publish the project distributions:

```shell
hatch publish --repo test  # to Test-PyPI
hatch publish --repo main  # to Main-PyPI
hatch publish  # to Main-PyPI
```

## License

`gitignore-builder` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
