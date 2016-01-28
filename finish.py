#!/user/bin/python
# -*- coding: utf-8 -*-


from bottle import route, run, template, request, app
from beaker.middleware import SessionMiddleware
from socket import gethostbyaddr, herror
from datetime import datetime
from pytz import timezone
import message
import sqlite3


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}


@route('/ask')
def ask():
    key = request.query.key
    if key == '':
        error('no_key')

    try:
        # lost key
    except Error:
        # code

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute(
        """CREATE TABLE waiting(
        name_last,
        name_first,
        kana_last,
        kana_first,
        student_id,
        isc_account,
        club_account)""")

    c.execute("INSERT INTO waiting VALUES (?, ?, ?, ?, ?, ?, ?)",
        session['name_last'],
        session['name_first'],
        session['kana_last'],
        session['kana_first'],
        session['student_id'],
        session['isc_account'],
        session['club_account'])

    conn.commit()
    conn.close()

    # send mail to user and admin

    return template('ask')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)
