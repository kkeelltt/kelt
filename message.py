#!/user/bin/python
# -*- coding: utf-8 -*-

# import base64
from email.mime.text import MIMEText
# from email.utils import formatdate
import smtplib
# import subprocess


def create_msg(from_addr, to_addr, subject, body_text):
    msg = MIMEText(body_text)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    # msg['Date'] = formatdate(localtime=True)
    return msg


def send_msg(host, msg):
    smtp = smtplib.SMTP(host)
    smtp.send_message(msg)
    smtp.quit()


def write_first(session):
    body = str()
    body += '===============================================================\n'
    body += '　共用計算機アカウント申請手続きのご案内\n'
    body += '===============================================================\n'
    body += '\n'
    body += '学生自治ネットワーク委員会からのお知らせです。\n'
    body += '以下のとおりアカウント申請を承りました。\n'
    body += '\n'
    body += '===============================================================\n'
    body += '　氏名　　　　　 : {name_last} {name_first} '.format(**session)
    body += '({kana_last} {kana_first})\n'.format(**session)
    body += '　学生番号　　　 : {student_id}\n'.format(**session)
    body += '　メールアドレス : {isc_account}@mail.kyutech.jp\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　ユーザ名　　　 : {club_account}\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　申請日時　　　 : {format_time}\n'.format(**session)
    body += '　アクセス元　　 : {remote_host} ({remote_addr})\n'.format(**session)
    body += '===============================================================\n'
    body += '\n'
    body += 'これらの申請内容に間違いがなければ、申請日時から30分以内に\n'
    body += '以下の URL へアクセスしてください。\n'
    body += 'http://localhost:8080/finish/{0}\n'.format(session.id)
    body += '\n'
    body += '※この申請内容に心当たりのない場合は、誠におそれいりますが\n'
    body += '　メールを破棄して頂きますようお願いいたします。\n'
    body += '\n'
    body += '-- \n'
    body += 'このメールは九州工業大学学生自治ネットワーク委員会の\n'
    body += '共用計算機アカウント発行申請自動受付システムにより送信されました。\n'
    body += '\n'
    body += '学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n'
    body += '===============================================================\n'
    body += '                 Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n'

    return body


def write_second(session):
    isc_ldap = dict(displayName='', gecos='', employeeNumber='', mail='')
    club_ldap = dict(displayName='', employeeNumber='')
    """
    for key in isc_ldap:
        cmd = '/home/staff/CIA/admin-sys/isc-ldap/ldifsearch'
        isc_ldap[key] = subprocess.Popen(
            [cmd, session['club_account'], key],
            stdout=subprocess.PIPE
        ).communicate()[0].decode()

    isc_ldap['displayName'] = base64.b64decode(isc_ldap['displayName'])
    """
    body = str()
    body += '===============================================================\n'
    body += '　共用計算機アカウント申請依頼\n'
    body += '===============================================================\n'
    body += '\n'
    body += '申請内容\n'
    body += '===============================================================\n'
    body += '　ユーザ名　　　　 : {club_account}\n'.format(**session)
    body += '　-------------------------------------------------------------\n'
    body += '　申請日時　　　　 : {format_time}\n'.format(**session)
    body += '　アクセス元　　　 : {remote_host} ({remote_addr})\n'.format(**session)
    body += '===============================================================\n'
    body += '\n'
    body += '申請者情報\n'
    body += '===============================================================\n'
    body += '　氏名（漢字）　　 : {name_last} {name_first}\n'.format(**session)
    body += '　氏名（ふりがな） : {kana_last} {kana_first}\n'.format(**session)
    body += '　学生番号　　　　 : {student_id}\n'.format(**session)
    body += '　メールアドレス　 : {isc_account}@mail.kyutech.jp\n'.format(**session)
    body += '===============================================================\n'
    body += '\n'
    body += 'データ照合 @isc.kyutech\n'
    body += '===============================================================\n'
    body += '　氏名（漢字）　　 : {displayName}'.format(**isc_ldap)
    body += '　氏名（ローマ字） : {gecos}'.format(**isc_ldap)
    body += '　学生番号　　　　 : {employeeNumber}'.format(**isc_ldap)
    body += '　メールアドレス　 : {mail}'.format(**isc_ldap)
    body += '===============================================================\n'
    body += '\n'
    body += 'データ照合 @club.kyutech\n'
    body += '===============================================================\n'
    body += '　氏名一致　　　　 : {displayName}'.format(**club_ldap)
    body += '　-------------------------------------------------------------\n'
    body += '　学生番号一致　　 : {employeeNumber}'.format(**club_ldap)
    body += '===============================================================\n'
    body += '\n'
    body += '-- \n'
    body += 'このメールは九州工業大学学生自治ネットワーク委員会の\n'
    body += '共用計算機アカウント発行申請自動受付システムにより送信されました。\n'
    body += '\n'
    body += '学生自治ネットワーク委員会: http://www.club.kyutech.ac.jp/\n'
    body += '===============================================================\n'
    body += '                 Copyright (C) 2016 Kentaro OISHI / K.I.T. SANC\n'

    return body
