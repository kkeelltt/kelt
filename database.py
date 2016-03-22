#!/user/bin/python
# -*- coding: utf-8 -*-

import sqlite3


def create():
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    sql = """CREATE TABLE waiting(name_last, name_first,
                                  kana_last, kana_first,
                                  student_id, isc_account,
                                  club_account, password
                                  )"""
    c.execute(sql)

    conn.commit()
    conn.close()


def insert(data):
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    sql = 'INSERT INTO waiting VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
    c.execute(sql, (
        data['name_last'],
        data['name_first'],
        data['kana_last'],
        data['kana_first'],
        data['student_id'],
        data['isc_account'],
        data['club_account'],
        data['password'])
    )

    conn.commit()
    conn.close()


def select(club_account):
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    sql = 'SELECT * FROM waiting WHERE club_account=?'
    c.execute(sql, (club_account,))
    tmp = c.fetchall()

    conn.commit()
    conn.close()

    if tmp:
        data = dict()
        data['name_last'] = tmp[0][0]
        data['name_first'] = tmp[0][1]
        data['kana_last'] = tmp[0][2]
        data['kana_first'] = tmp[0][3]
        data['student_id'] = tmp[0][4]
        data['isc_account'] = tmp[0][5]
        data['club_account'] = tmp[0][6]
        data['password'] = tmp[0][7]

        return data
    else:
        return None
