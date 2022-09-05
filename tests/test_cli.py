"""Unit-tests for the main CLI entry point."""
import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import IO
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Union
from unittest import TestCase

from click.core import BaseCommand
from click.testing import CliRunner
from click.testing import Result

from gitignore_builder import cli

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class CliCommandTestBase(TestCase, ABC):
    args: Optional[List[str]]
    result: Optional[Result]
    runner: Optional[CliRunner]

    def setUp(self) -> None:
        self.args = None
        self.result = None
        self.runner = CliRunner()

    def tearDown(self) -> None:
        self.runner = None
        self.result = None
        self.args = None

    @property
    @abstractmethod
    def command(self) -> BaseCommand:
        pass  # no cov

    def invoke(
            self,
            args: Optional[Union[str, Sequence[str]]] = None,
            input: Optional[Union[str, bytes, IO]] = None,
            env: Optional[Mapping[str, Optional[str]]] = None,
            catch_exceptions: bool = True,
            color: bool = False,
            **extra: Any,
    ) -> Result:
        self.result = self.runner.invoke(
            self.command, args, input, env, catch_exceptions, color, **extra
        )
        return self.result


class MainCliTest(CliCommandTestBase):

    @property
    def command(self):
        return cli.gitignore_builder

    def test_help_option_call_short_name(self):
        self.invoke(["-h"])
        self.assertIn("Usage: gitignore-builder {java|python} [out]", self.result.output)

    def test_help_option_call_full_name(self):
        self.invoke(["--help"])
        self.assertIn("Usage: gitignore-builder {java|python} [out]", self.result.output)
