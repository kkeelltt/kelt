#!/user/bin/python
# -*- coding: utf-8 -*-

from bottle import route, template
import re


def isstudent_id(s):
    return re.match('\A[0-9]{8}\Z', s)


def isisc_account(i):
    return re.match('\A[a-z][0-9]{6}[a-z]\Z', i)


def isusername(u):
    return re.match('\A[a-z][a-z0-9]{2,7}\Z', u)


def ispassword(p):
    return (re.match('\A.{16,}\Z', p) or
            re.match('\A(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}\Z', p))


def print_error(error_code):
    print(error_code)
