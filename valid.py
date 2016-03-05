#!/user/bin/python
# -*- coding: utf-8 -*-

import re
import shlex
import subprocess

import database


def blank(data):
    for key in data:
        if not data[key]:
            return True

    return False


def student_id(student_id):
    return re.match('^[0-9]{8}$', student_id)


def isc_account(isc_account):
    return re.match('^[a-z][0-9]{6}[a-z]$', isc_account)


def club_account(club_account):
    return re.match('^[a-z][a-z0-9]{2,7}$', club_account)


def duplicate(club_account):
    cmd1 = 'ldapsearch uid={0}'.format(club_account)
    cmd2 = 'grep numEntries'

    p1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(cmd2),
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    if p2.communicate()[0]:
        return True
    else:
        return False


def waiting(club_account):
    if database.search(club_account):
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
