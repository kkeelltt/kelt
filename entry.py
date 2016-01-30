#!/user/bin/python
# -*- coding: utf-8 -*-


from socket import gethostbyaddr, herror
from datetime import datetime
from bottle import route, post, run, template, request, app
from beaker.middleware import SessionMiddleware
import pytz
import message
import valid


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 60*60,
    'session.data_dir': './session',
    'session.auto': False
}


# http://:8080/ にアクセスされると実行
@route('/')
def index():
    # セッションIDを保存
    session = request.environ.get('beaker.session')
    session.save()
    return template('title', key=session.id)


# title.tplからリンク
@route('/show')
@route('/show/<key>')
@post('/show')
@post('/show/<key>')
def show(key=None):
    # 不正なアクセスでないかどうかを調べる
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
    if valid.isempty(post):
        error.append(valid.state('empty'))
    if not valid.isid(post['student_id']):
        error.append(valid.state('student_id'))
    if not valid.isisc(post['isc_account']):
        error.append(valid.state('isc_account'))
    if not valid.isusername(post['club_account']):
        error.append(valid.state('username'))
    if valid.isduplicate(post['club_account']):
        error.append(valid.state('duplicate'))
    if  valid.iswaiting(post['club_account']):
        error.append(valid.state('waiting'))
    if not valid.ispassword(post['password']):
        error.append(valid.state('password'))
    if not post['password'] == post['reenter']:
        error.append(valid.state('mismatch'))
    if not request.forms.agree == 'agree':
        error.append(valid.state('disagree'))

    # 入力内容に誤りが
    if error:
        # ある: エラーを出力
        return template('error', error_statement='<br>'.join(error))
    else:
        # ない: セッションIDを更新し、セッションに保存
        session.invalidate()
        for key in post:
            session[key] = post[key]

        session.save()

        # 申請日時・ホスト名・IPアドレスを取得
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        remote_addr = request.remote_addr
        try:
            remote_host = gethostbyaddr(remote_addr)[0]
        except herror:
            remote_host = '-----'

        # 申請内容の確認画面を出力
        return template('show', key=session.id,
            name_last=session['name_last'],
            name_first=session['name_first'],
            kana_last=session['kana_last'],
            kana_first=session['kana_first'],
            student_id=session['student_id'],
            isc_account=session['isc_account'],
            club_account=session['club_account'],
            time=time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            remote_host=remote_host,
            remote_addr=remote_addr
        )


# show.tplからリンク
@route('/mail')
@route('/mail/<key>')
def mail(key=None):
    # 不正なアクセスでないかどうかを調べる
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    # 申請日時・ホスト名・IPアドレスを取得
    time = datetime.now(pytz.timezone('Asia/Tokyo'))
    remote_addr = request.remote_addr
    try:
        remote_host = gethostbyaddr(remote_addr)[0]
    except herror:
        remote_host = '-----'

    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    charset = 'utf-8'
    subject = 'Account Request validation'
    body = message.write_first(session, time, remote_host, remote_addr)
    msg = message.create_msg(from_addr, to_addr, charset, subject, body)

    host = 'mail.club.kyutech.ac.jp'
    message.send_msg(from_addr, to_addr, msg, host, 25)

    return template('mail')


# 確認用メールからリンク
@route('/ask')
@route('/ask/<key>')
def ask(key=None):
    # 不正なアクセスでないかどうかを調べる
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE waiting(
            name_last, name_first, kana_last, kana_first,
            student_id, isc_account, club_account
        )'''
    )

    c.execute('INSERT INTO waiting VALUES (?, ?, ?, ?, ?, ?, ?)',
        session['name_last'],
        session['name_first'],
        session['kana_last'],
        session['kana_first'],
        session['student_id'],
        session['isc_account'],
        session['club_account']
    )

    conn.commit()
    conn.close()

    # send mail to user

    # send mail to admin

    session.delete()

    return template('ask')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='', port=8080, debug=True, reloader=True)
