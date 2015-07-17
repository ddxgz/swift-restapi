from keystoneclient.v2_0 import client
from keystoneclient.v3 import client as client3
import swiftclient
from config import Config

import logging, commands


# logging.basicConfig(format='\n===========My:%(levelname)s:%(message)s=========', 
#     level=logging.DEBUG)

conf = Config()

kc2 = client.Client(tenant_name='admin', 
                  username='admin', 
                  password='admin', 
                  auth_url='http://10.200.44.66:5000/v2.0')

kc = client.Client(token=conf.admin_token,
                            endpoint=conf.endpoint_url_v2, debug=True)

# kc.tenants.create(tenant_name='test4', description='test4 tenant', 
#     enabled=True)

atenants = kc.tenants.list()
tenants = kc2.tenants.list()

logging.debug('tenants:%s' % tenants)
logging.debug('tenants:%s' % tenants)
# logging.debug('tenants:%s' % [t.name for t in tenants])

# test1tenant = [x for x in tenants if x.name=='test4'][0]
# logging.debug('test1tenant:%s' % test1tenant.id)

# testuser1 = kc.users.create(name='testuser4', password='testing',
#     tenant_id=test1tenant.id)

users = kc.users.list()
# logging.debug('users:%s' % users)
# logging.debug('users:%s' % [t.name for t in users])
testuser1 = [x for x in users if x.name=='testuser4'][0]
# logging.debug('testuser1:%s' % testuser1.id)

# roles = kc.roles.list()
# logging.debug('roles:%s' % roles)
# logging.debug('roles:%s' % [t.name for t in roles])

# testrole = kc.roles.create('swifttestrole1')
# testrole = [x for x in roles if x.name=='swiftoperator'][0]
# logging.debug('testrole:%s' % testrole)

# logging.debug('before add_user_role, \n user:%s, \n role:%s, \n tenant:%s'
#     % (testuser1, testrole, test1tenant))

# kc.roles.add_user_role(testuser1, testrole, tenant=test1tenant, )

# temporary use this to add user role
"""
curl -g -i -X PUT http://10.200.44.66:35357/v2.0/tenants/9496d2f257124344a5a985db2b5fc2f7/users/b376afc290db49b5a10b59729dd174fb/roles/OS-KSADM/3ec64ede69bb49f9aaa34d3b5b48d9bf -H "User-Agent: python-keystoneclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}b521caa6e1db82e5a01c924a419870cb72b81635"
"""

# roleforuser = kc.roles.roles_for_user(testuser1, test1tenant)
# logging.debug('roleforuser:%s' % roleforuser)

services = kc.services.list()
logging.debug('services:%s' % services)
logging.debug('services:%s' % [t.name for t in services])
service = [x for x in services if x.name=='swift'][0]
logging.debug('service:%s' % service)

endpoints = kc.endpoints.list()
logging.debug('endpoints:%s' % endpoints[0])

# kc.endpoints.create(
#      region="RegionOne", service_id=service.id,
#     publicurl="http://10.200.44.66:8080/v1/AUTH_%s" % test1tenant.id,
#     internalurl="http://10.200.44.66:8080/v1/AUTH_%s" % test1tenant.id,
#     adminurl="http://10.200.44.66:5000/v2.0")



# admin_client = client3.Client(token='ADMIN',
#                             endpoint='http://10.200.44.66:35357/v3.0')
# tenants = admin_client.projects.list()
# print 'tenants: \n', tenants

# conf = Config('swiftconf.conf')

# logging.debug('self.conf.auth_url: %s,  conf.auth_version: %s' % (
#                  conf.auth_url, conf.auth_version))

# conn = swiftclient.Connection(conf.auth_url,
#                             conf.account_username,
#                             conf.password,
#                             auth_version=conf.auth_version)
# meta, objects = conn.get_container(conf.container)
# conn.head_account()
# logging.debug('meta: %s, \n  obj: %s' % (meta, objects))

# ## ok for uploading file
# auth_ref = kc.auth_ref
# logging.debug('auth_ref:%s' % auth_ref['serviceCatalog'][0]['endpoints'][0]['publicURL'])
# logging.debug('auth_ref:%s' % auth_ref)

# logging.debug('curl -X PUT --data-binary "@curl.py" \
#         -H "X-Auth-Token: %s"\
#         %s/disk/curl.py' % 
#         (auth_ref['token']['id'], auth_ref['serviceCatalog'][0]['endpoints'][0]['publicURL']))

# stat = commands.getoutput('curl -X PUT --data-binary "@config.py" \
#         -H "X-Auth-Token: %s"\
#         %s/disk/config.py' % 
#         (auth_ref['token']['id'], auth_ref['serviceCatalog'][0]['endpoints'][0]['publicURL']))
# logging.debug('put stat:%s' % stat)