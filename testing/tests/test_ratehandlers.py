import unittest

from django.http import HttpRequest
from django.contrib.auth.models import User

from krate.ratehandlers.noratehandler import NoRateHandler
from krate.ratehandlers.dbratehandler import DBRateHandler
from krate.ratehandlers.dbratehandler.models import *

from testing.models import TestModel


class NoRateHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = NoRateHandler()
        self.request = HttpRequest()
        self.request.META = {
            'CONTENT_LENGTH': '',
            'CONTENT_TYPE': 'text/html',
            'HTTP_ACCEPT_ENCODING': 'utf-8',
            'HTTP_ACCEPT_LANGUAGE': 'es',
            'HTTP_HOST': 'testhost',
            'HTTP_REFERER': 'testreferer',
            'HTTP_USER_AGENT': 'test user agent',
            'QUERY_STRING': '/',
            'REMOTE_ADDR': 'testaddress',
            'REMOTE_HOST': 'testhost',
            'REMOTE_USER': 'testuser',
            'REQUEST_METHOD': 'GET',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
        }
        (self.request.user, created) = User.objects.get_or_create(username='testuser')
        self.request.user.save()
        self.test1 = TestModel()
        self.test1.save()

    def test_rate_object(self):
        self.assertEqual(self.handler.rate_object(self.request, self.test1, 10), ('created', 0))

    def test_get_object_rate(self):
        self.assertEqual(self.handler.get_object_rate(self.test1), 0)

    def test_get_request_object_rate(self):
        self.assertEqual(self.handler.get_request_object_rate(self.request, self.test1), 0)

    def test_get_user_object_rate(self):
        self.assertEqual(self.handler.get_user_object_rate(self.request.user, self.test1), 0)


class DBRateHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = DBRateHandler()
        self.request1 = HttpRequest()
        self.request1.META = {
            'CONTENT_LENGTH': '',
            'CONTENT_TYPE': 'text/html',
            'HTTP_ACCEPT_ENCODING': 'utf-8',
            'HTTP_ACCEPT_LANGUAGE': 'es',
            'HTTP_HOST': 'testhost',
            'HTTP_REFERER': 'testreferer',
            'HTTP_USER_AGENT': 'test user agent',
            'QUERY_STRING': '/',
            'REMOTE_ADDR': 'testaddress',
            'REMOTE_HOST': 'testhost',
            'REMOTE_USER': 'testuser',
            'REQUEST_METHOD': 'GET',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
        }
        (self.request1.user, created) = User.objects.get_or_create(username='testuser1')
        self.request1.user.save()

        self.request2 = HttpRequest()
        self.request2.META = {
            'CONTENT_LENGTH': '',
            'CONTENT_TYPE': 'text/html',
            'HTTP_ACCEPT_ENCODING': 'utf-8',
            'HTTP_ACCEPT_LANGUAGE': 'es',
            'HTTP_HOST': 'testhost',
            'HTTP_REFERER': 'testreferer',
            'HTTP_USER_AGENT': 'test user agent',
            'QUERY_STRING': '/',
            'REMOTE_ADDR': 'testaddress',
            'REMOTE_HOST': 'testhost',
            'REMOTE_USER': 'testuser',
            'REQUEST_METHOD': 'GET',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
        }
        (self.request2.user, created) = User.objects.get_or_create(username='testuser2')
        self.request2.user.save()
        self.test1 = TestModel()
        self.test1.save()
        self.test2 = TestModel()
        self.test2.save()

    def test_rate_object(self):
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 10), ('created', 10))
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 5), ('modified', 5))
        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 10), ('created', 7.5))
        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 3), ('modified', 4))

        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 10), ('created', 10))
        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 5), ('modified', 5))
        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 10), ('created', 7.5))
        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 3), ('modified', 4))

    def test_get_object_rate(self):
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 10), ('created', 10))
        self.assertEqual(self.handler.get_object_rate(self.test1), 10)
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 5), ('modified', 5))
        self.assertEqual(self.handler.get_object_rate(self.test1), 5)
        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 10), ('created', 7.5))
        self.assertEqual(self.handler.get_object_rate(self.test1), 7.5)
        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 3), ('modified', 4))
        self.assertEqual(self.handler.get_object_rate(self.test1), 4)

        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 10), ('created', 10))
        self.assertEqual(self.handler.get_object_rate(self.test2), 10)
        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 5), ('modified', 5))
        self.assertEqual(self.handler.get_object_rate(self.test2), 5)
        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 10), ('created', 7.5))
        self.assertEqual(self.handler.get_object_rate(self.test2), 7.5)
        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 3), ('modified', 4))
        self.assertEqual(self.handler.get_object_rate(self.test2), 4)

    def test_get_request_object_rate(self):
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 10), ('created', 10))
        self.assertEqual(self.handler.get_request_object_rate(self.request1, self.test1), 10)
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 5), ('modified', 5))
        self.assertEqual(self.handler.get_request_object_rate(self.request1, self.test1), 5)

        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 10), ('created', 7.5))
        self.assertEqual(self.handler.get_request_object_rate(self.request2, self.test1), 10)
        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 3), ('modified', 4))
        self.assertEqual(self.handler.get_request_object_rate(self.request2, self.test1), 3)

        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 10), ('created', 10))
        self.assertEqual(self.handler.get_request_object_rate(self.request1, self.test2), 10)
        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 5), ('modified', 5))
        self.assertEqual(self.handler.get_request_object_rate(self.request1, self.test2), 5)

        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 10), ('created', 7.5))
        self.assertEqual(self.handler.get_request_object_rate(self.request2, self.test2), 10)
        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 3), ('modified', 4))
        self.assertEqual(self.handler.get_request_object_rate(self.request2, self.test2), 3)

    def test_get_user_object_rate(self):
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 10), ('created', 10))
        self.assertEqual(self.handler.get_user_object_rate(self.request1.user, self.test1), 10)
        self.assertEqual(self.handler.rate_object(self.request1, self.test1, 5), ('modified', 5))
        self.assertEqual(self.handler.get_user_object_rate(self.request1.user, self.test1), 5)

        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 10), ('created', 7.5))
        self.assertEqual(self.handler.get_user_object_rate(self.request2.user, self.test1), 10)
        self.assertEqual(self.handler.rate_object(self.request2, self.test1, 3), ('modified', 4))
        self.assertEqual(self.handler.get_user_object_rate(self.request2.user, self.test1), 3)

        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 10), ('created', 10))
        self.assertEqual(self.handler.get_user_object_rate(self.request1.user, self.test2), 10)
        self.assertEqual(self.handler.rate_object(self.request1, self.test2, 5), ('modified', 5))
        self.assertEqual(self.handler.get_user_object_rate(self.request1.user, self.test2), 5)

        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 10), ('created', 7.5))
        self.assertEqual(self.handler.get_user_object_rate(self.request2.user, self.test2), 10)
        self.assertEqual(self.handler.rate_object(self.request2, self.test2, 3), ('modified', 4))
        self.assertEqual(self.handler.get_user_object_rate(self.request2.user, self.test2), 3)
