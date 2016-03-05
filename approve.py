#!/user/bin/python
# -*- coding: utf-8 -*-

import bottle


@bottle.route('/approve')
def approve():
    # sql delete

    # ldap insert

    # send mail to user

    # send mail to admin

    return bottle.template('approve')
