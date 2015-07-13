import sys
import threading
import time
import urllib, urllib2
import requests
from six.moves import http_client
import logging
from wsgiref import simple_server
# import testtools
# from testtools.matchers import Equals, MatchesRegex
import unittest
import ast

import swiftclient
import falcon
import falcon.testing as testing

from restapi import app
from verbs import Visit
from config import Config
from utils import pretty_logging


logging.basicConfig(level=logging.DEBUG,
                format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')


HOST = 'http://127.0.0.1:9803'
ACCOUNT_ENDPOINT = HOST + '/v1/account'
DISK_ENDPOINT = HOST + '/v1/disk'


def runserver():
    httpd = simple_server.make_server('127.0.0.1', 9803, app)
    httpd.serve_forever()


def run_server():
    thread = threading.Thread(target=runserver)
    thread.daemon = True
    thread.start()
    # # Wait a moment for the thread to start up
    time.sleep(1)


class BaseTestCase(unittest.TestCase):
    tmp_accounts = []
    tmp_dirs = []
    tmp_files = []

    def setUp(self):
        self.tmp_accounts = []
        self.tmp_dirs = []
        self.tmp_files = []
        self.conf = Config()
        self.test_account_name1 = 'tester_for_delete12'
        self.test_account_pw1 = 'testing'

    def tearDown(self):
        headers = { 'username':self.test_account_name1,
                    'password':self.test_account_pw1,
                    'email':'user2@email.com' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }
        # visit = Visit(ACCOUNT_ENDPOINT)

        # visit.delete(headers=headers, data=urllib.urlencode(data))

        # for img in self.tmp_accounts:
        #     try:
        #         self.client.remove_image(img)
        #     except docker.errors.APIError:
        #         pass
        # for container in self.tmp_containers:
        #     try:
        #         self.client.stop(container, timeout=1)
        #         self.client.remove_container(container)
        #     except docker.errors.APIError:
        #         pass
        # for folder in self.tmp_folders:
        #     shutil.rmtree(folder)
        # self.client.close()


class TestAccount(BaseTestCase):
    """
    put an account
    delete an account
    """
    def runTest(self):
        headers = { 'username':self.test_account_name1,
                    'password':self.test_account_pw1,
                    'email':'user2@email.com' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }

        visit = Visit(ACCOUNT_ENDPOINT)

        # visit.get(headers=headers)
        resp_put = visit.put(headers=headers, data=urllib.urlencode(data))
        logging.debug('resp_put:{}'.format(resp_put))
        self.assertIn('username', resp_put)
        resp_put = ast.literal_eval(resp_put)
        self.assertEqual(self.test_account_name1, resp_put['username'])
        logging.debug('before get')

        resp_get1 = visit.get(headers=headers)
        logging.debug('resp_get1:{}'.format(resp_get1))
        self.assertIn('username', resp_get1)
        self.assertIn('disk_container', resp_get1)
        resp_get1 = ast.literal_eval(resp_get1)
        self.assertEqual(self.test_account_name1, resp_get1['username'])
        logging.debug('before get assertIn 2')
        self.assertEqual(
            self.test_account_name1 + '_' + self.conf.disk_container, 
            resp_get1['disk_container'])
        logging.debug('before delete')
        # visit.get(headers=headers)

        resp_del = visit.delete(headers=headers, data=urllib.urlencode(data))
        self.assertIn('username', resp_del)
        resp_del = ast.literal_eval(resp_del)
        self.assertEqual(self.test_account_name1, resp_del['username'])


# class TestDisk(BaseTestCase):
#     """
#     put an account
#     delete an account
#     """
#     def runTest(self):
#         headers = { 'username':self.test_account_name1,
#                     'password':self.test_account_pw1,
#                     'email':'user2@email.com' }
#         data = { 'email': {
#                     'from':'password1',
#                     'to':'user1@email.com' }
#                 }

#         visit = Visit(ACCOUNT_ENDPOINT)

#         # visit.get(headers=headers)
#         resp_put = visit.put(headers=headers, data=urllib.urlencode(data))
#         logging.debug('resp_put:{}'.format(resp_put))
#         self.assertIn('username', resp_put)
#         resp_put = ast.literal_eval(resp_put)
#         self.assertEqual(self.test_account_name1, resp_put['username'])
#         logging.debug('before get')

#         resp_get1 = visit.get(headers=headers)
#         logging.debug('resp_get1:{}'.format(resp_get1))
#         self.assertIn('username', resp_get1)
#         self.assertIn('disk_container', resp_get1)
#         resp_get1 = ast.literal_eval(resp_get1)
#         self.assertEqual(self.test_account_name1, resp_get1['username'])
#         logging.debug('before get assertIn 2')
#         self.assertEqual(
#             self.test_account_name1 + '_' + self.conf.disk_container, 
#             resp_get1['disk_container'])
#         logging.debug('before delete')
#         # visit.get(headers=headers)

#         resp_del = visit.delete(headers=headers, data=urllib.urlencode(data))
#         self.assertIn('username', resp_del)
#         resp_del = ast.literal_eval(resp_del)
#         self.assertEqual(self.test_account_name1, resp_del['username'])


if __name__ == '__main__':
    run_server()
    unittest.main()