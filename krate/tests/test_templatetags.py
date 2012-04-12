import unittest
from django.http import HttpRequest
from django.test.utils import override_settings
from krate.ratehandlers.noratehandler import NoRateHandler
from krate.ratehandlers.dbratehandler import DBRateHandler
from krate.ratehandlers.dbratehandler.models import *
from django.contrib.auth.models import User
from .models import TestModel, TestModel2
from django.template import Template, Context, TemplateSyntaxError

class KRateTemplateTagsTest(unittest.TestCase):
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

        self.handler.rate_object(self.request1, self.test1, 10)
        self.handler.rate_object(self.request2, self.test1, 7)

    def test_krate_tag(self):
        template1 = Template('{% load krate %}{% krate obj %}')
        template2 = Template('{% load krate %}{% krate obj default=No%}')

        rendered = template1.render(Context({ 'obj': self.test1 }))
        self.assertEqual(rendered, "8.5")
        rendered = template1.render(Context({ 'obj': self.test2 }))
        self.assertEqual(rendered, "")
        rendered = template2.render(Context({ 'obj': self.test1 }))
        self.assertEqual(rendered, "8.5")
        rendered = template2.render(Context({ 'obj': self.test2 }))
        self.assertEqual(rendered, "No")


    def test_mykrate_tag(self):
        template1 = Template('{% load krate %}{% mykrate obj request_or_user %}')
        template2 = Template('{% load krate %}{% mykrate obj request_or_user default=No%}')

        with self.assertRaises(TemplateSyntaxError):
            Template('{% load krate %}{% mykrate obj request_or_user =%}')

        with self.assertRaises(TemplateSyntaxError):
            Template('{% load krate %}{% mykrate obj request_or_user parameter %}')

        rendered = template1.render(Context({ 'obj': self.test1, 'request_or_user': self.request1 }))
        self.assertEqual(rendered, "10.0")
        rendered = template1.render(Context({ 'obj': self.test1, 'request_or_user': self.request2 }))
        self.assertEqual(rendered, "7.0")
        rendered = template1.render(Context({ 'obj': self.test2, 'request_or_user': self.request1 }))
        self.assertEqual(rendered, "")
        rendered = template1.render(Context({ 'obj': self.test2, 'request_or_user': self.request2 }))
        self.assertEqual(rendered, "")

        rendered = template2.render(Context({ 'obj': self.test1, 'request_or_user': self.request1 }))
        self.assertEqual(rendered, "10.0")
        rendered = template2.render(Context({ 'obj': self.test1, 'request_or_user': self.request2 }))
        self.assertEqual(rendered, "7.0")
        rendered = template2.render(Context({ 'obj': self.test2, 'request_or_user': self.request1 }))
        self.assertEqual(rendered, "No")
        rendered = template2.render(Context({ 'obj': self.test2, 'request_or_user': self.request2 }))
        self.assertEqual(rendered, "No")

        with self.assertRaises(TemplateSyntaxError):
            rendered = template1.render(Context({ 'obj': self.request1, 'request_or_user': self.test1 }))
