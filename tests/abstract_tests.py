"""This module defines common abstract base classes."""
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory
from typing import Optional, List, Union, Sequence, IO, Mapping, Any
from unittest import TestCase

from click import BaseCommand
from click.testing import Result, CliRunner

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class TempDirTestBase(TestCase, ABC):
    """Base class for unit-tests that require temp-dir."""

    temp_dir: Optional[Path]

    @abstractmethod
    def setUp(self) -> None:
        self._temp_dir = TemporaryDirectory()  # pylint: disable=consider-using-with
        self.temp_dir = Path(self._temp_dir.name)
        _log.debug("setUp - created temp-dir: '%s'", self.temp_dir)

    @abstractmethod
    def tearDown(self) -> None:

        try:
            _log.debug("tearDown - performing TemporaryDirectory cleanup...")
            self._temp_dir.cleanup()
            _log.debug("tearDown - ...DONE!")
        except Exception as e:
            _log.warning(
                "tearDown - error during TemporaryDirectory cleanup: '%s'", e
            )

        self._temp_dir = None

        if self.temp_dir.exists():
            try:
                _log.debug("tearDown - deleting temp-dir...")
                rmtree(self.temp_dir, ignore_errors=True)
                _log.debug("tearDown - ...DONE!")
            except Exception as e:
                _log.warning(
                    "tearDown - error while deleting temp-dir: '%s'", e
                )

        self.temp_dir = None


class CliCommandTestBase(TempDirTestBase, ABC):
    """Base class for CLI-related unit-tests."""

    args: Optional[List[str]]
    result: Optional[Result]
    runner: Optional[CliRunner]

    def setUp(self) -> None:
        super().setUp()
        self.args = None
        self.result = None
        self.runner = CliRunner()

    def tearDown(self) -> None:
        self.runner = None
        self.result = None
        self.args = None
        super().tearDown()

    @property
    @abstractmethod
    def command(self) -> BaseCommand:
        pass  # no cov

    def invoke(
            self,
            args: Optional[Union[str, Sequence[str]]] = None,
            input: Optional[Union[str, bytes, IO]] = None,  # pylint: disable=redefined-builtin
            env: Optional[Mapping[str, Optional[str]]] = None,
            catch_exceptions: bool = True,
            color: bool = False,
            **extra: Any,
    ) -> Result:
        self.result = self.runner.invoke(
            self.command, args, input, env, catch_exceptions, color, **extra
        )
        return self.result
