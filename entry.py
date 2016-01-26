#!/user/bin/python
# -*- coding: utf-8 -*-


from bottle import route, run, template, request, app
from beaker.middleware import SessionMiddleware
from socket import gethostname, gethostbyname
from datetime import datetime, timezone
import pytz
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate


ENCODING = "utf-8"
FROM_ADDR = "kelt@club.kyutech.ac.jp"
SMTP_SRV = "mail.club.kyutech.ac.jp"


def create_msg(from_addr, to_addr, charset, subject, body):
    msg = MIMEText(body, 'plain', charset)
    msg['Subject'] = Header(subject,charset)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate(localtime=True)
    return msg

def send_msg(from_addr, to_addr, msg, host, port):
    smtp = smtplib.SMTP(host, port)
    smtp.ehlo()
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.close()


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}


@route('/title')
def title():
    return template('title')


@route('/show', method='POST')
def show():
    session = request.environ.get('beaker.session')
    #session['password'] = request.forms.password
    session['name_last'] = request.forms.name_last
    session['name_first'] = request.forms.name_first
    session['kana_last'] = request.forms.kana_last
    session['kana_first'] = request.forms.kana_first
    session['student_id'] = request.forms.student_id
    session['isc_account'] = request.forms.isc_account
    session['club_account'] = request.forms.club_account
    time = datetime.now(pytz.timezone('Asia/Tokyo'))

    return template('show',
        name_last=session['name_last'],
        name_first=session['name_first'],
        kana_last=session['kana_last'],
        kana_first=session['kana_first'],
        student_id=session['student_id'],
        isc_account=session['isc_account'],
        club_account=session['club_account'],
        time=time.strftime('%Y-%m-%d %H:%M:%S %z'),
        hostname=gethostname(),
        remote_addr=request.remote_addr)


@route('/mail')
def mail():
    session = request.environ.get('beaker.session')
    session.save()

    for_user  = "=================================================================\n"
    for_user += "　共用計算機アカウント申請手続きのご案内\n"
    for_user += "=================================================================\n"
    for_user += "\n"
    for_user += "学生自治ネットワーク委員会からのお知らせです。\n"
    for_user += "以下のとおりアカウント申請を承りました。\n"
    for_user += "\n"
    for_user += "=================================================================\n"
    for_user += "　氏名　　　　　 : " + session['name_last'] + " " + session['name_first'] + " (" + session['kana_last'] + " " + session['kana_first'] + ")\n"
    for_user += "　学生番号　　　 : " + session['student_id'] + "\n"
    for_user += "　メールアドレス : " + session['isc_account'] + "@mail.kyutech.jp\n"
    for_user += "　-------------------------------------------------------------\n"
    for_user += "　ユーザ名　　　 : " + session['club_account'] + "\n"
    for_user += "　-------------------------------------------------------------\n"
    for_user += "　申請日時　　　 : " + datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S %z') + "\n"
    for_user += "　アクセス元　　 : " + gethostname() + " (" + request.remote_addr + ")\n"
    for_user += "=================================================================\n"
    for_user += "\n"
    for_user += "これらの申請内容に間違いがなければ、申請日時から <<30分以内>> に\n"
    for_user += "以下の URL へアクセスしてください。\n"
    for_user += "https://entry.club.kyutech.ac.jp/mars/finish.py?key=" + session.id + "\n"
    for_user += "\n"
    for_user += "※この申請内容に心当たりのない場合は、誠におそれいりますが\n"
    for_user += "　メールを破棄して頂きますようお願いいたします。\n"
    for_user += "\n"
    for_user += "-- \n"
    for_user += "このメールは九州工業大学学生自治ネットワーク委員会の\n"
    for_user += "共用計算機アカウント発行申請自動受付システムにより送信されました。\n"
    for_user += "\n"
    for_user += "学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n"
    for_user += "=================================================================\n"
    for_user += "                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n"

    to_addr = "lan2014@club.kyutech.ac.jp"
    subject = "Account Request Validation"
    msg = create_msg(FROM_ADDR, to_addr, ENCODING, subject, for_user)
    send_msg(FROM_ADDR, to_addr, msg, SMTP_SRV, 25)

    return template('mail')


if __name__ == '__main__':
    app = SessionMiddleware(app(), session_opts)
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)
