"""
Tests for custom Django management commands.
Command: pytest core/tests
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError


@patch('core.management.commands.wait_for_db.Command.check')
def test_wait_for_db_ready(patched_check):
    """Test waiting for database if the database is ready."""

    patched_check.return_value = True

    call_command('wait_for_db')

    patched_check.assert_called_once_with(databases=['default'])


@patch('core.management.commands.wait_for_db.Command.check')
@patch('time.sleep')
def test_wait_for_db_delay(patched_sleep, patched_check):
    """Test waiting database when getting OperationalError."""

    patched_check.side_effect = [Psycopg2Error] * 2 + \
                                [OperationalError] * 3 + [True]

    call_command('wait_for_db')

    assert patched_check.call_count == 6
    patched_check.assert_called_with(databases=['default'])

