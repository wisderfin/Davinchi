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


