import logging, commands

from keystoneclient.v2_0 import client

from myexceptions import KeystoneUserCreateException
from config import Config
from utils import pretty_logging

conf = Config('swiftconf.conf')

# logging.basicConfig(format='\n===========My:%(levelname)s:%(message)s=========', 
#     level=logging.DEBUG)


def delete_user(swift_tenant, username, password):
    """
    return a dict contains the info of the deleted user
    """
    admin = client.Client(token=conf.admin_token,
                            endpoint=conf.endpoint_url_v2, debug=True)
    users = admin.users.list()
    logging.debug('users:%s' % [t.name for t in users])
    # usernames = [x.name for x in users]
    user = [x for x in users if x.name==username]
    if user:
        tenants = admin.tenants.list()
        tenant = [x for x in tenants if x.name==swift_tenant][0]
        logging.debug('tenant:%s' % tenant)
        roles = admin.roles.list()
        role = [x for x in roles if x.name==conf.swift_role][0]
        logging.debug('role:%s' % role)
        logging.debug('user:%s' % user[0])
        # admin.roles.remove_user_role(user=user[0], role=role, tenant=tenant)
        temp_remove_user_role(user=user[0], role=role, tenant=tenant)
        logging.debug('after remove_user_role')
        temp_delete_user(user[0])
        return 1
    else:
        return 0


def create_user(swift_tenant, username, password):
    """
    return a dict contains the info of the created user
    """
    # create tenant, user, role, endpoint
    admin = client.Client(token=conf.admin_token,
                            endpoint=conf.endpoint_url_v2, debug=True)
    try:
        tenants = admin.tenants.list()
    except:
        raise KeystoneUserCreateException

    # logging.debug('tenants:%s' % tenants)
    # logging.debug('tenants:%s' % [t.name for t in tenants])
    tenantnames = [x.name for x in tenants]

    if swift_tenant not in tenantnames:
        logging.debug('no tenant')
        try:       
            tenant = admin.tenants.create(tenant_name=swift_tenant, 
                description='%s tenant' % swift_tenant, 
                enabled=True)
            services = admin.services.list()
            logging.debug('services:%s' % services)
            # logging.debug('=======services:%s' % [t.name for t in services])
            service = [x for x in services if x.name==conf.swift_service][0]
            # logging.debug('service:%s' % service)
            # endpoints = admin.endpoints.list()
            # logging.debug('endpoints:%s' % endpoints[0])

            """
            no need to crate each endpoint
            """
            # admin.endpoints.create(
            #      region=conf.swift_region, service_id=service.id,
            #     publicurl="http://%s:8080/v1/AUTH_%s" % 
            #         (conf.auth_host, tenant.id),
            #     internalurl="http://%s:8080/v1/AUTH_%s" % 
            #         (conf.auth_host, tenant.id),
            #     adminurl="http://%s:5000/v2.0" % conf.auth_host)
        except:
            raise KeystoneUserCreateException

        logging.debug('after create endpoints!:')
    else:
        tenant = [x for x in tenants if x.name==swift_tenant][0]
        logging.debug('tenant:%s' % tenant.id)

    users = admin.users.list()
    logging.debug('users:%s' % [t.name for t in users])
    usernames = [x.name for x in users]
    pretty_logging({'username':username, 
                        'tenant':tenant.name,
                        'password':password}, ' before create user:')
    if username not in usernames:
        try:   
            user = admin.users.create(name=username, password=password,
                tenant_id=tenant.id)
            pretty_logging({'username':username, 
                            'tenant':tenant.name,
                            'password':password}, 'created user:')
        except:
            raise KeystoneUserCreateException

    else:
        user = [x for x in users if x.name==username][0]

    try:
        roles = admin.roles.list()
        role = [x for x in roles if x.name==conf.swift_role][0]
        logging.debug('roles:{}, roleforswift:{}'.format(roles, role))
        assert role.name == conf.swift_role

        # admin.roles.add_user_role(user, role, tenant)
        temp_add_user_role(user, role, tenant)
    except:
        raise KeystoneUserCreateException

    # client2 = client.Client(tenant_name=tenant.name, 
    #               username=user.name, 
    #               password=user.password, 
    #               auth_url='http://10.200.44.66:5000/v2.0')
    # endpoints = admin.endpoints.list()
    # logging.debug('%s, endpoints:%s' % (len(endpoints), endpoints[0]))
    # endpoint = [x.publicurl for x in endpoints \
    #     if x.publicurl=="http://%s:8080/v1/AUTH_%s" % (conf.auth_host, tenant.id)][0]

    try:
        roleforuser = admin.roles.roles_for_user(user, tenant)
        logging.debug('roleforuser:%s, conf.swift_role:%s' % (roleforuser,
            conf.swift_role))
    except:
        raise KeystoneUserCreateException

    user_roles = [str(user_role.name) for user_role in roleforuser]
    logging.debug('user_roles:{}'.format(user_roles))
    for ur in user_roles:
        if conf.swift_role == ur:
            logging.debug('yyyyyyyyyes')
    if len(roleforuser) == 0:
        logging.debug('add_user_role failed for user :%s, will discard all \
            changes' % user.name)
        # admin.users.delete(user)
        temp_delete_user(user)
        logging.debug('after admin.users.delete(user)!')
        raise KeystoneUserCreateException
    # elif roleforuser[0].name == conf.swift_role:
    elif conf.swift_role in user_roles:
        newuser = {}
        newuser['tenant'] = {'name':tenant.name, 'id':tenant.id}        
        newuser['user'] = {'name':user.name, 'id':user.id}
        newuser['role'] = {'name':role.name, 'id':role.id}

        # newuser['endpoint'] = endpoint

        return newuser
    else:
        logging.debug('Unknown error when create keystone user and relation')
        temp_delete_user(user)
        logging.debug('== after admin.users.delete(user)!')
        raise KeystoneUserCreateException


