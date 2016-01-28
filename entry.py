#!/user/bin/python
# -*- coding: utf-8 -*-


from bottle import route, run, template, request, app
from beaker.middleware import SessionMiddleware
from socket import gethostbyaddr, herror
from datetime import datetime
from pytz import timezone
import message
import valid


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}


@route('/')
def index():
    return template('title')


@route('/show', method='POST')
def confirm():
    post = {}
    error = []
    for key, value in request.forms.decode().allitems():
        post[key] = value

    if valid.isempty(post):
        error.append(valid.state('empty'))

    if not valid.isid(post['student_id']):
        error.append(valid.state('id'))

    if not valid.isisc(post['isc_account']):
        error.append(valid.state('isc'))

    if not valid.isuser(post['club_account']):
        error.append(valid.state('user'))

    if valid.isduplicate(post['club_account']):
        error.append(valid.state('duplicate'))

    if  valid.iswaiting(post['club_account']):
        error.append(valid.state('waiting'))

    if not valid.ispassword(post['password']):
        error.append(valid.state('password'))

    if not valid.isequal(post['password'], post['reenter']):
        error.append(valid.state('mismatch'))

    session = request.environ.get('beaker.session')
    for key in post:
        if key == "password":
            session[key] = post[key] + "[shadow]"
        else:
            session[key] = post[key]

    time = datetime.now(timezone('Asia/Tokyo'))
    remote_addr = request.remote_addr

    try:
        remote_host = gethostbyaddr(remote_addr)[0]
    except herror:
        remote_host = "-----"

    if len(error) > 0:
        return template('error', error_statement='<br>'.join(error))
    else:
        return template('show',
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


@route('/mail')
def send():
    session = request.environ.get('beaker.session')
    session.save()

    time = datetime.now(timezone('Asia/Tokyo'))
    remote_addr = request.remote_addr

    try:
        remote_host = gethostbyaddr(remote_addr)[0]
    except herror:
        remote_host = "-----"

    from_addr = "kelt@club.kyutech.ac.jp"
    to_addr = "lan2014@club.kyutech.ac.jp"
    subject = "Account Request validation"
    body = message.write_first(session, time, remote_host, remote_addr)
    msg = message.create_msg(FROM_ADDR, to_addr, 'utf-8', subject, body)

    SMTP_SERVER = "mail.club.kyutech.ac.jp"
    message.send_msg(FROM_ADDR, to_addr, msg, SMTP_SERVER, 25)

    return template('mail')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='', port=8080, debug=True, reloader=True)
