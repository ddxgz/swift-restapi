import logging, commands

from keystoneclient.v2_0 import client

from myexceptions import KeystoneUserCreateException
from config import Config
from utils import pretty_logging

conf = Config('swiftconf.conf')

logging.basicConfig(format='\n===========My:%(levelname)s:%(message)s=========', 
    level=logging.DEBUG)


def createuser(swift_tenant, username, password):
    """
    return a dict contains the info of the created user
    """
    # create tenant, user, role, endpoint
    admin = client.Client(token=conf.admin_token,
                            endpoint=conf.endpoint_url_v2, debug=True)

    tenants = admin.tenants.list()
    # logging.debug('tenants:%s' % tenants)
    # logging.debug('tenants:%s' % [t.name for t in tenants])
    tenantnames = [x.name for x in tenants]

    if swift_tenant not in tenantnames:       
        tenant = admin.tenants.create(tenant_name=swift_tenant, 
            description='%s tenant' % swift_tenant, 
            enabled=True)
        services = admin.services.list()
        # logging.debug('services:%s' % services)
        # logging.debug('=======services:%s' % [t.name for t in services])
        service = [x for x in services if x.name==conf.swift_service][0]
        # logging.debug('service:%s' % service)
        # endpoints = admin.endpoints.list()
        # logging.debug('endpoints:%s' % endpoints[0])

        admin.endpoints.create(
             region=conf.swift_region, service_id=service.id,
            publicurl="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id,
            internalurl="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id,
            adminurl="http://10.200.44.66:5000/v2.0")
    else:
        tenant = [x for x in tenants if x.name==swift_tenant][0]
    # logging.debug('tenant:%s' % tenant.id)

    users = admin.users.list()
    logging.debug('users:%s' % [t.name for t in users])
    usernames = [x.name for x in users]
    if username not in usernames:       
        user = admin.users.create(name=username, password=password,
            tenant_id=tenant.id)
        pretty_logging({'username':username, 
                        'tenant':tenant.name}, 'created user:')
    else:
        user = [x for x in users if x.name==username][0]

    roles = admin.roles.list()
    role = [x for x in roles if x.name==conf.swift_role][0]
    logging.debug('roles:%s' % roles)

    # admin.roles.add_user_role(user, role, tenant)
    temp_add_user_role(user, role, tenant)

    # client2 = client.Client(tenant_name=tenant.name, 
    #               username=user.name, 
    #               password=user.password, 
    #               auth_url='http://10.200.44.66:5000/v2.0')
    endpoints = admin.endpoints.list()
    logging.debug('%s, endpoints:%s' % (len(endpoints), endpoints[0]))
    endpoint = [x.publicurl for x in endpoints \
        if x.publicurl=="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id][0]

    roleforuser = admin.roles.roles_for_user(user, tenant)
    logging.debug('roleforuser:%s, conf.swift_role:%s' % (roleforuser,
        conf.swift_role))
    if len(roleforuser) is 0:
        logging.debug('add_user_role failed for user :%s, will discard all \
            changes' % user.name)
        # admin.users.delete(user)
        temp_delete_user(user)
        logging.debug('== after admin.users.delete(user)!')
        raise KeystoneUserCreateException
    elif roleforuser[0].name == conf.swift_role:
        newuser = {}
        newuser['tenant'] = {'name':tenant.name, 'id':tenant.id}
        newuser['user'] = {'name':user.name, 'id':user.id, 
            'password':user.password}
        newuser['role'] = {'name':role.name, 'id':role.id}
        newuser['endpoint'] = endpoint
        return newuser
    else:
        logging.debug('Unknown error when create keystone user and relation')
        temp_delete_user(user)
        logging.debug('== after admin.users.delete(user)!')
        raise KeystoneUserCreateException


def temp_add_user_role(user, role, tenant):
    curlstr = 'curl -g -i -X PUT %s/tenants/%s/users/%s/roles/OS-KSADM/%s \
    -H "User-Agent: python-keystoneclient" \
    -H "Accept: application/json" \
    -H "X-Auth-Token: %s"' % (
        conf.endpoint_url_v2, tenant.id, user.id, role.id, conf.admin_token)
    stat = commands.getoutput(curlstr)
    logging.debug('temp_add_user_role stat:%s, curlstr:%s' % (stat, curlstr))


def temp_delete_user(user):
    curlstr = 'curl -g -i -X DELETE %s/users/%s \
    -H "User-Agent: python-keystoneclient" \
    -H "Accept: application/json" \
    -H "X-Auth-Token: %s"' % (
        conf.endpoint_url_v2, user.id, conf.admin_token)
    stat = commands.getoutput(curlstr)
    logging.debug('temp_add_user_role stat:%s' % stat)

# createuser(conf.account, 'tester402', 'testing')