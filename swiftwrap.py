import logging
import json

import swiftclient

from myexceptions import KeystoneUserCreateException
from config import Config
import keystonewrap


conf = Config()


def create_user(swift_tenant, username, password, account_level):
    """
    return a dict contains userinfo and containers
    """
    if conf.auth_version is '1':
        logging.error('createuser requres auth_version 2!')
    logging.debug('in swiftwrap createuser')
    try:
        user = keystonewrap.create_user(swift_tenant, username, password)
        logging.debug(json.dumps(user, encoding='utf-8'))
        logging.debug('services:%s'%conf.services)
        for container in conf.services:
            logging.debug('recu')
            put_container(swift_tenant, username, password, 
                username+'_'+container)
        return user
    except KeystoneUserCreateException:
        logging.debug('swiftwrap KeystoneUserCreateException!')
        raise


def put_container(tenant, username, password, container):
    logging.debug('swift_tenant:')

    conn = swiftclient.Connection(conf.auth_url,
                                  tenant+':'+username,
                                  password,
                                  auth_version=conf.auth_version)
    conn.put_container(container)


def move_object(tenant, username, password, container, source, dest):

    copy_object(tenant, username, password, container, source, dest)
    conn = swiftclient.Connection(conf.auth_url,
                                  tenant+':'+username,
                                  password,
                                  auth_version=conf.auth_version)
    conn.delete_object(container, source)


def copy_object(tenant, username, password, container, source, dest):
    headers = {}
    conn = swiftclient.Connection(conf.auth_url,
                                  tenant+':'+username,
                                  password,
                                  auth_version=conf.auth_version)
    headers['X-Copy-From'] = '/' + container + '/' + source
    headers['Content-Length'] = 0
    conn.put_object(container, dest, headers)

# createuser(conf.account, 'tester402', 'testing', 0)
