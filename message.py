#!/user/bin/python
# -*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate


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


def write_first(session, time, remote_host, remote_addr):
    body  = "=================================================================\n"
    body += "　共用計算機アカウント申請手続きのご案内\n"
    body += "=================================================================\n"
    body += "\n"
    body += "学生自治ネットワーク委員会からのお知らせです。\n"
    body += "以下のとおりアカウント申請を承りました。\n"
    body += "\n"
    body += "=================================================================\n"
    body += ("　氏名　　　　　 : " + session['name_last'] + " " + session['name_first'] +
             " (" + session['kana_last'] + " " + session['kana_first'] + ")\n")
    body += "　学生番号　　　 : " + session['student_id'] + "\n"
    body += "　メールアドレス : " + session['isc_account'] + "@mail.kyutech.jp\n"
    body += "　-------------------------------------------------------------\n"
    body += "　ユーザ名　　　 : " + session['club_account'] + "\n"
    body += "　-------------------------------------------------------------\n"
    body += "　申請日時　　　 : " + time.strftime('%Y-%m-%d %H:%M:%S %Z%z') + "\n"
    body += "　アクセス元　　 : " + remote_host + " (" + remote_addr + ")\n"
    body += "=================================================================\n"
    body += "\n"
    body += "これらの申請内容に間違いがなければ、申請日時から <<30分以内>> に\n"
    body += "以下の URL へアクセスしてください。\n"
    body += "https://entry.club.kyutech.ac.jp/mars/finish.py?key=" + session.id + "\n"
    body += "\n"
    body += "※この申請内容に心当たりのない場合は、誠におそれいりますが\n"
    body += "　メールを破棄して頂きますようお願いいたします。\n"
    body += "\n"
    body += "-- \n"
    body += "このメールは九州工業大学学生自治ネットワーク委員会の\n"
    body += "共用計算機アカウント発行申請自動受付システムにより送信されました。\n"
    body += "\n"
    body += "学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n"
    body += "=================================================================\n"
    body += "                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n"

    return body


def write_second(session, time, remote_host, remote_addr):
    body  = "=================================================================\n"
    body += "　共用計算機アカウント申請手続きのご案内\n"
    body += "=================================================================\n"
    body += "\n"
    body += "学生自治ネットワーク委員会からのお知らせです。\n"
    body += "以下のとおりアカウント申請を承りました。\n"
    body += "\n"
    body += "=================================================================\n"
    body += ("　氏名　　　　　 : " + session['name_last'] + " " + session['name_first'] +
             " (" + session['kana_last'] + " " + session['kana_first'] + ")\n")
    body += "　学生番号　　　 : " + session['student_id'] + "\n"
    body += "　メールアドレス : " + session['isc_account'] + "@mail.kyutech.jp\n"
    body += "　-------------------------------------------------------------\n"
    body += "　ユーザ名　　　 : " + session['club_account'] + "\n"
    body += "　-------------------------------------------------------------\n"
    body += "　申請日時　　　 : " + time.strftime('%Y-%m-%d %H:%M:%S %z') + "\n"
    body += "　アクセス元　　 : " + remote_host + " (" + remote_addr + ")\n"
    body += "=================================================================\n"
    body += "\n"
    body += "これらの申請内容に間違いがなければ、申請日時から <<30分以内>> に\n"
    body += "以下の URL へアクセスしてください。\n"
    body += "https://entry.club.kyutech.ac.jp/mars/finish.py?key=" + session.id + "\n"
    body += "\n"
    body += "※この申請内容に心当たりのない場合は、誠におそれいりますが\n"
    body += "　メールを破棄して頂きますようお願いいたします。\n"
    body += "\n"
    body += "-- \n"
    body += "このメールは九州工業大学学生自治ネットワーク委員会の\n"
    body += "共用計算機アカウント発行申請自動受付システムにより送信されました。\n"
    body += "\n"
    body += "学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n"
    body += "=================================================================\n"
    body += "                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n"

    return body


