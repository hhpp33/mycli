# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
#import db_utils as dbutils
import fixture_utils as fixutils


def before_all(context):
    """
    Set env parameters.
    """
    os.environ['LINES'] = "100"
    os.environ['COLUMNS'] = "100"
    os.environ['PAGER'] = 'cat'
    os.environ['EDITOR'] = 'nano'

    context.exit_sent = False

    vi = '_'.join([str(x) for x in sys.version_info[:3]])
    db_name = context.config.userdata.get('my_test_db', None)
    #db_name_full = '{0}_{1}'.format(db_name, vi)
    db_name_full = None

    # Store get params from config.
    context.conf = {
        'host': context.config.userdata.get('my_test_host', 'localhost'),
        'user': context.config.userdata.get('my_test_user', 'postgres'),
        'pass': context.config.userdata.get('my_test_pass', None),
        'cli_command': context.config.userdata.get('my_cli_command', None) or 'python -m mycli.main',
        'dbname': None,
        'dbname_tmp': None,
        'vi': vi
    }

    # if context.conf['pass']:
    #     os.environ['PGPASS'] = context.conf['pass']
    # else:
    #     if 'PGPASS' in os.environ:
    #         del os.environ['PGPASS']
    #     if 'PGHOST' in os.environ:
    #         del os.environ['PGHOST']

    #context.cn = dbutils.create_db(context.conf['host'], context.conf['user'],
    #                               context.conf['pass'],
    #                               context.conf['dbname'])

    context.fixture_data = fixutils.read_fixture_files()


def after_all(context):
    """
    Unset env parameters.
    """
    #dbutils.close_cn(context.cn)
    #dbutils.drop_db(context.conf['host'], context.conf['user'],
    #                context.conf['pass'], context.conf['dbname'])

    # Restore env vars.
    #for k, v in context.pgenv.items():
    #    if k in os.environ and v is None:
    #        del os.environ[k]
    #    elif v:
    #        os.environ[k] = v


def after_scenario(context, _):
    """
    Cleans up after each test complete.
    """

    if hasattr(context, 'cli') and not context.exit_sent:
        # Terminate nicely.
        context.cli.terminate()
