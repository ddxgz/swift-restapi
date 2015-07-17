import threading
import time
import logging
import unittest
import ast
import urllib
import urllib2
from wsgiref import simple_server

import swiftclient

from restapi import app
from verbs import Visit
from config import Config
from utils import pretty_logging


logging.basicConfig(
    filename='log_test_integration.log', filemode='w',
    level=logging.DEBUG,
    format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
    datefmt='%d %b %Y %H:%M:%S')


HOST = 'http://127.0.0.1:9803'
ACCOUNT_ENDPOINT = HOST + '/v1/account'
DISK_ENDPOINT = HOST + '/v1/disk'
SUCCESS_STATUS_CODES = [200, 201, 202, 204]


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
        self.conf = Config()
        self.test_account_name1 = 'tester_for_delete_'+str(time.time())[:10]
        self.test_account_pw1 = 'testing'
        self.test_account_name2 = 'tester_for_disk_'+str(time.time())[:10]
        self.test_account_pw2 = 'testing'
        self.dir1 = 'test_dir'+str(time.time())[:10]
        self.file1 = 'test_file'+str(time.time())[:10]
        self.fileobj1 = 'restapi.py'

    def tearDown(self):
        headers = { 'username':self.test_account_name1,
                    'password':self.test_account_pw1,
                    'email':'user2@email.com' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }

        visit = Visit(DISK_ENDPOINT)
        accvisit = Visit(ACCOUNT_ENDPOINT)

        """
        use keystoneclient and swiftclient to clean
        """
        try:
            del_code, resp_del = accvisit.delete(headers=headers, 
                data=urllib.urlencode(data))
            logging.info('resp_del:{}'.format(resp_del))
        except:
            print('no need to clean account')
        try:
            code_del, resp_del = visit.delete(suffix_url='/'+self.dir1, 
                headers=headers)
        except:
            print('no need to clean dir1')
        try:
            code_del, resp_del = visit.delete(suffix_url='/'+self.file1, 
                headers=headers)
        except:
            print('no need to clean file1')


class TestConnection(BaseTestCase):
    """
    test if the connect to swift and keystone is ok
    """
    def runTest(self):
        pass


