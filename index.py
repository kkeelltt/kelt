#!/user/bin/python
# -*- coding: utf-8 -*-

from bottle import route, run, template, request
from datetime import datetime
from socket import gethostname, gethostbyname


# localhost:8080
@route('/')
def title():
    #Call views/title.tpl
    return template('title')


# localhost:8080/show
@route('/show', method='POST')
def show():
    # Call views/show.tpl
    return template('show',
    name_last = request.forms.name_last,
    name_first = request.forms.name_first,
    ruby_last = request.forms.ruby_last,
    ruby_first = request.forms.ruby_first,
    student_id = request.forms.student_id,
    isc_account = request.forms.isc_account,
    club_account = request.forms.club_account,
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
    hostname = gethostname(),
    ipaddress = gethostbyname(gethostname()))


# localhost:8080/mail
@route('/mail')
def mail():
    # Call views/mail.tpl
    return template('mail')

# Launch build in server
run(host='localhost', port=8080, debug=True, reloader=True)
