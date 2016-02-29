import database

session = {}
session['name_last'] = 'Kai'
session['name_first'] = 'Yuto'
session['kana_last'] = 'K'
session['kana_first'] = 'Y'
session['club_account'] = 'kiiiite'
session['isc_account'] = 'o222222o'
session['password'] = 'kaikaikaikia'

#database.insert(session)

if database.select('kelkelt'):
    print('waiting')
else:
    print('available')
