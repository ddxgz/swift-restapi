from keystoneclient.v2_0 import client
from keystoneclient.v3 import client as client3
import swiftclient
from config import Config

import logging, commands


logging.basicConfig(format='===========My:%(levelname)s:%(message)s=========', 
    level=logging.DEBUG)


# kc = client.Client(tenant_name='restapi', 
#                   username='tester', 
#                   password='testing', 
#                   auth_url='http://10.200.44.66:5000/v2.0')

# tenants = kc.tenants.list()

# users = kc.users.list()

admin_client = client3.Client(token='ADMIN',
                            endpoint='http://10.200.44.66:35357/v3.0')
tenants = admin_client.projects.list()
print 'tenants: \n', tenants

conf = Config('swiftconf.conf')

logging.debug('self.conf.auth_url: %s,  conf.auth_version: %s' % (
                 conf.auth_url, conf.auth_version))

conn = swiftclient.Connection(conf.auth_url,
                            conf.account_username,
                            conf.password,
                            auth_version=conf.auth_version)
meta, objects = conn.get_container(conf.container)

logging.debug('meta: %s, \n  obj: %s' % (meta, objects))

## ok for uploading file
# auth_ref = kc.auth_ref
# logging.debug('auth_ref:%s' % auth_ref['serviceCatalog'][0]['endpoints'][0]['publicURL'])

# logging.debug('curl -X PUT --data-binary "@curl.py" \
#         -H "X-Auth-Token: %s"\
#         %s/disk/curl.py' % 
#         (auth_ref['token']['id'], auth_ref['serviceCatalog'][0]['endpoints'][0]['publicURL']))

# stat = commands.getoutput('curl -X PUT --data-binary "@config.py" \
#         -H "X-Auth-Token: %s"\
#         %s/disk/config.py' % 
#         (auth_ref['token']['id'], auth_ref['serviceCatalog'][0]['endpoints'][0]['publicURL']))
# logging.debug('put stat:%s' % stat)