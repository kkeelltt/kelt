#!/user/bin/python
# -*- coding: utf-8 -*-


from socket import gethostbyaddr, herror
from datetime import datetime
from bottle import route, post, run, template, request, app
from beaker.middleware import SessionMiddleware
import pytz
import message
import valid
import database


@route('/request')
def request():
    # login

    # sql select

    return template('request')


@route('/finish')
def finish():
    # sql delete

    # ldap insert

    # send mail to user

    # send mail to admin

    return template('finish')
