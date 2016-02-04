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


def write_first(session):
    body  = '=================================================================\n'
    body += '　共用計算機アカウント申請手続きのご案内\n'
    body += '=================================================================\n'
    body += '\n'
    body += '学生自治ネットワーク委員会からのお知らせです。\n'
    body += '以下のとおりアカウント申請を承りました。\n'
    body += '\n'
    body += '=================================================================\n'
    body += '　氏名　　　　　 : {name_last} {name_first} ({kana_last} {kana_first})\n'.format(**session)
    body += '　学生番号　　　 : {student_id}\n'.format(**session)
    body += '　メールアドレス : {isc_account}@mail.kyutech.jp\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　ユーザ名　　　 : {club_account}\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　申請日時　　　 : {format_date}\n'.format(**session)
    body += '　アクセス元　　 : {remote_host} ({remote_addr})\n'.format(**session)
    body += '=================================================================\n'
    body += '\n'
    body += 'これらの申請内容に間違いがなければ、申請日時から30分以内に\n'
    body += '以下の URL へアクセスしてください。\n'
    body += 'http://:8080/ask/' + session.id + '\n'
    body += '\n'
    body += '※この申請内容に心当たりのない場合は、誠におそれいりますが\n'
    body += '　メールを破棄して頂きますようお願いいたします。\n'
    body += '\n'
    body += '-- \n'
    body += 'このメールは九州工業大学学生自治ネットワーク委員会の\n'
    body += '共用計算機アカウント発行申請自動受付システムにより送信されました。\n'
    body += '\n'
    body += '学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n'
    body += '=================================================================\n'
    body += '                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n'

    return body


def write_second(session):
    body  = '=================================================================\n'
    body += '　共用計算機アカウント申請手続きのご案内\n'
    body += '=================================================================\n'
    body += '\n'
    body += '学生自治ネットワーク委員会からのお知らせです。\n'
    body += '以下のとおりアカウント申請を承りました。\n'
    body += '\n'
    body += '=================================================================\n'
    body += '　氏名　　　　　 : {name_last} {name_first} ({kana_last} {kana_first})\n'.format(**session)
    body += '　学生番号　　　 : {student_id}\n'.format(**session)
    body += '　メールアドレス : {isc_account}@mail.kyutech.jp\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　ユーザ名　　　 : {club_account}\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　申請日時　　　 : {format_date}\n'.format(**session)
    body += '　アクセス元　　 : {remote_host} ({remote_addr})\n'.format(**session)
    body += '=================================================================\n'
    body += '\n'
    body += '数日中にアカウントを発行し、アカウント登録完了のメールをお送りしますので\n'
    body += '今しばらくお待ち頂ますようお願いいたします。\n'
    body += '\n'
    body += '-- \n'
    body += 'このメールは九州工業大学学生自治ネットワーク委員会の\n'
    body += '共用計算機アカウント発行申請自動受付システムにより送信されました。\n'
    body += '\n'
    body += '学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n'
    body += '=================================================================\n'
    body += '                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n'

    return body


def write_third(session):
    body  = '=================================================================\n'
    body += '　共用計算機アカウント申請依頼\n'
    body += '=================================================================\n'
    body += '\n'
    body += '申請内容\n'
    body += '=================================================================\n'
    body += '　ユーザ名　　　　 : {club_account}\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　申請日時　　　　 : {format_date}\n'.format(**session)
    body += '　アクセス元　　　 : {remote_host} ({remote_addr})\n'.format(**session)
    body += '=================================================================\n'
    body += '\n'
    body += '申請者情報\n'
    body += '=================================================================\n'
    body += '　氏名（漢字）　　 : {name_last} {name_first}\n'.format(**session)
    body += '　氏名（ふりがな） : {kana_last} {kana_first}\n'.format(**session)
    body += '　学生番号　　　　 : {student_id}\n'.format(**session)
    body += '　メールアドレス　 : {isc_account}@mail.kyutech.jp\n'.format(**session)
    body += '=================================================================\n'
    body += '\n'
    body += 'データ照合 @isc.kyutech\n'
    body += '=================================================================\n'
    body += '　氏名（漢字）　　 : '
    body += '　氏名（ローマ字） : '
    body += '　学生番号　　　　 : '
    body += '　メールアドレス　 : '
    body += '=================================================================\n'
    body += '\n'
    body += 'データ照合 @club.kyutech\n'
    body += '=================================================================\n'
    body += '　学生番号一致　　 : '
    body += '　-------------------------------------------------------------\n'
    body += '　氏名一致　　　　 : '
    body += '=================================================================\n'
    body += '\n'
    body += '-- \n'
    body += 'このメールは九州工業大学学生自治ネットワーク委員会の\n'
    body += '共用計算機アカウント発行申請自動受付システムにより送信されました。\n'
    body += '\n'
    body += '学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n'
    body += '=================================================================\n'
    body += '                   Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n'

    return body
