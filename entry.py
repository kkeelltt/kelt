#!/user/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from socket import gethostbyaddr

from beaker.middleware import SessionMiddleware
import bottle as btl
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


@btl.route('/')
def index():
    # セッションIDを保存
    session = btl.request.environ.get('beaker.session')
    session.save()
    return btl.template('index', key=session.id)


@btl.route('/confirm')
@btl.route('/confirm/<key>')
@btl.route('/confirm', method='POST')
@btl.route('/confirm/<key>', method='POST')
def confirm(key=None):
    # 不正なアクセスでないかチェック
    session = btl.request.environ.get('beaker.session')
    if not key:
        return btl.template('error', error_statement=valid.state('no_key'))
    if not key == session.id:
        return btl.template('error', error_statement=valid.state('lost_key'))

    # フォームの内容をすべて取得
    data = {}
    for key, value in btl.request.forms.decode().allitems():
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

    if not btl.request.forms.agree == 'agree':
        error_list.append(valid.state('disagree'))

    # 入力内容に誤りが
    if error_list:
        # ある: エラーの一覧を表示
        return btl.template('error', error_list='<br>'.join(error_list))
    else:
        # ない: セッションに保存
        for key in data:
            if key == 'password':
                session[key] = data[key] + '[shadow]'
            else:
                session[key] = data[key]

        # 申請日時・ホスト名・IPアドレスを取得
        date = datetime.now(pytz.timezone('Asia/Tokyo'))
        session['format_date'] = date.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        session['remote_addr'] = btl.request.remote_addr
        try:
            session['remote_host'] = gethostbyaddr(btl.request.remote_addr)[0]
        except OSError:
            session['remote_host'] = '-----'

        session.save()

        # 申請内容の確認画面を表示
        return btl.template(
            'confirm',
            key=session.id,
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


@btl.route('/send')
@btl.route('/send/<key>')
def send(key=None):
    # 不正なアクセスでないかチェック
    session = btl.request.environ.get('beaker.session')
    if not key:
        return btl.template('error', error_statement=valid.state('no_key'))
    if not key == session.id:
        return btl.template('error', error_statement=valid.state('lost_key'))

    # 以下12行コメントアウト
    """
    # セッションIDを更新して保存
    tmp = {}
    for key in session:
        tmp[key] = session[key]

    session.invalidate()
    for key in tmp:
        session[key] = tmp[key]

    session.save()
    """

    # ユーザ宛に確認用メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account btl.request validation'
    for_user = message.write_first(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_user)
    message.send_msg(from_addr, to_addr, msg, host, 25)

    return btl.template('send')


@btl.route('/ask')
@btl.route('/ask/<key>')
def ask(key=None):
    # 不正なアクセスでないかチェック
    session = btl.request.environ.get('beaker.session')
    if not key:
        return btl.template('error', error_statement=valid.state('no_key'))
    if not key == session.id:
        return btl.template('error', error_statement=valid.state('lost_key'))

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

    return btl.template('ask')


if __name__ == '__main__':
    btl.app = SessionMiddleware(btl.app(), session_opts)
    btl.run(app=btl.app, host='', port=8080, debug=True, reloader=True)
