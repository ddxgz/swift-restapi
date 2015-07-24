import sys
import threading
import time
import urllib, urllib2
import requests
from six.moves import http_client
import logging
# import testtools
# from testtools.matchers import Equals, MatchesRegex
import unittest
from wsgiref import simple_server

import swiftclient
import falcon
import falcon.testing as testing

# from restapi import runserver
from verbs import Visit
from config import Config
from utils import pretty_logging
from restapi import app

logging.basicConfig(level=logging.DEBUG,
                format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')


HOST = 'http://127.0.0.1:9803'


def runserver():
    httpd = simple_server.make_server('127.0.0.1', 9803, app)
    httpd.serve_forever()


# class TestWsgi(unittest.TestCase):
class TestAPI:
    """
    This test needs a functional Swift with Keystone, tests the real functions
     of the API.
    """
    def __init__(self):
        self.setUp()
        self.disk_visit = Visit(HOST+'/v1/disk')
        self.acc_visit = Visit(HOST+'/v1/account')
        self.conf = Config()

    def setUp(self):
        thread = threading.Thread(target=runserver)
        thread.daemon = True
        thread.start()

        # # Wait a moment for the thread to start up
        time.sleep(1)


    def run_all(self):
        self.test_put_account()
        self.test_get_home()
        # self.test_put_account()
        # self.test_put_dir()
        # self.test_put_file()
        # # self.test_delete_home()
        # self.test_delete_account()

    def test_get_home(self):
        # runserver()
        # resp = requests.get('http://127.0.0.1:9803/v1/disk')
        headers = { 'username':'tester3838',
                    'password':'testing',
                    'email':'user2@email.com' }
        visit = Visit('http://127.0.0.1:9803/v1/disk')

        visit.get(headers=headers)
        # visit.put(headers=headers, data=urllib.urlencode(data))

        # self.assertEqual(resp.status_code, 200)
        # time.sleep(8)
        # # NOTE(kgriffs): This will cause a different path to
        # # be taken in req._wrap_stream. Have to use httplib
        # # to prevent the invalid header value from being
        # # forced to "0".
        # conn = http_client.HTTPConnection('localhost', 9803)
        # headers = {'Content-Length': 'invalid'}
        # conn.request('PUT', '/', headers=headers)
        # resp = conn.getresponse()
        # self.assertEqual(resp.status, 200)

        # headers = {'Content-Length': '0'}
        # resp = requests.put('http://localhost:9803', headers=headers)
        # self.assertEqual(resp.status_code, 200)

        # resp = requests.post('http://localhost:9803')
        # self.assertEqual(resp.status_code, 405)

    def test_get_dir(self):
        headers = { 'username':'tester3838',
                    'password':'testing',
                    'dir':'fold1' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }

        self.disk_visit.get(headers=headers)

    def test_get_file(self):
        pass

    def test_get_account(self):
        pass

    def test_put_dir(self):
        username = 'tester3838'
        password = 'testing'
        fold1 = 'fold1/'
        headers = { 'username': username,
                    'password': password,
                    'dir':fold1 }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }

        

        self.disk_visit.get(headers=headers)
        # visit.put(headers=headers, data=urllib.urlencode(data))
        self.disk_visit.put(
            suffix_url='/'+fold1, 
            headers=headers,
            data=urllib.urlencode(data))
        self.disk_visit.get(headers=headers)

        conn = swiftclient.Connection(self.conf.auth_url,
                              self.conf.account+':'+username,
                              password,
                              auth_version=self.conf.auth_version)
        meta = conn.head_object(username+'_'+self.conf.disk_container, fold1)
        for key, header in meta.items():
            # pretty_logging({'header':type(header)})
            if 'content-type' == key:
                pretty_logging({'meta':header})
                assert header == 'application/directory'
        # pretty_logging({'typemeta':type(meta)})
        # pretty_logging({'fullemeta':meta})


    def test_put_file(self):
        username = 'tester3838'
        password = 'testing'
        headers = { 'username':'tester3838',
                    'password':'testing',
                    'email':'user2@email.com' }
        visit = Visit('http://127.0.0.1:9803/v1/disk')
        fileobj = '/models.py'

        visit.get(headers=headers)
        # visit.put(headers=headers, data=urllib.urlencode(data))
        visit.put_file(filename='models.py', 
            suffix_url=fileobj, 
            headers=headers)
        visit.get(headers=headers)

        conn = swiftclient.Connection(self.conf.auth_url,
                              self.conf.account+':'+username,
                              password,
                              auth_version=self.conf.auth_version)
        meta, objects = conn.get_container(username+'_'+self.conf.disk_container)
        for obj in objects:
            pretty_logging({'obj':obj})
            if obj.get('name') == fileobj.lstrip('/'):
                assert 1 == 1
                return
        assert 1 == 0

    def test_delete_file(self):
        pass

    def test_put_account(self):
        headers = { 'username':'tester3838',
                    'password':'testing',
                    'email':'user2@email.com' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }
        # visit = Visit('http://10.200.44.84:8090/v1/account')
        visit = Visit('http://127.0.0.1:9803/v1/account')

        # visit.get(headers=headers)
        visit.put(headers=headers, data=urllib.urlencode(data))
        visit.get(headers=headers)

    def test_delete_account(self):
        headers = { 'username':'tester_for_delete8',
                    'password':'testing',
                    'email':'user2@email.com' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }
        # visit = Visit('http://10.200.44.84:8090/v1/account')
        visit = Visit('http://127.0.0.1:9803/v1/account')
        logging.debug('before put')

        visit.put(headers=headers, data=urllib.urlencode(data))
        # visit.get(headers=headers)
        visit.delete(headers=headers, data=urllib.urlencode(data))
        # visit.get(headers=headers)

    def test_delete_home(self):
        headers = { 'username':'tester3838',
                    'password':'testing',
                    'email':'user2@email.com' }

        # visit = Visit('http://10.200.44.84:8090/v1/account')
        visit = Visit('http://127.0.0.1:9803/v1/disk')

        # visit.get(headers=headers)
        visit.delete(headers=headers)


if __name__ == '__main__':
    # runserver()
    # unittest.main()
    t=TestAPI()
    # t.test_get_home()
    t.run_all()


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