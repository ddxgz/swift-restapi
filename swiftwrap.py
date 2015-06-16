import logging
import json

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
    user = keystonewrap.createuser(swift_tenant, username, password)
    logging.debug(json.dumps(user, encoding='utf-8'))
    # for service in conf.services:
    #     put_container(swift_tenant, username, service)
    return user

# createuser(conf.account, 'tester402', 'testing', 0)