#!/user/bin/python
# -*- coding: utf-8 -*-

import re
import shlex
import subprocess

import database


def blank(post):
    for key in post:
        if not post[key]:
            return True

    return False


def student_id(student_id):
    return re.match('\A[0-9]{8}\Z', student_id)


def isc(isc_account):
    return re.match('\A[a-z][0-9]{6}[a-z]\Z', isc_account)


def username(username):
    return re.match('\A[a-z][a-z0-9]{2,7}\Z', username)


def duplicate(username):
    cmd1 = 'ldapsearch uid={0}'.format(username)
    cmd2 = 'grep numEntries'

    p1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(cmd2),
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    if p2.communicate()[0]:
        return True
    else:
        return False


def waiting(username):
    if database.search(username):
        return True
    else:
        return False


def password(password):
    return (
        re.match('\A[!-~]{16,}\Z', password) or
        re.match("""\A(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])
                    (?=.*[^a-zA-Z0-9])[!-~]{8,}\Z""", password)
        )


def state(error_code):
    return error_cases[error_code]


error_cases = {
    'blank': 'フォームに空欄があります。',
    'student_id': '学生番号が不正です。',
    'isc_account': '情報科学センターアカウントが不正です。',
    'username': '共用計算機アカウントが不正です。',
    'duplicate': 'ご希望のアカウント名は既に使用されています。',
    'waiting': 'ご希望のアカウントでの申請はすでに受け付けられています。',
    'password': 'パスワードが不正です。',
    'mismatch': 'パスワードが一致しません。',
    'disagree': '規約に同意しないとアカウントは申請できません。',
    'no_key': '不正なアクセスを検出しました。',
    'lost_key': 'セッション情報がありません。'
}
