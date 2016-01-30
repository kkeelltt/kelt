#!/user/bin/python
# -*- coding: utf-8 -*-


import re


def isempty(post):
    for key in post:
        if not post[key]:
            return True

    return False


def isid(student_id):
    return re.match('\A[0-9]{8}\Z', student_id)


def isisc(isc_account):
    return re.match('\A[a-z][0-9]{6}[a-z]\Z', isc_account)


def isusername(username):
    return re.match('\A[a-z][a-z0-9]{2,7}\Z', username)


def isduplicate(username):
    return False


def iswaiting(username):
    return False


def ispassword(password):
    return (
        re.match('\A[!-~]{16,}\Z', password) or
        re.match('\A(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9])[!-~]{8,}\Z', password)
    )


def isequal(password, reenter):
    return password == reenter


def state(error_code):
    return error_cases[error_code]


error_cases = {
    'empty'      : 'フォームに空欄があります。',
    'student_id' : '学生番号が不正です。',
    'isc_account': '情報科学センターアカウントが不正です。',
    'username'   : '共用計算機アカウントが不正です。',
    'duplicate'  : 'ご希望のアカウント名は既に使用されています。',
    'waiting'    : 'ご希望のアカウントでの申請はすでに受け付けられています。',
    'password'   : 'パスワードが不正です。',
    'mismatch'   : 'パスワードが一致しません。',
    'disagree'   : '規約に同意しないとアカウントは申請できません。',
    'access'     : '不正なアクセスを検出しました。',
    'lost_key'   : 'セッション情報がありません。'
}
