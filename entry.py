#!/user/bin/python
# -*- coding: utf-8 -*-

import base64
from datetime import datetime
import hashlib
from socket import gethostbyaddr

from beaker.middleware import SessionMiddleware
import bottle
import pytz

import database
import message
import valid

__version__ = 'Rev.2016030'
SMTP_SVR = 'mail.club.kyutech.ac.jp'
FROM_ADDR = 'kelt@club.kyutech.ac.jp'  # entry@club.kyutech.ac.jp
ADMIN_ADDR = 'lan2014@club.kyutech.ac.jp'  # admin-sys@club.kyutech.ac.jp

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 60 * 60,
    'session.data_dir': './session',
    'session.auto': False
}


@bottle.route('/')
def index():
    # セッションIDを作成
    session = bottle.request.environ.get('beaker.session')
    session.save()
    return bottle.template('index', key=session.id)


@bottle.route('/confirm')
@bottle.route('/confirm/<key>')
@bottle.route('/confirm', method='POST')
@bottle.route('/confirm/<key>', method='POST')
def confirm(key=None):
    session = bottle.request.environ.get('beaker.session')

    # 不正なアクセスでないかチェック
    if not key == session.id:
        return bottle.template('error', error=valid.state('lost_key'))

    # フォームの内容をすべて取得
    data = dict()
    for key, value in bottle.request.forms.decode().allitems():
        data[key] = value

    # 入力内容に誤りがないかどうかチェック
    error = list()
    if valid.blank(data):
        error.append(valid.state('blank'))

    if not valid.student_id(data['student_id']):
        error.append(valid.state('student_id'))

    if not valid.isc_account(data['isc_account']):
        error.append(valid.state('isc_account'))

    if not valid.club_account(data['club_account']):
        error.append(valid.state('club_account'))

    # if valid.duplicate(data['club_account']):
    #    error.append(valid.state('duplicate'))

    if valid.waiting(data['club_account']):
        error.append(valid.state('waiting'))

    if not valid.password(data['password']):
        error.append(valid.state('password'))
    else:
        if not data['password'] == data['password_retype']:
            error.append(valid.state('mismatch'))

    if not bottle.request.forms.agree == 'agree':
        error.append(valid.state('disagree'))

    # 入力内容に誤りがあった場合、誤り内容の一覧を表示
    if error:
        return bottle.template('error', error='<br>'.join(error))

    # パスワードの暗号化
    h = hashlib.sha1()
    h.update(data['password'].encode())
    data['password'] = '{SHA}' + base64.b64encode(h.digest()).decode()

    # 申請日時・ホスト名・IPアドレスを取得
    date = datetime.now(pytz.timezone('Asia/Tokyo'))
    data['format_time'] = date.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    data['remote_addr'] = bottle.request.remote_addr
    try:
        data['remote_host'] = gethostbyaddr(data['remote_addr'])[0]
    except OSError:
        data['remote_host'] = '-----'

    # セッションに保存
    for key in data:
        session[key] = data[key]

    session.save()

    # 申請内容の確認画面を表示
    return bottle.template(
        'confirm',
        key=session.id,
        name_last=session['name_last'],
        name_first=session['name_first'],
        kana_last=session['kana_last'],
        kana_first=session['kana_first'],
        student_id=session['student_id'],
        isc_account=session['isc_account'],
        club_account=session['club_account'],
        format_time=session['format_time'],
        remote_host=session['remote_host'],
        remote_addr=session['remote_addr']
    )


@bottle.route('/send')
@bottle.route('/send/<key>')
def send(key=None):
    session = bottle.request.environ.get('beaker.session')

    # 不正なアクセスでないかチェック
    if not key == session.id:
        return bottle.template('error', error=valid.state('lost_key'))

    # ユーザ宛に確認用メールを送信
    to_addr = 'lan2014@club.kyutech.ac.jp'
    # to_addr = '{isc_account}@mail.kyutech.jp'.format(**session)
    subject = 'Account request validation'
    for_user = message.write_first(session)
    msg = message.create_msg(FROM_ADDR, to_addr, subject, for_user)
    message.send_msg(SMTP_SVR, msg)

    return bottle.template('send')


@bottle.route('/finish')
@bottle.route('/finish/<key>')
def finish(key=None):
    session = bottle.request.environ.get('beaker.session')

    # 不正なアクセスでないかチェック
    if not key == session.id:
        return bottle.template('error', error=valid.state('lost_key'))

    # 承認待ちリストに突っ込む
    database.insert(session)

    # 運用部宛に申請依頼メールを送信
    subject = 'Request for account ({club_account})'.format(**session)
    for_admin = message.write_second(session)
    msg = message.create_msg(FROM_ADDR, ADMIN_ADDR, subject, for_admin)
    message.send_msg(SMTP_SVR, msg)

    # セッションを削除
    session.delete()

    return bottle.template('finish')


if __name__ == '__main__':
    app = SessionMiddleware(bottle.app(), session_opts)
    bottle.run(app=app, host='', port=8080, debug=True, reloader=True)
