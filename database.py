#!/user/bin/python
# -*- coding: utf-8 -*-

import sqlite3


def create():
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    sql = """CREATE TABLE waiting(name_last, name_first,
                                  kana_last, kana_first,
                                  club_account, isc_account, password)"""
    c.execute(sql)

    conn.commit()
    conn.close()


def insert(session):
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    sql = 'INSERT INTO waiting VALUES(?, ?, ?, ?, ?, ?, ?)'
    c.execute(sql, (
        session['name_last'],
        session['name_first'],
        session['kana_last'],
        session['kana_first'],
        session['club_account'],
        session['isc_account'],
        session['password'])
    )

    conn.commit()
    conn.close()


def search(club_account):
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    sql = 'SELECT club_account FROM waiting WHERE club_account=?'
    c.execute(sql, (club_account,))
    result = c.fetchone()

    conn.commit()
    conn.close()

    return result
