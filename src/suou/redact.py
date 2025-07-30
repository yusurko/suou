"""
"Security through obscurity" helpers for less sensitive logging
"""

import re


def redact_url_password(u: str) -> str:
    """
    Remove password from URIs.

    The password part in URIs is:
    scheme://username:password@hostname/path?query
                      ^------^

    NEW 0.5.0
    """
    return re.sub(r':[^@:/ ]+@', ':***@', u)


__all__ = ('redact_url_password', )