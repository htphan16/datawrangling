import requests
import json
import pprint

BASE_URL = "https://api.spotify.com/v1/"
ARTIST_URL = BASE_URL + "artist/"
ALBUM_URL = BASE_URL + "albums/"
access_token = 'BQBJlyoPnCYe49i5P8Y5oWrUgcY2PAxAisy_ElPv3jXBHgYQm6BFBdlUykj1QZhsg8qfYE2lE5g0a0ixC84Cny4n_51FDOrrJZW-HjQQ0rdamkau0wJgTz-0gaRwO6HaXzFF8SlhiyHDVthpD2-sFW8Cqdcu-BBI90iQrWN5WRN2zpw_x1G0HK7-kyU7lfGazAe8ZpdmqA-fz42gPmzd-IUAmSiEObNmMemydrR-IO8nQeZodVC18BuTAZCAxVxbJ6NM4uhuZF-EcJ4Lx7I8dMo2LPgw0oyn'
ly_tear = '2jJfnAZE6IG3oYnUv2eCj4'
fy = '66J1OXSaS3hBZASOV3el8t'

def query_site(url, uid, suburl, params):
    r = requests.get(url + uid + suburl, params=params, headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(access_token)})
    print("requesting", r.url)
    print(r)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


#pprint.pprint(query_site(ALBUM_URL, ly_tear, '', {}))
#pprint.pprint(query_site(ALBUM_URL, ly_tear, '/tracks', {}))
pprint.pprint(query_site(ALBUM_URL, '', '', {'ids': ly_tear + ',' + fy}))

