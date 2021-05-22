import json
from datetime import datetime
from my_text import Text
text = Text()

import googlemaps
from aiogram import types
from geopy.distance import geodesic

from bot2 import db, bot
from config2 import API_KEY , NIKO



def roztoyanie(location: dict):

    you = (location['latitude'], location['longitude'])
    km = geodesic(NIKO, you).km
    return int(km)

def proschet(location: dict):
    you = (location['latitude'], location['longitude'])
    gmaps_client = googlemaps.Client(key=API_KEY)

    d = gmaps_client.distance_matrix(
        origins=NIKO,
        destinations=(you),
        mode='driving',
    )
    return d['rows'][0]['elements'][0]['distance']['text'].replace('km', '')


async def send_all():
    subscriptions = db.get_subscriptions()
    prise = read_json()
    data = datetime.today().strftime("%d.%m.%Y")

    for user in subscriptions:
        await bot.send_message(user[1], text.prise_rozsilka(data,prise), disable_notification=True)


def admin_validate(message: types.Message)-> bool:
    admin_many = db.get_admin()
    for admin in admin_many:
        if admin[1] == str(message.from_user.id):
            return True

def user_subskribe(message: types.Message) ->bool:
    user = db.get_user(message.from_user.id)
    print(user)
    if db.get_user(message.from_user.id):
        user = db.get_user(message.from_user.id)
        if user[0][2] == 1:
            return True

def read_json():
    utput_json = json.load(open('data1.json'))
    return ("\n".join("🌿{}\t{}грн/т".format(k, v) for k, v in utput_json.items()))

def vremya():
    data = datetime.now().hour
    if 8 < int(data) < 17 :
        return True

if __name__ == '__main__':
    pass
