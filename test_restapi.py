import mock
import random

import unittest
from django.core.urlresolvers import reverse

import swiftclient
import restapi import HomeListener


class RESTApiTest(unittest.TestCase):
    """ Unit tests for swiftbrowser

    All calls using python-swiftclient.clients are replaced using mock """

    def test_get_home(self):

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'],
                         'http://testserver' + reverse('login'))

        self.assertEqual(resp.context['containers'], [])