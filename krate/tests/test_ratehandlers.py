import unittest
from django.http import HttpRequest
from django.test.utils import override_settings
from krate.ratehandlers.noratehandler import NoRateHandler
from krate.ratehandlers.dbratehandler import DBRateHandler
from krate.ratehandlers.dbratehandler.models import *
from django.contrib.auth.models import User
from .models import TestModel, TestModel2

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
        self.assertEqual(self.handler.rate_object(self.request, self.test1, 10), None)

    def test_get_object_rate(self):
        self.assertEqual(self.handler.get_object_rate(self.request, self.test1), 0)

    def test_get_request_object_rate(self):
        self.assertEqual(self.handler.get_object_rate(self.request, self.test1), 0)

    def test_get_user_object_rate(self):
        self.assertEqual(self.handler.get_object_rate(self.request.user, self.test1), 0)

class DBRateHandlerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_rate_object(self):
        pass

    def test_get_object_rate(self):
        pass

    def test_get_request_object_rate(self):
        pass

    def test_get_user_object_rate(self):
        pass