class TestAccount(BaseTestCase):
    """
    put an account
    delete an account

    TODO: test 40x situations
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
        put_code, resp_put = visit.put(headers=headers, 
            data=urllib.urlencode(data))
        logging.info('put_code:{}, resp_put:{}'.format(put_code, resp_put))
        self.assertIn('username', resp_put)
        self.assertIn(put_code, SUCCESS_STATUS_CODES)
        resp_put = ast.literal_eval(resp_put)
        self.assertEqual(self.test_account_name1, resp_put['username'])
        logging.debug('before get')

        get1_code, resp_get1 = visit.get(headers=headers)
        logging.debug('resp_get1:{}'.format(resp_get1))
        self.assertIn('username', resp_get1)
        self.assertIn('disk_container', resp_get1)
        self.assertEqual(get1_code, 200)
        resp_get1 = ast.literal_eval(resp_get1)
        logging.info('resp_get1:{}'.format(resp_get1))
        self.assertEqual(self.test_account_name1, resp_get1['username'])
        logging.debug('before get assertIn 2')
        self.assertEqual(
            self.test_account_name1 + '_' + self.conf.disk_container, 
            resp_get1['disk_container'])
        logging.debug('before delete')
        # visit.get(headers=headers)

        del_code, resp_del = visit.delete(headers=headers, 
            data=urllib.urlencode(data))
        logging.info('resp_del:{}'.format(resp_del))
        self.assertIn('username', resp_del)
        self.assertIn(del_code, SUCCESS_STATUS_CODES)
        resp_del = ast.literal_eval(resp_del)
        self.assertEqual(self.test_account_name1, resp_del['username'])
        """
        use keystoneclient to test if delete ok
        """


class TestDisk(BaseTestCase):
    """
    test if the GET /disk returns 20x
    test if the PUT /disk with dir ok
    """
    def runTest(self):
        headers = { 'username':self.test_account_name2,
                    'password':self.test_account_pw2,
                    'email':'user2@email.com' }
        data = { 'email': {
                    'from':'password1',
                    'to':'user1@email.com' }
                }
        dir1 = self.dir1
        file1 = self.file1
        fileobj1 = self.fileobj1

        visit = Visit(DISK_ENDPOINT)
        accvisit = Visit(ACCOUNT_ENDPOINT)

        # visit.get(headers=headers)
        put_code, resp_put = accvisit.put(headers=headers, 
            data=urllib.urlencode(data))
        logging.info('put_code:{}, resp_put:{}'.format(put_code, resp_put))
        self.assertIn('username', resp_put)
        self.assertIn(put_code, SUCCESS_STATUS_CODES)
        resp_put = ast.literal_eval(resp_put)
        self.assertEqual(self.test_account_name2, resp_put['username'])

        get1_code, resp_get1 = visit.get(headers=headers)
        logging.debug('resp_get1:{}'.format(resp_get1))
        self.assertIn('meta', resp_get1)
        self.assertIn('objects', resp_get1)
        self.assertIn(get1_code, SUCCESS_STATUS_CODES)
        resp_get1 = ast.literal_eval(resp_get1)
        logging.debug('resp_get1:{}'.format(resp_get1))
        obj_num = int(resp_get1['meta']['x-container-object-count'])

        logging.debug('before get assertIn 2')


        headers_dir = { 'username':self.test_account_name2,
                    'password':self.test_account_pw2,
                    'dir':dir1}
        code_dir, resp_put_dir = visit.put(
                                    suffix_url='/'+dir1, 
                                    headers=headers_dir,
                                    data=urllib.urlencode(data))
        self.assertIn('info', resp_put_dir)
        self.assertIn(dir1, resp_put_dir)
        self.assertIn(code_dir, SUCCESS_STATUS_CODES)
        get2_code, resp_get2 = visit.get(headers=headers)
        logging.debug('resp_get1:{}'.format(resp_get2))
        self.assertIn('meta', resp_get2)
        self.assertIn('objects', resp_get2)
        self.assertIn(get2_code, SUCCESS_STATUS_CODES)
        self.assertIn(dir1.rstrip('/')+'/', resp_get2)
        resp_get2 = ast.literal_eval(resp_get2)
        self.assertEqual(str(obj_num+1), 
            resp_get2['meta']['x-container-object-count'])
        self.assertEqual('application/directory', 
            resp_get2['objects'][dir1.rstrip('/')+'/']['content_type'])

        code_url, resp_put_url = visit.put(
                                    suffix_url='/'+dir1+'/'+file1, 
                                    headers=headers,
                                    data=urllib.urlencode(data))
        self.assertIn(code_url, SUCCESS_STATUS_CODES)
        self.assertIn('auth_token', resp_put_url)
        self.assertIn('storage_url', resp_put_url)
        self.assertIn(dir1+'/'+file1, resp_put_url)
        code_file, resp_put_file = visit.put_file(
                                    filename=fileobj1,
                                    suffix_url='/'+dir1+'/'+file1, 
                                    headers=headers,
                                    data=urllib.urlencode(data))
        self.assertIn(code_file, SUCCESS_STATUS_CODES)
        self.assertIn('content-type', resp_put_file)
        get3_code, resp_get3 = visit.get(headers=headers)
        logging.debug('resp_get3:{}'.format(resp_get3))
        self.assertIn('meta', resp_get3)
        self.assertIn('objects', resp_get3)
        self.assertIn(get3_code, SUCCESS_STATUS_CODES)
        resp_get3 = ast.literal_eval(resp_get3)
        logging.debug('resp_get3:{}'.format(resp_get3))
        self.assertEqual(str(obj_num+2), 
            resp_get3['meta']['x-container-object-count'])
        self.assertNotEqual('application/directory', 
            resp_get3['objects'][dir1+'/'+file1]['content_type'])

        code_del, resp_del = visit.delete(suffix_url='/'+dir1, 
            headers=headers)
        self.assertIn(code_del, SUCCESS_STATUS_CODES)
        time.sleep(3)
        get4_code, resp_get4 = visit.get(headers=headers)
        logging.debug('resp_get4:{}'.format(resp_get4))
        self.assertIn('meta', resp_get4)
        self.assertIn('objects', resp_get4)
        self.assertIn(get4_code, SUCCESS_STATUS_CODES)
        resp_get4 = ast.literal_eval(resp_get4)
        logging.debug('resp_get4:{}'.format(resp_get4))
        self.assertEqual(str(obj_num), 
            resp_get4['meta']['x-container-object-count'])
        self.assertNotIn(dir1, resp_get4)
        self.assertNotIn(file1, resp_get4)
        """
        use swiftclient to test if delete ok
        """

        del_code, resp_del = accvisit.delete(headers=headers, 
            data=urllib.urlencode(data))
        logging.debug('resp_del:{}'.format(resp_del))
        self.assertIn('username', resp_del)
        self.assertIn(del_code, SUCCESS_STATUS_CODES)
        resp_del = ast.literal_eval(resp_del)
        self.assertEqual(self.test_account_name2, resp_del['username'])


if __name__ == '__main__':
    run_server()
    unittest.main()