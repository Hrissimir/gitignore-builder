"""Helper module for IO-related operations."""
import logging
from pathlib import Path
from typing import Optional

import requests
import yaml

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def format_data_to_yaml(data: dict) -> Optional[str]:
    """Serialize dict data to YAML string."""

    try:
        return yaml.dump(
            data,
            Dumper=yaml.SafeDumper,
            default_flow_style=False,
            sort_keys=False,
        )
    except Exception as e:
        _log.error("Error while formatting data to YAML! Details: '%s'", e)
        return None


def parse_data_from_yaml(text: str) -> Optional[dict]:
    """Deserialize data from YAML text."""

    try:
        return yaml.load(text, Loader=yaml.SafeLoader)
    except Exception as e:
        _log.error("Error while parsing YAML data: '%s'", e)
        return None


def read_file_as_text(file: Path) -> Optional[str]:
    """Read text from file."""

    _log.debug("Reading text from file: '%s'", file)
    try:
        data = file.read_bytes()
        return data.decode(encoding="utf-8", errors="surrogateescape")
    except Exception as e:
        _log.error("Error while reading text from file: '%s'", e)
        return None


def read_file_as_data(file: Path) -> Optional[dict]:
    """Parse and return data from YAML file."""

    _log.info("Reading data from file: '%s'", file)
    text = read_file_as_text(file)
    if text is None:
        _log.error("...FAILED! (could not read the file)")
        return None

    data = parse_data_from_yaml(text)
    if data is None:
        _log.error("...FAILED! (could not parse the data)")

    _log.debug("...DONE!")
    return data


def read_url_as_text(url: str) -> Optional[str]:
    """Call this to retrieve text contents from a given URL.

    Args:
        url(str): Target URL

    Returns:
        str: The URL contents upon success, None in all other cases.
    """

    _log.info("Reading text from URL: '%s' ...", url)

    try:
        with requests.get(url, allow_redirects=True, timeout=10) as response:
            text = response.text
        _log.info("...DONE!")
        return text

    except Exception as e:
        _log.error("...ERROR! Details: '%s'", e)
        return None


def write_text_to_file(text: str, file: Path):
    """Write text to file."""

    _log.info("Writing text to file: '%s'", file)

    folder = file.parent
    if not folder.exists():
        _log.warning("Creating missing folder at: '%s'", folder)
        folder.mkdir(parents=True, exist_ok=True)

    try:
        file_contents = text.encode(encoding="utf-8", errors="surrogateescape")
        file.write_bytes(file_contents)
    except Exception as e:
        _log.error("...ERROR! Details: '%s'", e)
        raise

    _log.info("...DONE!")


def write_data_to_file(data: dict, file: Path):
    """Serialize data to YAML and write it to file."""

    text = format_data_to_yaml(data)
    write_text_to_file(text, file)
