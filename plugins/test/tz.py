
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
name: tz
version_added: 2.6.0
author:
  - Jim Tarpley (@trippsc2)
short_description: Validates Linux timezone names.
requirements:
  - pytz
description:
  - This module validates Linux timezone names using the pytz.
options:
  _input:
    type: str
    required: true
    description:
      - The timezone name to validate.
"""

EXAMPLES = r"""
- name: Validate timezone
  ansible.builtin.assert:
    that:
      - '"America/New_York" is trippsc2.general.tz'

- name: Validate timezone
  ansible.builtin.assert:
    that:
      - '"America/Not_Real" is not trippsc2.general.tz'
"""

RETURN = r"""
_value:
  type: bool
  description: Whether the timezone name is valid.
"""

from ansible.errors import AnsibleError
from ansible.module_utils.six import raise_from

from typing import Optional

try:
    from pytz import timezone
    from pytz.exceptions import UnknownTimeZoneError
except ImportError as import_exception:
    LIBRARY_MISSING_EXCEPTION: Optional[Exception] = import_exception
else:
    LIBRARY_MISSING_EXCEPTION: Optional[Exception] = None


def tz(value: str) -> bool:
    """
    Whether the timezone name is valid.

    Args:
        value: The timezone name to validate.

    Returns:
        bool: Whether the timezone name is valid.
    """

    if LIBRARY_MISSING_EXCEPTION is not None:
        raise_from(
            AnsibleError('Python package pytz must be installed to use this test.'),
            LIBRARY_MISSING_EXCEPTION
        )

    try:
        timezone(value)
    except UnknownTimeZoneError:
        return False
    except Exception as e:
        raise_from(AnsibleError('An error occurred while validating the timezone name.'), e)

    return True


class TestModule:
    def tests(self):
        return {
            'tz': tz
        }
