import re
from uuid import uuid4
from models.hotel import HotelModel
import random

cities = list()
names = list()
with open('scripts/cities.txt', 'r') as file:
    read_cities = file.readlines()
    for j in read_cities:
        city = j.strip('\n')
        cities.append(city)


with open('scripts/names_hotel.txt', 'r') as file:
    read_names = file.readlines()
    for j in read_names:
        name = j.strip('\n')
        names.append(name)

def insert_data():
    for _ in range(400):
        hotel_id = str(uuid4())
        name = random.choice(names)
        stars = round(random.uniform(1, 5), 1)
        daily = round(random.uniform(100, 600), 2)
        location = random.choice(cities)

        hotel = HotelModel(hotel_id=hotel_id, name=name,
                            stars=stars, daily=daily, location=location)
        
        hotel.save()

    return {"message": "Inserted many Hotels, see database."}, 201
