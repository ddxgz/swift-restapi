from __future__ import absolute_import, division, print_function

from wsgiref import simple_server
import falcon
import json
import Queue
import sys, os
import datetime
import logging
import ast

from swiftutils import get_temp_key, get_temp_url

import swiftclient
# from swiftclient import client
import peewee

from config import Config
from models import AccountModel, database
from myexceptions import UserNotExistException, PasswordIncorrectException, \
    KeystoneUserCreateException
import keystonewrap
import swiftwrap
from utils import pretty_logging, list_with_key

logging.basicConfig(format='===========My:%(levelname)s:%(message)s=========', 
    level=logging.DEBUG)
#sys.path.append('.')


class PathListener:
    """
    unuseful at present
    """
    def __init__(self):
        self.conf = Config('swiftconf.conf')

    def on_get(self, req, resp, path, thefile):

        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            logging.debug('username:%s, password:%s' % (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')
        try:
            # if path2file:
            logging.debug('path2file:%s, file:%s' % (path, thefile))
            # logging.debug('self.conf.auth_url: %s,  conf.auth_version: %s' % (
            #     self.conf.auth_url, self.conf.auth_version))
            # conn = swiftclient.Connection(self.conf.auth_url,
            #                       self.conf.account_username,
            #                       self.conf.password,
            #                       auth_version=self.conf.auth_version or 1)
            # meta, objects = conn.get_container(self.conf.container)
            # meta, obj = conn.get_object(self.conf.container, path2file)
            # logging.debug('meta: %s,   obj: %s' % (meta, obj))

            storage_url, auth_token = swiftclient.client.get_auth(
                                    self.conf.auth_url,
                                    self.conf.account_username,
                                  self.conf.password,
                                  auth_version=1)
            # logging.debug('rs: %s'% swiftclient.client.get_auth(
            #                         self.conf.auth_url,
            #                         self.conf.account_username,
            #                       self.conf.password,
            #                       auth_version=1))
            logging.debug('url:%s, toekn:%s' % (storage_url, auth_token))
         
            temp_url = get_temp_url(storage_url, auth_token,
                                          self.conf.disk_container, path2file)
            resp_dict = {}
            # resp_dict['meta'] = meta
            # objs = {}
            # for obj in objects:
            #     logging.debug('obj:%s' % obj.get('name'))
            #     objs[obj.get('name')] = obj
            resp_dict['temp_url'] = temp_url
            logging.debug('resp_dict:%s' % resp_dict)

        except:
            raise falcon.HTTPBadRequest('bad req', 
                'username or password not correct!')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(resp_dict, encoding='utf-8', 
            sort_keys=True, indent=4)
        resp.body = temp_url
        # resp.stream = obj
        # resp.head = meta


class HomeListener:
    def __init__(self):
        self.conf = Config('swiftconf.conf')

    def on_get(self, req, resp):
        """
        :param req.header.username: the username, should be tenant:user when dev
        :param req.header.password: password 

        :returns: a json contains all objects in disk container, and metameata
                {"meta":{}, "objects":{"obj1": {}}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            logging.debug('username:%s, password:%s' % (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')
        try:
            logging.debug('self.conf.auth_url: %s,  conf.auth_version: %s' % (
                self.conf.auth_url, self.conf.auth_version))
            # user = AccountModel.get(AccountModel.username==username, 
            #                             AccountModel.password==password)
            user = AccountModel.auth(username, password)
            # logging.debug('1st resp_dict:%s' % resp_dict)

            resp_dict['info'] = 'successfully get user:%s' % username
            resp_dict['username'] = user.username
            resp_dict['email'] = user.email
            resp_dict['account_level'] = user.account_level
            resp_dict['join_date'] = user.join_date
            resp_dict['keystone_info'] = user.keystone_info
            logging.debug('1st resp_dict:%s' % resp_dict)
            conn = swiftclient.Connection(self.conf.auth_url,
                                  user.keystone_tenant+':'+user.keystone_username,
                                  user.password,
                                  auth_version=self.conf.auth_version)
            meta, objects = conn.get_container(user.disk_container)
            logging.debug('meta: %s,   objects: %s' % (meta, objects))
            resp_dict = {}
            resp_dict['meta'] = meta
            logging.debug('resp_dict:%s' % resp_dict)
            objs = {}
            for obj in objects:
                logging.debug('obj:%s' % obj.get('name'))
                objs[obj.get('name')] = obj
            resp_dict['objects'] = objs        
        except UserNotExistException:
            logging.debug('in UserNotExistException')

            resp_dict['info'] = 'user:%s does not exist' % username
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        except PasswordIncorrectException:
            logging.debug('in PasswordIncorrectException')
            resp_dict['info'] = 'user:%s password not correct' % username
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(resp_dict, encoding='utf-8', 
            sort_keys=True, indent=4)

    def on_post(self, req, resp):
        """
        :param req.header.username: the username, should be tenant:user when dev
        :param req.header.password: password 

        :returns: a json contains the successfully changed files
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            logging.debug('in home post, username:%s, password:%s' % (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')
        try:
            # logging.debug('env:%s , \nstream:%s, \ncontext:%s, \ninput:%s, \n\
            #     params: %s ' % (
            #     req.env, req.stream.read(), req.context, 
            #     req.env['wsgi.input'], req.params.get))
     
            logging.debug('self.conf.auth_url: %s,  conf.auth_version: %s' % (
                self.conf.auth_url, self.conf.auth_version))

            update_list = ast.literal_eval(req.params.get('disk'))
            pretty_logging({'update_list':update_list})
            move_list = []
            copy_list = []
            move_list = list_with_key(update_list, 'move')
            copy_list = list_with_key(update_list, 'copy')
   
            # if len(update_list) > 0:
            #     for pair in update_list:
            #         # pretty_logging(pair)
            #         pretty_logging(move_list, 'movelist')
            #         pretty_logging(copy_list, 'copylist')
            # else:
            #     pretty_logging({}, 'no files in update_list!')

            user = AccountModel.auth(username, password)
            pretty_logging({'tenent:':user.keystone_tenant,
                'username':user.username,
                'disk_container':user.disk_container})
            if len(move_list) > 0:
                for pair in move_list:
                    # pretty_logging(pair)
                    pretty_logging(pair, 'movelist')
                    swiftwrap.move_object(user.keystone_tenant,
                                    user.keystone_username,
                                    user.password,
                                    user.disk_container,
                                    pair.get('from'),
                                    pair.get('move'))
            else:
                pretty_logging({}, 'no files in update_list!')


            if len(copy_list) > 0:
                for pair in copy_list:
                    # pretty_logging(pair)
                    pretty_logging(pair, 'copylist')
                    swiftwrap.copy_object(user.keystone_tenant,
                                    user.keystone_username,
                                    user.password,
                                    user.disk_container,
                                    pair.get('from'),
                                    pair.get('copy'))
            else:
                pretty_logging({}, 'no files in update_list!')

            # user = AccountModel.get(AccountModel.username==username, 
            #                             AccountModel.password==password)
            logging.debug('1st resp_dict:%s' % resp_dict)

            resp_dict['info'] = 'successfully get user:%s' % username
            resp_dict['username'] = user.username
            resp_dict['email'] = user.email
            resp_dict['account_level'] = user.account_level
            resp_dict['join_date'] = user.join_date
            resp_dict['keystone_info'] = user.keystone_info
            logging.debug('2nd resp_dict:%s' % resp_dict)
     
        except UserNotExistException:
            logging.debug('in UserNotExistException')

            resp_dict['info'] = 'user:%s does not exist' % username
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        except PasswordIncorrectException:
            logging.debug('in PasswordIncorrectException')
            resp_dict['info'] = 'user:%s password not correct' % username
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(resp_dict, encoding='utf-8', 
            sort_keys=True, indent=4)

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_405
        resp.body = json.dumps({'info':'Delete home is not implemented yet!'}, 
            encoding='utf-8', 
            sort_keys=True, indent=4)


class DiskSinkAdapter(object):
    conf = Config('swiftconf.conf')

    def __call__(self, req, resp, path2file):
        """
        :param req.header.username: the username, should be tenant:user when dev
        :param req.header.password: password 
        :path2file the part in the request url /v1/disk/(?P<path2file>.+?), to 
            identify the resource to manipulate 

        :returns: a json contains correspond response info
            GET: the temp_url of the file in a resp dict
            PUT: the auth_token and storage_url in a resp dict for uploading file
            DELETE: description of if the operation success or fail
        """
        logging.debug('in sink req.method:%s  path2file:%s' % (
            req.method, path2file))
        resp_dict = {}

        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            req_dir = req.get_header('dir') or None
            logging.debug('username:%s, password:%s' % (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')

        if req.method == 'GET':
            try:
                user = AccountModel.auth(username, password)
                os_options = {'tenant_name':user.keystone_tenant}

                storage_url, auth_token = swiftclient.client.get_auth(
                                        self.conf.auth_url,
                                  user.keystone_tenant+':'+user.keystone_username,
                                  user.password,
                                   os_options=os_options,
                                      auth_version=self.conf.auth_version)
                logging.debug('url:%s, toekn:%s' % (storage_url, auth_token))
                # if path2file[-1] is '/':
                if req_dir:
                    meta, objects = conn.get_container(user.disk_container,
                        delimiter='/',
                        prefix=req_dir)
                    logging.debug('meta: %s,   objects: %s' % (meta, objects))
                    resp_dict['meta'] = meta
                    logging.debug('resp_dict:%s' % resp_dict)
                    objs = {}
                    for obj in objects:
                        logging.debug('obj:%s' % obj.get('name'))
                        objs[obj.get('name')] = obj
                    resp_dict['objects'] = objs
                else:
                    temp_url = get_temp_url(storage_url, auth_token,
                                                  user.disk_container, path2file)
                    resp_dict = {}
                    # resp_dict['meta'] = meta
                    resp_dict['temp_url'] = temp_url
                    resp_dict['path2file'] = path2file
                resp.status = falcon.HTTP_200
                # logging.debug('resp_dict:%s' % resp_dict)
            except:
                raise falcon.HTTPBadRequest('bad req', 
                    'username or password not correct!')

        elif req.method == 'PUT':
            try:
                # if path2file:
                logging.debug(' path2file:%s' % (path2file))

                # logging.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
                # req.env, req.stream.read()))

                user = AccountModel.auth(username, password)
                os_options = {'tenant_name':user.keystone_tenant}
                storage_url, auth_token = swiftclient.client.get_auth(
                                        self.conf.auth_url,
                                user.keystone_tenant+':'+user.keystone_username,
                                  user.password,
                                  os_options=os_options,
                                      auth_version=self.conf.auth_version)
                logging.debug('url:%s, toekn:%s, if dir:%s' % 
                    (storage_url, auth_token, req_dir))

                if req_dir:
                    # modify to create multiple dir when req_dir with multiple '/'
                    req_dir = req_dir.rstrip('/')
                    req_dir += '/'
                    
                    content_type = 'application/directory'
                    obj = None

                    swiftclient.client.put_object(storage_url, auth_token,
                              user.disk_container, req_dir, obj,
                              content_type=content_type)

                    resp_dict['info'] = 'successfully create fold:%s' % req_dir
                else:
                    logging.debug('in else')

                    logging.debug('url:%s, token:%s' % (storage_url, auth_token))
                    resp_dict['auth_token'] = auth_token
                    resp_dict['storage_url'] = storage_url + '/' + \
                        user.disk_container + '/' + path2file
                resp.status = falcon.HTTP_201
                logging.debug('resp_dict:%s' % resp_dict)

            except:
                raise falcon.HTTPBadRequest('bad req', 
                    'username or password not correct!')

        elif req.method == 'DELETE':
            resp_dict = {}

            try:
                # if path2file:
                logging.debug(' path2file:%s' % (path2file))
                logging.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
                req.env, req.stream.read()))
                user = AccountModel.auth(username, password)
                conn = swiftclient.client.Connection(self.conf.auth_url,
                                  user.keystone_tenant+':'+user.keystone_username,
                                  user.password,
                                  auth_version=self.conf.auth_version)
                meta, objects = conn.get_container(user.disk_container, 
                    prefix=path2file)
                logging.debug('meta: %s,  \n objects: %s' % (meta, objects))
                if objects:
                    for obj in objects:
                        conn.delete_object(user.disk_container, obj['name'])
                    resp_dict['description'] = 'The files have been deleted'
                else:
                    resp_dict['description'] = 'There is no file to be \
                        deleted'
                resp.status = falcon.HTTP_204
                logging.debug('resp_dict:%s' % resp_dict)

            except:
                raise falcon.HTTPBadRequest('bad req', 
                    'username or password not correct!')
        resp.body = json.dumps(resp_dict, encoding='utf-8', 
            sort_keys=True, indent=4)


class AccountListener:
    def __init__(self):
        self.conf = Config('swiftconf.conf')

    def on_put(self, req, resp):
        """
        :param req.header.username: the username
        :param req.header.password: password 
        :param req.header.email: email 

        :returns: a json contains info of the operation, if the register is
            success or failed
        """
        logging.debug('in account put')
        resp_dict = {}

        try:
            username = req.get_header('username') or ''
            password = req.get_header('password') or ''
            email = req.get_header('email') or 'email'
            # params = req.get_param_as_list()
            # logging.debug('params:%s'%params)
            logging.debug('username:%s, password:%s, email:%s' % 
                (username, password, email))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')
        
        try:
            logging.debug('in account put create')

            with database.atomic():
                # AccountModel.create(username=username, 
                #     password=password,
                #     email=email,
                #     join_date=str(datetime.datetime.now())+' GMT+8',
                #     account_level=0,
                #     swift_tenant='test',
                #     swift_username=username,
                #     swift_password=password)
                new_user = AccountModel.create(username=username, 
                    password=password,
                    email=email,
                    join_date=str(datetime.datetime.now())+' GMT+8',
                    account_level=0,
                    keystone_tenant=self.conf.account,
                    keystone_username=username,
                    keystone_password=password,
                    disk_container=username+'_'+self.conf.disk_container,
                    keystone_info='')
                logging.debug('in account put create database.atomic')

            # conn = swiftclient.client.Connection(self.conf.auth_url,
            #                       self.conf.account_username,
            #                       self.conf.password,
            #                       auth_version=self.conf.auth_version or 1)
            keystone_info = swiftwrap.create_user(new_user.keystone_tenant, 
                new_user.keystone_username,
                new_user.keystone_password, 
                new_user.account_level)
            logging.debug('keystone_info:%s' % keystone_info)
            q = AccountModel.update(keystone_info=keystone_info).where(
                AccountModel.username == username, 
                AccountModel.password == password)
            q.execute()
            resp_dict['info'] = 'successfully create user:%s' % username
            resp.status = falcon.HTTP_201
        except KeystoneUserCreateException:
            logging.debug('==in restapi KeystoneUserCreateException!')
            q = AccountModel.delete().where(AccountModel.username==username, 
                    AccountModel.password==password)
            q.execute()
            resp_dict['info'] = 'create user failed, did not create user:%s' % username
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        except peewee.IntegrityError:
            logging.debug('in account put create except')

            # `username` is a unique column, so this username already exists,
            # making it safe to call .get().
            old_user = AccountModel.get(AccountModel.username == username)
            logging.debug('user exists...')
            resp_dict['info'] = 'user exists, did not create user:%s' % username
            resp.status = falcon.HTTP_409
            try:
                change_user = AccountModel.get(AccountModel.username==username, 
                                AccountModel.password==password)
            except:
                logging.debug('change user data failed...')
        resp.body = json.dumps(resp_dict, encoding='utf-8')

    def on_get(self, req, resp):
        """
        :returns: info of the user in the req.header
        """
        logging.debug('in account get')
        resp_dict = {}

        try:
            username = req.get_header('username') or ''
            password = req.get_header('password') or ''
            # email = req.get_header('email') or 'email'
            # params = req.get_param_as_list()
            # logging.debug('params:%s'%params)
            logging.debug('username:%s, password:%s' % 
                (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')
        
        try:
            logging.debug('in account model get')

            # user = AccountModel.get(AccountModel.username==username, 
            #                             AccountModel.password==password)
            user = AccountModel.auth(username, password)

            resp_dict['info'] = 'successfully get user:%s' % username
            resp_dict['username'] = user.username
            resp_dict['email'] = user.email
            resp_dict['account_level'] = user.account_level
            resp_dict['join_date'] = user.join_date
            resp_dict['keystone_info'] = user.keystone_info
            resp_dict['disk_container'] = user.disk_container
            resp_dict['auth'] = 1

            # keystone_info = swiftwrap.createuser(new_user.keystone_tenant, 
            #     new_user.keystone_username,
            #     new_user.keystone_password, new_user.account_level)

            resp.status = falcon.HTTP_200
        except UserNotExistException:
            logging.debug('in UserNotExistException')

            resp_dict['info'] = 'user:%s does not exist' % username
            resp_dict['auth'] = 0
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        except PasswordIncorrectException:
            logging.debug('in PasswordIncorrectException')
            resp_dict['info'] = 'user:%s password not correct' % username
            resp_dict['auth'] = 0
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(resp_dict, encoding='utf-8')
        # except:
        #     # `username` is a unique column, so this username already exists,
        #     # making it safe to call .get().
        #     resp_dict['info'] = 'user:%s does not exist or password not right' % username
        #     logging.debug('user does not exist or password not right...')
        #     resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps(resp_dict, encoding='utf-8')


    def on_delete(self, req, resp):
        """
        DEVELOPMENT ONLY!

        Delete the account, and all the files belong to this account
        """
        logging.debug('in account delete')
        resp_dict = {}

        try:
            username = req.get_header('username') or ''
            password = req.get_header('password') or ''
            # email = req.get_header('email') or 'email'
            # params = req.get_param_as_list()
            # logging.debug('params:%s'%params)
            logging.debug('username:%s, password:%s' % 
                (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req', 
                'when read from req, please check if the req is correct.')
        
        try:
            # user = AccountModel.get(AccountModel.username==username, 
            #                             AccountModel.password==password)
            user = AccountModel.auth(username, password)

            conn = swiftclient.client.Connection(self.conf.auth_url,
                            user.keystone_tenant+':'+user.keystone_username,
                                  user.password,
                                  auth_version=self.conf.auth_version)
            # for container in self.conf.services:
            #     conn.delete_container(username+'_'+container)

            keystonewrap.delete_user(user.keystone_tenant, 
                    user.keystone_username,
                    user.keystone_password)
            logging.debug('after delete keytone user')
            q = AccountModel.delete().where(AccountModel.username==username, 
                    AccountModel.password==password)
            q.execute()
            resp_dict['info'] = 'user:%s deleted successfully' % username
            resp.status = falcon.HTTP_200

        except:
            logging.debug('in delete user Exception')
            resp_dict['info'] = 'delete user:%s not successfully' % username
            resp.status = falcon.HTTP_400
        resp.body = json.dumps(resp_dict, encoding='utf-8', 
            sort_keys=True, indent=4)

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