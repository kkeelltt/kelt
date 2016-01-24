#!/user/bin/python
# -*- coding: utf-8 -*-

from bottle import route, post, run, template, request
from socket import gethostname
from datetime import datetime

SmtpServer = "mail.club.kyutech.ac.jp"
DestAddress = "admin-sys@club.kyutech.ac.jp"
FromAddress = "entry@club.kyutech.ac.jp"


# localhost:8080
@route('/')
def title():
    #Call views/title.tpl
    return template('title')


# localhost:8080/show
@post('/show')
def show():
    # hogeeeeeeee
    name_last = request.forms.name_last
    name_first = request.forms.name_first
    kana_last = request.forms.kana_last
    kana_first = request.forms.kana_first
    student_id = request.forms.student_id
    isc_account = request.forms.isc_account
    club_account = request.forms.club_account
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    hostname = gethostname()
    remote_addr = request.remote_addr

    # Call views/show.tpl
    return template('show',
        name_last = name_last,
        name_first = name_first,
        kana_last = kana_last,
        kana_first = kana_first,
        student_id = student_id,
        isc_account = isc_account,
        club_account = club_account,
        time = time,
        hostname = hostname,
        remote_addr = remote_addr)


# localhost:8080/mail
@route('/mail')
def mail():
    # Call views/mail.tpl
    return template('mail', isc_account = isc_account)


# Launch build in server
run(host='localhost', port=8080, debug=True, reloader=True)
