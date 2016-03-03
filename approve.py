#!/user/bin/python
# -*- coding: utf-8 -*-

import bottle as btl


@btl.route('/request')
def request():
    # login

    # sql select

    return btl.template('request')


@btl.route('/finish')
def finish():
    # sql delete

    # ldap insert

    # send mail to user

    # send mail to admin

    return btl.template('finish')
