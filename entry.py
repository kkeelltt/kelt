#!/user/bin/python
# -*- coding: utf-8 -*-

from base64 import b64encode
from datetime import datetime
from hashlib import sha1
from socket import gethostbyaddr

from beaker.middleware import SessionMiddleware
import bottle
import pytz

import database
import message
import valid


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 60 * 60,
    'session.data_dir': './session',
    'session.auto': False
}


@bottle.route('/')
def index():
    # セッションIDを保存
    session = bottle.request.environ.get('beaker.session')
    session.save()
    return bottle.template('index', key=session.id)


@bottle.route('/confirm')
@bottle.route('/confirm/<key>')
@bottle.route('/confirm', method='POST')
@bottle.route('/confirm/<key>', method='POST')
def confirm(key=None):
    # 不正なアクセスでないかチェック
    session = bottle.request.environ.get('beaker.session')
    if not key:
        return bottle.template('error', error_list=valid.state('no_key'))
    if not key == session.id:
        return bottle.template('error', error_list=valid.state('lost_key'))

    # フォームの内容をすべて取得
    data = {}
    for key, value in bottle.request.forms.decode().allitems():
        data[key] = value

    # 入力内容の整合性チェック
    error_list = []
    if valid.blank(data):
        error_list.append(valid.state('blank'))

    if not valid.student_id(data['student_id']):
        error_list.append(valid.state('student_id'))

    if not valid.isc(data['isc_account']):
        error_list.append(valid.state('isc_account'))

    if not valid.username(data['club_account']):
        error_list.append(valid.state('username'))

    if valid.duplicate(data['club_account']):
        error_list.append(valid.state('duplicate'))

    if valid.waiting(data['club_account']):
        error_list.append(valid.state('waiting'))

    if not valid.password(data['password']):
        error_list.append(valid.state('password'))

    if not data['password'] == data['reenter']:
        error_list.append(valid.state('mismatch'))

    if not bottle.request.forms.agree == 'agree':
        error_list.append(valid.state('disagree'))

    # 入力内容に誤りが
    if error_list:
        # ある: エラーの一覧を表示
        return bottle.template('error', error_list='<br>'.join(error_list))
    else:
        # ない: セッションに保存
        for key in data:
            if key == 'password':
                h = sha1()
                h.update(data[key].encode())
                session[key] = '{SHA}' + b64encode(h.digest()).decode()
            else:
                session[key] = data[key]

        # 申請日時・ホスト名・IPアドレスを取得
        date = datetime.now(pytz.timezone('Asia/Tokyo'))
        session['format_date'] = date.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        session['remote_addr'] = bottle.request.remote_addr
        try:
            session['remote_host'] = gethostbyaddr(session['remote_addr'])[0]
        except OSError:
            session['remote_host'] = '-----'

        session.save()

        # 申請内容の確認画面を表示
        return bottle.template(
            'confirm', key=session.id,
            name_last=session['name_last'],
            name_first=session['name_first'],
            kana_last=session['kana_last'],
            kana_first=session['kana_first'],
            student_id=session['student_id'],
            isc_account=session['isc_account'],
            club_account=session['club_account'],
            format_date=session['format_date'],
            remote_host=session['remote_host'],
            remote_addr=session['remote_addr']
        )


@bottle.route('/send')
@bottle.route('/send/<key>')
def send(key=None):
    # 不正なアクセスでないかチェック
    session = bottle.request.environ.get('beaker.session')
    if not key:
        return bottle.template('error', error_list=valid.state('no_key'))
    if not key == session.id:
        return bottle.template('error', error_list=valid.state('lost_key'))

    # ユーザ宛に確認用メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account bottle.request validation'
    for_user = message.write_first(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_user)
    message.send_msg(from_addr, to_addr, msg, host, 25)

    return bottle.template('send')


@bottle.route('/ask')
@bottle.route('/ask/<key>')
def ask(key=None):
    # 不正なアクセスでないかチェック
    session = bottle.request.environ.get('beaker.session')
    if not key:
        return bottle.template('error', error_list=valid.state('no_key'))
    if not key == session.id:
        return bottle.template('error', error_list=valid.state('lost_key'))

    # 承認待ちリストに突っ込む
    database.insert(session)

    # 運用部宛に申請依頼メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account request Succeeded'
    for_admin = message.write_third(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_admin)
    message.send_msg(from_addr, to_addr, msg, host, 25)

    # セッションを削除
    session.delete()

    return bottle.template('ask')


if __name__ == '__main__':
    app = SessionMiddleware(bottle.app(), session_opts)
    bottle.run(app=app, host='', port=8080, debug=True, reloader=True)
