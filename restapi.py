from __future__ import absolute_import, division, print_function

from wsgiref import simple_server
import falcon
import json
import Queue
import sys, os
import datetime
import logging

from swiftutils import get_temp_key, get_temp_url

import swiftclient
# from swiftclient import client
import peewee

from config import Config
from models import AccountModel, database
from myexceptions import UserNotExistException, PasswordIncorrectException
import keystonewrap
import swiftwrap

logging.basicConfig(format='===========My:%(levelname)s:%(message)s=========', 
    level=logging.DEBUG)
#sys.path.append('.')



conf = Config('swiftconf.conf')

app = falcon.API()

if conf.auth_version == "2":
    from restapi_v2 import HomeListener, PathListener, AccountListener, \
        DiskSinkAdapter

    home_listener = HomeListener()
    path_listener = PathListener()
    account_listener = AccountListener()
    sink = DiskSinkAdapter()
elif conf.auth_version is "1":
    home_listener = HomeListener_v1()
    path_listener = PathListener_v1()
    account_listener = AccountListener_v1()
    sink = DiskSinkAdapter()
# home_listener = HomeListener()
# path_listener = PathListener()
# account_listener = AccountListener()

# app.add_route('/v1/disk/{path}/{file}', path_listener)
app.add_route('/v1/disk', home_listener)
app.add_route('/v1/account', account_listener)
# app.add_route('/v1/disk/{filename}', home_listener)

app.add_sink(sink, r'^/v1/disk/(?P<path2file>.+?)$')


## Useful for debugging problems in your API; works with pdb.set_trace()
# if __name__ == '__main__':
#     httpd = simple_server.make_server('127.0.0.1', 8008, app)
#     httpd.serve_forever()

# conf = Config('swiftconf.conf')
# conn = swiftclient.Connection(conf.auth_url,
#                                   'test:tester',
#                                   'testing',
#                                   auth_version=conf.auth_version or 1)
# conn.head_account()