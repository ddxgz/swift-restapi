import sys
import threading
import time
import urllib, urllib2
import requests
from six.moves import http_client
# import testtools
# from testtools.matchers import Equals, MatchesRegex
import unittest

import falcon
import falcon.testing as testing

from restapi import runserver
from test_verbs import Visit

# runserver()

# class TestWsgi(unittest.TestCase):
class TestAPI:
    def __init__(self):
        self.setUp()

    def setUp(self):
        thread = threading.Thread(target=runserver)
        thread.daemon = True
        thread.start()

        # # Wait a moment for the thread to start up
        time.sleep(1)

    def test_get_home(self):
        # runserver()
        resp = requests.get('http://127.0.0.1:9803/v1/disk')
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

if __name__ == '__main__':
    # runserver()
    # unittest.main()
    t=TestAPI()
    # t.test_get_home()
    t.test_put_account()