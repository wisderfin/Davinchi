import math

from geopy.geocoders import Nominatim


async def get_city_name(latitude, longitude):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((latitude, longitude), language="ru")
    address = location.raw['address']
    city = address.get('city', '')
    if not city:
        city = address.get('town', '')
    if not city:
        city = address.get('village', '')
    state = address['state']
    return f'{state}, {city}'


def long_by_coordinate(lat1, lon1, lat2, lon2):
    R = 6371.0

    # Перевод градусов в радианы
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Разница координат
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Формула Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Расстояние в километрах
    distance = R * c

    return round(distance, 1)

