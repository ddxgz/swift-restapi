import logging
import json

import swiftclient

from myexceptions import KeystoneUserCreateException
from config import Config
import keystonewrap


conf = Config('swiftconf.conf')


def createuser(swift_tenant, username, password, account_level):
    """
    return a dict contains userinfo and containers
    """
    if conf.auth_version is '1':
        logging.error('createuser requres auth_version 2!')
    logging.debug('in swiftwrap createuser')
    try:
        user = keystonewrap.createuser(swift_tenant, username, password)
        logging.debug(json.dumps(user, encoding='utf-8'))
        logging.debug('services:%s'%conf.services)
        for container in conf.services:
            logging.debug('recu')
            put_container(swift_tenant, username, password, 
                username+'_'+container)
        return user
    except KeystoneUserCreateException:
        logging.debug('==in swiftwrap KeystoneUserCreateException!')
        raise


def put_container(swift_tenant, username, password, container):
    logging.debug('swift_tenant:')

    conn = swiftclient.Connection(conf.auth_url,
                                  swift_tenant+':'+username,
                                  password,
                                  auth_version=2)
    conn.put_container(container)

# createuser(conf.account, 'tester402', 'testing', 0)