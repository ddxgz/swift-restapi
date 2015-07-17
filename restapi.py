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


# logging.basicConfig(
#     filename='log_restapi.log', filemode='w',
#     level=logging.DEBUG,
#     format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
#     datefmt='%d %b %Y %H:%M:%S')


conf = Config()

app = falcon.API()

if conf.auth_version == "2":
    from restapi_keystone import HomeListener, PathListener, AccountListener, \
        DiskSinkAdapter

    # home_listener = HomeListener()
    # path_listener = PathListener()
    # account_listener = AccountListener()
    # sink = DiskSinkAdapter()
elif conf.auth_version is "1":
    from restapi_tempauth import HomeListener, PathListener, AccountListener, \
        DiskSinkAdapter
    # home_listener = HomeListener()
    # path_listener = PathListener()
    # account_listener = AccountListener()
    # sink = DiskSinkAdapter()

home_listener = HomeListener()
# path_listener = PathListener()
account_listener = AccountListener()
sink = DiskSinkAdapter()
    
# app.add_route('/v1/disk/{path}/{file}', path_listener)
app.add_route('/v1/disk', home_listener)
app.add_route('/v1/account', account_listener)
# app.add_route('/v1/disk/{filename}', home_listener)

app.add_sink(sink, r'^/v1/disk/(?P<path2file>.+?)$')


## Useful for debugging problems in your API; works with pdb.set_trace()
# if __name__ == '__main__':
# def runserver():
#     httpd = simple_server.make_server('127.0.0.1', 9803, app)
#     httpd.serve_forever()
