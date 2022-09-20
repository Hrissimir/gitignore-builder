"""Helper module with logic that doesn't fit into any other module."""

import logging
from typing import Optional

import requests

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def url_to_text(url: str) -> Optional[str]:
    """Call this to retrieve text contents from a given URL.

    Args:
        url(str): Target URL

    Returns:
        str: The URL contents upon success, None in all other cases.
    """

    _log.debug("Getting text contents from URL: '%s' ...", url)
    try:
        with requests.get(url, allow_redirects=True) as response:
            text = response.text
        _log.debug(
            "Text successfully retrieved! Contents below this line:\n%s", text
        )
        return text

    except Exception as e:
        _log.error(
            "Error while getting text from url '%s'! Details: %s", url, e
        )
        return None
