#!/user/bin/python
# -*- coding: utf-8 -*-


from socket import gethostbyaddr
from datetime import datetime
from bottle import route, post, run, template, request, app
from beaker.middleware import SessionMiddleware
import pytz
import message
import valid
import database


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 60*60,
    'session.data_dir': './session',
    'session.auto': False
}


# http://:8080/
@route('/')
def index():
    # セッションIDを保存
    session = request.environ.get('beaker.session')
    session.save()
    return template('index', key=session.id)


# index.tplからリンク
@route('/confirm')
@route('/confirm/<key>')
@post('/confirm')
@post('/confirm/<key>')
def confirm(key=None):
    # 不正なアクセスでないかチェック
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    # フォームの内容をすべて取得
    post = {}
    for key, value in request.forms.decode().allitems():
        post[key] = value

    # 入力内容の整合性チェック
    error = []
    if valid.blank(post):
        error.append(valid.state('empty'))

    if not valid.student_id(post['student_id']):
        error.append(valid.state('student_id'))

    if not valid.isc(post['isc_account']):
        error.append(valid.state('isc_account'))

    if not valid.username(post['club_account']):
        error.append(valid.state('username'))

    #if valid.duplicate(post['club_account']):
    #error.append(valid.state('duplicate'))

    if  valid.waiting(post['club_account']):
        error.append(valid.state('waiting'))

    if not valid.password(post['password']):
        error.append(valid.state('password'))

    if not post['password'] == post['reenter']:
        error.append(valid.state('mismatch'))

    if not request.forms.agree == 'agree':
        error.append(valid.state('disagree'))

    # 入力内容に誤りが
    if error:
        # ある: エラーの一覧を表示
        return template('error', error_statement='<br>'.join(error))
    else:
        # ない: セッションに保存
        for key in post:
            if key == 'password':
                session[key] = post[key] + '[shadow]'
            else:
                session[key] = post[key]

        # 申請日時・ホスト名・IPアドレスを取得
        date = datetime.now(pytz.timezone('Asia/Tokyo'))
        session['format_date'] = date.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        session['remote_addr'] = request.remote_addr
        try:
            session['remote_host'] = gethostbyaddr(request.remote_addr)[0]
        except OSError:
            session['remote_host'] = '-----'

        session.save()

        # 申請内容の確認画面を表示
        return template('confirm', key=session.id,
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


# confirm.tplからリンク
@route('/send')
@route('/send/<key>')
def send(key=None):
    # 不正なアクセスでないかチェック
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    # 以下12行コメントアウト
    '''
    # セッションIDを更新して保存
    tmp = {}
    for key in session:
        tmp[key] = session[key]

    session.invalidate()
    for key in tmp:
        session[key] = tmp[key]

    session.save()
    '''

    # ユーザ宛に確認用メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account Request validation'
    for_user = message.write_first(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_user)
    #message.send_msg(from_addr, to_addr, msg, host, 25)
    print(for_user)

    return template('send')


# 確認用メールからリンク
@route('/ask')
@route('/ask/<key>')
def ask(key=None):
    # 不正なアクセスでないかチェック
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    # 承認待ちリストに突っ込む
    database.insert(session)

    # 運用部宛に申請依頼メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account Request Succeeded'
    for_admin = message.write_third(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_admin)
    #message.send_msg(from_addr, to_addr, msg, host, 25)
    print(for_admin)

    # セッションを削除
    session.delete()

    return template('ask')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='', port=8080, debug=True, reloader=True)
