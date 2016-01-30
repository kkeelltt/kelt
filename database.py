#!/user/bin/python
# -*- coding: utf-8 -*-


import sqlite3


def create():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    sql = '''CREATE TABLE waiting
             (name_last, name_first, kana_last, kana_first,
              student_id, isc_account, club_account)'''
    c.execute(sql)

    conn.commit()
    conn.close()


def insert(session):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    sql = '''INSERT INTO waiting VALUES
             (:name_last, :name_first, :kana_last, :kana_first,
              :student_id, :isc_account, :club_account)'''
    c.execute(sql, session)

    conn.commit()
    conn.close()


#def select():



#def update():



#def delete():
