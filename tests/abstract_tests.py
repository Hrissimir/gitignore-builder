"""This module defines common abstract base classes."""
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory
from typing import Optional
from unittest import TestCase

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
