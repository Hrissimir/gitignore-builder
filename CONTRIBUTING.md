# Contributing

Common instructions for project contributors and maintainers.

This document is aimed at the less-experienced Windows user new to Python.

Linux and MacOS users - just replace `pip instlall` with `pip3 install --user`.

The guides assume the user is having Python 3.7 or newer installed on machine.

-----

**Table of Contents**

* [Pre-requisites](#pre-requisites)
* [Contributors](#contributors)
    - [Plan](#plan)
    - [Implement](#implement)
    - [Submit](#submit)
* [Maintainers](#maintainers)
    - [Review](#review)
    - [Build](#build)
    - [Publish](#publish)

-----

# Pre-requisites

Install core packages used for development

```shell
# open CMD as Administrator and run:
pip install --upgrade setuptools wheel virutalenv pipenv hatch
# close the Administrator CMD instance
```

**NOTE: Use only NON-Administrator CMD for all instructions below this line!**

Get the code

```shell
git clone git@github.com:Hrissimir/gitignore-builder.git
```

Create and activate development environment

```shell
# navigate to project dir
cd gitignore-builder

# create dev-env and install all deps from Pipfile with single command
pipenv install --dev

# note: the dev-env is created upon first call to pipenv and reused from then on

# activate the dev-env (or prefix all further commands with 'pipenv run ')
pipenv shell

# confirm all is OK by running the unit-tests
hatch run cov
```

**NOTE**:
**All further instructions assume commands are invoked inside active dev-env!**



-----

# Contributors

## Plan

Create new branch based on master **before**  doing any changes

```shell
git checkout master
git pull --all
git pull --tags
git checkout -b branch_name_goes_here
```

Describe the functionality that you're adding:

> Get familiar with the contents of the [README.md](./README.md) file.
>
> Find a relevant section for the description or create new one if needed.
>
> Describe what you're trying to achieve from an end-user's perspective.
>
> Only add a high-level overview and maybe a couple of usage-examples.
>
> Commit the changes.

Define the desired interface and behaviour by writing the unit-tests first:

> Create new module for the unit-tests under the `tests/` folder.
>
> Write a single test that defines how the new code is going to be called.
>
> Clarify how the API should look by adding few more (does not compile yet).
>
> Proofread the unit-tests once more before proceeding.
>
> Commit the changes.

## Implement

* Add the non-existing packages/modules that were defined in the unit-tests.
* Do not implement them, just add `pass` instead of method bodies.
* Ensure the IDE shows no warnings about missing packages/modules/methods.
* Run the unit-tests until no failures due import/attr errors, only asserts.
* Commit the changes before proceeding with implementation
* Write the code as if you're never going to do any cleanup (give it your best).
* Commit every time you make a test pass, add new ones if needed.
* Repeat until all-pass and make sure the coverage is >90% with `hatch run cov`.

## Submit

1. Revisit the contents of the [README.md](./README.md) file.
2. Push your local branch to the remote repo and switch-back to master.
    ```shell
    git push --set-upstream origin branch_name_goes_here
    ```
3. Create and submit PR targeting master.
    - Keep the description brief - don't put the commit history here.
4. Get the latest changes from master after your PR is merged
    ```shell
    git checkout master
    git pull --all
    git pull --tags
    ```

-----

# Maintainers

## Review

Pull the PR contents and run the tests

```shell
git checkout master
git pull --all
git pull --tags
git checkout pr_branch_name_goes_here
hatch cov
```

* Ensure all unit-tests pass.
* Ensure coverage is above 90%.
* Ensure the contents of [README.md](./README.md) match the reality.

Merge the PR branch to master and push the changes.

```shell
git checkout master
git merge pr_branch_name_goes_here
git push
```

## Build

Bump-up the project version accordingly

```shell
hatch version patch  # no public-API changes (bugfix in method body)
hatch version minor  # backwards-compatible change (new public-API method)
hatch version major,rc  # backwards-incompatible change (e.g. release-candidate)
hatch version release  # acceptance tests passed, remove .rc suffix for release.
git commit -am "Bump-up project version to x.y.z"  # commit
git tag vX.Y.Z  # prefix the version-number with v
git push  # push the code changes
git push --tags  # push the tag change
```

Building the project distribution:

```shell
hatch build -t wheel  # wheel only
hatch build -t stdist  # sdist only
hatch build  # both
```

## Publish

Configure PyPI tokens:

```shell
# syntax: keyring set <private-repository URL> <private-repository username>
keyring set https://test.pypi.org/legacy/ __token__  # for Test-PyPI
keyring set https://upload.pypi.org/legacy/ __token__  # for Main-PyPI
```

Publish the project distributions:

```shell
# using hatch
hatch publish --repo test  # Test-PyPI
hatch publish --repo main  # Main-PyPI
hatch publish  # Main-PyPI

# using twine
twine upload --repository testpypi dist/*  # Test-PyPI
twine upload dist/*  # Main-PyPI
```

Installing from Test-PyPI:

```shell
# use this inside newly-created env
pip install --index-url https://test.pypi.org/simple/ gitignore-builder

# use this if there are issues with resolving the dependencies
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gitignore-builder
```

