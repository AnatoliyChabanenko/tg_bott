import googlemaps
import os
from dotenv import  load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')


def proschet(location: dict):
    me = ('46.849476', '31.990699')
    you = (location['latitude'], location['longitude'])
    gmaps_client = googlemaps.Client(key=API_KEY)

    d = gmaps_client.distance_matrix(
        origins=me,
        destinations=(you),
        mode='driving',
    )
    print(d)
    return d['rows'][0]['elements'][0]['distance']['text'].replace('km', '')