def temp_add_user_role(user, role, tenant):
    """
    temporay used, thanks to the Unknown bug of keystoneclient
    """
    logging.debug('user.name:{}, role.name:{}, tenant.name{}:'.format(
        user.name, role.name, tenant.name))
    curlstr = 'curl -g -i -X PUT %s/tenants/%s/users/%s/roles/OS-KSADM/%s \
    -H "User-Agent: python-keystoneclient" \
    -H "Accept: application/json" \
    -H "X-Auth-Token: %s"' % (
        conf.endpoint_url_v2, tenant.id, user.id, role.id, conf.admin_token)
    stat = commands.getoutput(curlstr)
    logging.debug('temp_add_user_role stat:%s, curlstr:%s' % (stat, curlstr))


def temp_delete_user(user):
    """
    temporay used, thanks to the Unknown bug of keystoneclient
    """
    curlstr = 'curl -g -i -X DELETE %s/users/%s \
    -H "User-Agent: python-keystoneclient" \
    -H "Accept: application/json" \
    -H "X-Auth-Token: %s"' % (
        conf.endpoint_url_v2, user.id, conf.admin_token)
    stat = commands.getoutput(curlstr)
    logging.debug('temp_delete_user stat:%s' % stat)


def temp_remove_user_role(user, role, tenant):
    """
    temporay used, thanks to the Unknown bug of keystoneclient
    """
    curlstr = 'curl -g -i -X DELETE %s/tenants/%s/users/%s/roles/OS-KSADM/%s \
    -H "User-Agent: python-keystoneclient" \
    -H "Accept: application/json" \
    -H "X-Auth-Token: %s"' % (
        conf.endpoint_url_v2, tenant.id, user.id, role.id, conf.admin_token)
    stat = commands.getoutput(curlstr)
    logging.debug('temp_remove_user_role stat:%s' % stat)


def create_service(service_name='swift', service_type='object-store', 
    description='Swift service'):
    """
    create service for init 
    """
    # create tenant, user, role, endpoint
    admin = client.Client(token=conf.admin_token,
                            endpoint=conf.endpoint_url_v2, debug=True)

    services = admin.services.list()
    # logging.debug('services:%s' % services)
    # logging.debug('services:%s' % [t.name for t in services])
    # servicenames = [x.name for x in services]
    servicenames = [x.name.lower() for x in services]

    if service_name not in servicenames:       
        service = admin.services.create(name=service_name, 
            service_type=service_type,
            description=description)
        services = admin.services.list()
        logging.debug('services:%s' % services)
        # logging.debug('=======services:%s' % [t.name for t in services])
        # service = [x for x in services if x.name==conf.swift_service][0]
        # logging.debug('service:%s' % service)
        # endpoints = admin.endpoints.list()
        # logging.debug('endpoints:%s' % endpoints[0])
        # admin.services.create(service_name, service_type, description)
        # admin.endpoints.create(
        #      region=conf.swift_region, service_id=service.id,
        #     publicurl="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id,
        #     internalurl="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id,
        #     adminurl="http://10.200.44.66:5000/v2.0")
    else:
        logging.info('service: %s already exists, not need to create.' % 
            service_name)


def create_role(role_name):
    """
    create role for init 
    dupuliate role
    """
    # create tenant, user, role, endpoint
    admin = client.Client(token=conf.admin_token,
                            endpoint=conf.endpoint_url_v2, debug=True)

    roles = admin.roles.list()
    logging.debug('roles:%s' % roles)
    # logging.debug('services:%s' % [t.name for t in services])
    rolenames = [x.name for x in roles]

    if role_name not in rolenames:       
        role = admin.roles.create(name=role_name)
        roles = admin.roles.list()
        logging.debug('roles:%s' % roles)
        # logging.debug('=======services:%s' % [t.name for t in services])
        # service = [x for x in services if x.name==conf.swift_service][0]
        # logging.debug('service:%s' % service)
        # endpoints = admin.endpoints.list()
        # logging.debug('endpoints:%s' % endpoints[0])
        # admin.services.create(service_name, service_type, description)
        # admin.endpoints.create(
        #      region=conf.swift_region, service_id=service.id,
        #     publicurl="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id,
        #     internalurl="http://10.200.44.66:8080/v1/AUTH_%s" % tenant.id,
        #     adminurl="http://10.200.44.66:5000/v2.0")
    else:
        logging.info('role: %s already exists, not need to create.' % 
            role_name)


# createuser(conf.account, 'tester402', 'testing')

# admin = client.Client(token=conf.admin_token,
#                             endpoint=conf.endpoint_url_v2, debug=True)
# services = admin.services.list()
# logging.debug('services:%s' % services)
# # logging.debug('=======services:%s' % [t.name for t in services])
# service = [x for x in services if x.name==conf.swift_service][0]
# admin.endpoints.create(
#              region=conf.swift_region, service_id=service.id,
#             publicurl="http://%s:8080/v1/AUTH_$(tenant_id)s" % 
#                 (conf.auth_host),
#             internalurl="http://%s:8080/v1/AUTH_$(tenant_id)s" % 
#                 (conf.auth_host),
#             adminurl="http://%s:5000/v2.0" % conf.auth_host)