def write_third(session, time, remote_host, remote_addr):
    body  = "=================================================================\n"
    body += "　共用計算機アカウント申請手続きのご案内\n"
    body += "=================================================================\n"
    body += "\n"
    body += "学生自治ネットワーク委員会からのお知らせです。\n"
    body += "以下のとおりアカウント申請を承りました。\n"
    body += "\n"
    body += "=================================================================\n"
    body += ("　氏名　　　　　 : " + session['name_last'] + " " + session['name_first'] +
             " (" + session['kana_last'] + " " + session['kana_first'] + ")\n")
    body += "　学生番号　　　 : " + session['student_id'] + "\n"
    body += "　メールアドレス : " + session['isc_account'] + "@mail.kyutech.jp\n"
    body += "　-------------------------------------------------------------\n"
    body += "　ユーザ名　　　 : " + session['club_account'] + "\n"
    body += "　-------------------------------------------------------------\n"
    body += "　申請日時　　　 : " + time.strftime('%Y-%m-%d %H:%M:%S %z') + "\n"
    body += "　アクセス元　　 : " + remote_host + " (" + remote_addr + ")\n"
    body += "=================================================================\n"
    body += "\n"
    body += "これらの申請内容に間違いがなければ、申請日時から <<30分以内>> に\n"
    body += "以下の URL へアクセスしてください。\n"
    body += "https://entry.club.kyutech.ac.jp/mars/finish.py?key=" + session.id + "\n"
    body += "\n"
    body += "※この申請内容に心当たりのない場合は、誠におそれいりますが\n"
    body += "　メールを破棄して頂きますようお願いいたします。\n"
    body += "\n"
    body += "-- \n"
    body += "このメールは九州工業大学学生自治ネットワーク委員会の\n"
    body += "共用計算機アカウント発行申請自動受付システムにより送信されました。\n"
    body += "\n"
    body += "学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n"
    body += "=================================================================\n"
    body += "                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n"

    return body


def write_fourth(session, time, remote_host, remote_addr):
    body  = "=================================================================\n"
    body += "　共用計算機アカウント申請手続きのご案内\n"
    body += "=================================================================\n"
    body += "\n"
    body += "学生自治ネットワーク委員会からのお知らせです。\n"
    body += "以下のとおりアカウント申請を承りました。\n"
    body += "\n"
    body += "=================================================================\n"
    body += ("　氏名　　　　　 : " + session['name_last'] + " " + session['name_first'] +
             " (" + session['kana_last'] + " " + session['kana_first'] + ")\n")
    body += "　学生番号　　　 : " + session['student_id'] + "\n"
    body += "　メールアドレス : " + session['isc_account'] + "@mail.kyutech.jp\n"
    body += "　-------------------------------------------------------------\n"
    body += "　ユーザ名　　　 : " + session['club_account'] + "\n"
    body += "　-------------------------------------------------------------\n"
    body += "　申請日時　　　 : " + time.strftime('%Y-%m-%d %H:%M:%S %z') + "\n"
    body += "　アクセス元　　 : " + remote_host + " (" + remote_addr + ")\n"
    body += "=================================================================\n"
    body += "\n"
    body += "これらの申請内容に間違いがなければ、申請日時から <<30分以内>> に\n"
    body += "以下の URL へアクセスしてください。\n"
    body += "https://entry.club.kyutech.ac.jp/mars/finish.py?key=" + session.id + "\n"
    body += "\n"
    body += "※この申請内容に心当たりのない場合は、誠におそれいりますが\n"
    body += "　メールを破棄して頂きますようお願いいたします。\n"
    body += "\n"
    body += "-- \n"
    body += "このメールは九州工業大学学生自治ネットワーク委員会の\n"
    body += "共用計算機アカウント発行申請自動受付システムにより送信されました。\n"
    body += "\n"
    body += "学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n"
    body += "=================================================================\n"
    body += "                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n"

    return body
