#!/user/bin/python
# -*- coding: utf-8 -*-

import bottle

import database
import ldap


@bottle.route('/check/<key>')
def check(key=None):
    data = database.select(key)
    isc_ldap = ldap.ldifsearch(data[5])

    return bottle.template(
        'check',
        name_last=data[0],
        name_first=data[1],
        kana_last=data[2],
        kana_first=data[3],
        club_account=data[4],
        isc_account=data[5],
        displayName=isc_ldap['displayName'],
        gecos=isc_ldap['gecos'],
        employeeNumber=isc_ldap['employeeNumber'],
        mail=isc_ldap['mail']
    )


if __name__ == '__main__':
    bottle.run(host='', port=8080, debug=True, reloader=True)
