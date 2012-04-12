from django import template
from django.http import HttpRequest
from django.contrib.auth.models import User, AnonymousUser
from ..settings import *
from ..ratehandlers import ratehandler

register = template.Library()

class KRateNode(template.Node):
    def __init__(self, obj, **kwargs):
        self.obj = template.Variable(obj)
        self.kwargs = kwargs

    def render(self, context):
        obj = self.obj.resolve(context)
        value = ratehandler.get_object_rate(obj, **self.kwargs)
        if value == None:
            return self.kwargs.get('default', '')
        else:
            return value

def do_krate(parser, token):
    splited = token.split_contents()
    if len(splited) == 1:
        raise template.TemplateSyntaxError("krate tag requires one or more arguments")
    else:
        obj = splited[1]
        tail = splited[2:]

    kwargs = {}
    for pair in tail:
        splited_pair = pair.split("=")
        if len(splited_pair) != 2:
            raise template.TemplateSyntaxError("krate tag kwargs must be key=value format")
        kwargs[splited_pair[0]] = splited_pair[1]

    return KRateNode(obj, **kwargs)

class MyKRateNode(template.Node):
    def __init__(self, obj, request_or_user, **kwargs):
        self.obj = template.Variable(obj)
        self.request_or_user = template.Variable(request_or_user)
        self.kwargs = kwargs

    def render(self, context):
        obj = self.obj.resolve(context)
        request_or_user = self.request_or_user.resolve(context)

        if isinstance(request_or_user, HttpRequest):
            value = ratehandler.get_request_object_rate(request_or_user, obj, **self.kwargs)
        elif isinstance(request_or_user, User):
            value = ratehandler.get_user_object_rate(request_or_user, obj, **self.kwargs)
        elif isinstance(request_or_user, AnonymousUser):
            raise template.TemplateSyntaxError("mykrate second argument can't be the anonymous user")
        else:
            raise template.TemplateSyntaxError("mykrate second argument must be an resquest or user")

        if value == None:
            return self.kwargs.get('default', None)
        else:
            return value


def do_mykrate(parser, token):
    splited = token.split_contents()
    if len(splited) < 3:
        raise template.TemplateSyntaxError("mykrate tag requires two or more arguments")
    else:
        obj = splited[1]
        request_or_user = splited[2]
        tail = splited[3:]

    kwargs = {}
    for pair in tail:
        splited_pair = pair.split("=")
        if len(splited_pair) != 2:
            raise template.TemplateSyntaxError("mykrate tag kwargs must be key=value format")
        kwargs[splited_pair[0]] = splited_pair[1]

    return MyKRateNode(obj, request_or_user, **kwargs)

register.tag('krate', do_krate)
register.tag('mykrate', do_mykrate)
