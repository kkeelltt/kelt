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
    return template('title', key=session.id)


# title.tplからリンク
@route('/show')
@route('/show/<key>')
@post('/show')
@post('/show/<key>')
def show(key=None):
    # 不正なアクセスじゃないかをチェック
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
        # ある: エラーの一覧を表示
        return template('error', error_statement='<br>'.join(error))
    else:
        # ない: セッションIDを更新し、セッションに保存
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
        return template('show', key=session.id,
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


# show.tplからリンク
@route('/mail')
@route('/mail/<key>')
def mail(key=None):
    # 不正なアクセスじゃないかをチェック
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    # セッションIDを更新
    tmp = {}
    for key in session:
        tmp[key] = session[key]

    session.invalidate()
    for key in tmp:
        session[key] = tmp[key]

    session.save()

    # ユーザ宛に確認用メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account Request validation'
    for_user = message.write_first(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_user)
    message.send_msg(from_addr, to_addr, msg, host, 25)
    print(for_user)
    return template('mail')


# 確認用メールからリンク
@route('/ask')
@route('/ask/<key>')
def ask(key=None):
    # 不正なアクセスじゃないかをチェック
    session = request.environ.get('beaker.session')
    if not key:
        return template('error', error_statement=valid.state('access'))
    if not key == session.id:
        return template('error', error_statement=valid.state('lost_key'))

    # 承認待ちリストに突っ込む
    database.insert(session)

    # ユーザ宛に申請完了メールを送信
    host = 'mail.club.kyutech.ac.jp'
    from_addr = 'kelt@club.kyutech.ac.jp'
    to_addr = 'lan2014@club.kyutech.ac.jp'
    subject = 'Account Request Succeeded'
    for_user = message.write_second(session)
    msg = message.create_msg(from_addr, to_addr, 'utf-8', subject, for_user)
    message.send_msg(from_addr, to_addr, msg, host, 25)
    print(for_user)

    session.delete()

    return template('ask')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='', port=8080, debug=True, reloader=True)
