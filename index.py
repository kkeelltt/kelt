#!/user/bin/python
# -*- coding: utf-8 -*-

from bottle import route, post, run, template, request, app
from beaker.middleware import SessionMiddleware
from socket import gethostname
from datetime import datetime


SmtpServer = "mail.club.kyutech.ac.jp"
DestAddress = "admin-sys@club.kyutech.ac.jp"
FromAddress = "entry@club.kyutech.ac.jp"


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

@route('/')
def title():
    return template('title')


@post('/show')
def show():
    s = request.environ.get('beaker.session')
    s['name_last'] = request.forms.name_last
    s['name_first'] = request.forms.name_first
    s['kana_last'] = request.forms.kana_last
    s['kana_first'] = request.forms.kana_first
    s['student_id'] = request.forms.student_id
    s['isc_account'] = request.forms.isc_account
    s['club_account'] = request.forms.club_account
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    hostname = gethostname()
    remote_addr = request.remote_addr
    s.save()

    return template('show',
        name_last = s['name_last'],
        name_first = s['name_first'],
        kana_last = s['kana_last'],
        kana_first = s['kana_first'],
        student_id = s['student_id'],
        isc_account = s['isc_account'],
        club_account = s['club_account'],
        time = time,
        hostname = hostname,
        remote_addr = remote_addr)


@route('/mail')
def mail():
    return template('mail')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)
