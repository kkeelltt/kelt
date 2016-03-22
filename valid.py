#!/user/bin/python
# -*- coding: utf-8 -*-

import re

import bottle

import database
import ldap

error_cases = {
    'blank': 'フォームに空欄があります。',
    'student_id': '学生番号が不正です。',
    'isc_account': '情報科学センターアカウントが不正です。',
    'club_account': '共用計算機アカウントが不正です。',
    'duplicate': 'ご希望のアカウント名は既に使用されています。',
    'waiting': 'ご希望のアカウントでの申請はすでに受け付けられています。',
    'password': 'パスワードが不正です。',
    'mismatch': 'パスワードが一致しません。',
    'disagree': '規約に同意しないとアカウントは申請できません。',
    'lost_key': '不正なアクセスを検出しました。',
}


def validation(data):
    error_list = list()
    if blank(data):
        error_list.append(state('blank'))

    if not student_id(data['student_id']):
        error_list.append(state('student_id'))

    if not isc_account(data['isc_account']):
        error_list.append(state('isc_account'))

    if not club_account(data['club_account']):
        error_list.append(state('club_account'))

    # if duplicate(data['club_account']):
    #    error_list.append(state('duplicate'))

    if waiting(data['club_account']):
        error_list.append(state('waiting'))

    if not password(data['password']):
        error_list.append(state('password'))
    else:
        if not data['password'] == data['password_retype']:
            error_list.append(state('mismatch'))

    if not bottle.request.forms.get('agree') == 'agree':
        error_list.append(state('disagree'))

    return error_list


def blank(data):
    for key in data:
        if not data[key]:
            return True
    else:
        return False


def student_id(student_id):
    return re.match('^[0-9]{8}$', student_id)


def isc_account(isc_account):
    return re.match('^[a-z][0-9]{6}[a-z]$', isc_account)


def club_account(club_account):
    return re.match('^[a-z][a-z0-9]{2,7}$', club_account)


def duplicate(club_account):
    if ldap.ldapsearch(club_account):
        return True
    else:
        return False


def waiting(club_account):
    if database.select(club_account):
        return True
    else:
        return False


def password(password):
    ptn1 = '^[!-~]{16,}$'
    ptn2 = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9])[!-~]{8,}$'
    return (re.match(ptn1, password) or
            re.match(ptn2, password))


def state(error_code):
    return error_cases[error_code]
