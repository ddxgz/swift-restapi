import os

from six.moves import configparser


class Config(object):
    def __init__(self, conf_file=None):
        if conf_file:
            self.config_file = conf_file
            self._get_config(specified=True)
        else:
            self._get_config()

    def _get_config(self, specified=False):
        if specified is True:
            config_file = self.config_file
        else:
            config_file = os.environ.get('',
                                     './server.conf')
        config = configparser.SafeConfigParser({'auth_version': '1'})
        config.read(config_file)
        if config.has_section('swiftconf'):
            auth_host = config.get('swiftconf', 'auth_host')
            auth_port = config.getint('swiftconf', 'auth_port')
            auth_ssl = config.getboolean('swiftconf', 'auth_ssl')
            auth_prefix = config.get('swiftconf', 'auth_prefix')
            self.auth_host = auth_host
            self.auth_version = config.get('swiftconf', 'auth_version')
            self.account = config.get('swiftconf', 'account')
            self.username = config.get('swiftconf', 'username')
            self.password = config.get('swiftconf', 'password')
            self.disk_container = config.get('swiftconf', 'disk_container')
            self.auth_url = ""
            if auth_ssl:
                self.auth_url += "https://"
            else:
                self.auth_url += "http://"
            self.auth_url += "%s:%s%s" % (auth_host, auth_port, auth_prefix)
            if self.auth_version == "1":
                self.auth_url += 'v1.0'
            self.account_username = "%s:%s" % (self.account, self.username)
        else:
            self.skip_tests = True
        
        if config.has_section('services'):
            services_line = config.get('services', 'services')
            service_list = services_line.split(',')
            self.services = [i.strip() for i in service_list]

        if config.has_section('devsetting'):
            no_catch = config.get('devsetting', 'no_catch')
            if no_catch is '0':
                self.no_catch = 0
            else:
                self.no_catch = 1
            auto_rename = config.get('devsetting', 'auto_rename')
            if auto_rename is '0':
                self.auto_rename = 0
            else:
                self.auto_rename = 1

        if config.has_section('keystone'):
            self.admin_token = config.get('keystone', 'admin_token')
            self.auth_url_v2 = config.get('keystone', 'auth_url_v2')
            self.endpoint_url_v2 = config.get('keystone', 'endpoint_url_v2')
            self.swift_role = config.get('keystone', 'swift_role')
            self.swift_region = config.get('keystone', 'swift_region')
            self.swift_service = config.get('keystone', 'swift_service')
            
