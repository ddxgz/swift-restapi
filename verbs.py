import sys
import os
import ast
import urllib, urllib2
import requests
import commands

import logging

# logging.basicConfig(format='===========%(levelname)s:%(message)s=========', 
#     level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')


class Visit():
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers, 
            data=data)
        req.get_method = lambda: 'PUT'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put_file(self, filename='', suffix_url='', headers=None, data=None):
        code_url, resp_str = self.put(suffix_url=suffix_url, headers=headers)
        resp = ast.literal_eval(resp_str)
        logging.debug('resp:%s' % (resp))
        token = resp.get('auth_token')
        storage_url = resp.get('storage_url')
        headers = {'x-storage-token':token}
        files = {'file': open(filename)}
        put_resp = requests.put(storage_url, files=files, headers=headers)
        page = put_resp.headers
        code = put_resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page


    def post(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, 
            headers=headers, data=data)
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page


    def delete(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers, 
            data=data)
        req.get_method = lambda: 'DELETE'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page



headers = { 'username':'aaa',
            'password':'aaa' }
data = { 'username':'user1',
          'password':'password1',
          'email':'user1@email.com' }

# visit = Visit('http://10.200.43.103:5000/v2.0/tokens')
# visit = Visit('http://10.200.43.176:8888/v1/disk')
visit = Visit('http://10.200.44.84:8888/v1/disk')

# visit.get(headers=headers)


# headers = { 'username':'test:tester',
#             'password':'testing' }
# # data = { 'username':'user1',
# #           'password':'password1',
# #           'email':'user1@email.com' }
# data = { 'username':'user1',
#             'password':'password1',
#             'email':'user1@email.com' }
# visit = Visit('http://10.200.44.84:8080/v1/disk')
# visit = Visit('http://10.200.43.176:8888/v1/disk')
# visit = Visit('http://10.200.44.84:8090/v1/account')

# visit.get(headers=headers)
# visit.put(suffix_url='/curl.py', headers=headers)
# visit.put_file(filename='curl.py', suffix_url='/fold3/curl.py', headers=headers)
# visit.delete(suffix_url='/fold3/curl.py', headers=headers)

# v1 account
# visit.post(headers=headers, data=urllib.urlencode(data))


# v2 disk
headers = { 'username':'testuser7',
            'password':'testing',
            'email':'user2@email.com' }
data = { 'disk': [
                # {
                # 'from':'/fold1/subfold1/models.py',
                # 'move':'/pics/new.png' 
                # },
                {
                'from':'fold1/subfold2/curl.py',
                'copy':'pics/cnew2.conf' 
                },
                # {
                # 'from':'fold1/subfold1/models.py',
                # 'move':'pics2/new2.png' 
                # },
                {
                'from':'fold1/subfold2/curl.py',
                'copy':'pics2/cnew3.conf' 
                },
                {
                'from':'fold1/subfold1/models.py',
                'move':'pics/new.png' 
                },
                {
                'from':'config.py',
                'copy':'pics3/cnew4.conf' 
                }
            ]
        }
# visit = Visit('http://10.200.43.176:8888/v1/disk')
# visit = Visit('http://10.200.44.84:8090/v1/disk')
# visit = Visit('http://127.0.0.1:9803/v1/disk')
# visit.get(headers=headers)
# visit.get(headers=headers, suffix_url='/pics/')
# # # visit.put(suffix_url='/curl.py', headers=headers)
# visit.put_file(filename='models.py', suffix_url='/fold1/subfold1/models.py', headers=headers)
# visit.put_file(filename='curl.py', suffix_url='/fold1/subfold2/curl.py', headers=headers)
# visit.put_file(filename='config.py', suffix_url='/config.py', headers=headers)
# visit.delete(suffix_url='/fold1/curl.py', headers=headers)
# visit.post(headers=headers, data=urllib.urlencode(data))
# visit.get(headers=headers)


# v2 account
headers = { 'username':'tester444456',
            'password':'testing',
            'email':'user2@email.com' }
data = { 'email': {
            'from':'password1',
            'to':'user1@email.com' }
        }
visit = Visit('http://10.200.44.84:8888/v1/account')
# visit = Visit('http://127.0.0.1:9803/v1/account')

# visit.get(headers=headers)
# visit.put(headers=headers, data=urllib.urlencode(data))
# visit.post(headers=headers, data=urllib.urlencode(data))



# headers = { 'Content-Type':'application/json'}
# data = { "auth": 
#           {"passwordCredentials":
#               {"username": "tester", 
#               "password": "testing"},
#               "tenantName":"restapi"
#           }
#       }
# keytonevisit = Visit('http://10.200.44.66:5000/v2.0/tokens')
# # keytonevisit.get(headers=headers)
# keytonevisit.post(headers=headers, data=urllib.urlencode(data))