#!/user/bin/python
# -*- coding: utf-8 -*-

import base64
import shlex
import subprocess


def ldapsearch(uid):
    cmd1 = 'ldapsearch uid={0}'.format(uid)
    cmd2 = 'grep numEntries'
    p1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(cmd2),
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    if p2.communicate()[0]:
        return True
    else:
        return False


def ldifsearch(isc_account):
    isc_ldap = dict(displayName='', gecos='', employeeNumber='', mail='')

    for key in isc_ldap:
        cmd = '/home/kelt/isc-ldap/ldifsearch'
        isc_ldap[key] = subprocess.Popen(
            [cmd, isc_account, key],
            stdout=subprocess.PIPE
        ).communicate()[0].decode()
    else:
        isc_ldap['displayName'] = base64.b64decode(isc_ldap['displayName'])

    return isc_ldap
