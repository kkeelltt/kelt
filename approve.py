#!/user/bin/python
# -*- coding: utf-8 -*-

import bottle


@bottle.route('/request')
def request():
    # login

    # sql select

    return bottle.template('request')


@bottle.route('/finish')
def finish():
    # sql delete

    # ldap insert

    # send mail to user

    # send mail to admin

    return bottle.template('finish')
