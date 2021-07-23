from models.site import SiteModel
from uuid import uuid4
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import datetime
from flask_jwt_extended.view_decorators import jwt_required


def normalize_path_params(location=None, min_stars=0, max_stars=5, min_daily=0, 
                            max_daily=10000, limit=50, offset=0, **data) -> dict:

    if location:
        return {
            'min_stars': min_stars,
            'max_stars': max_stars,
            'min_daily': min_daily,
            'max_daily': max_daily,
            'location': location,
            'limit': limit,
            'offset': offset
        }
    return {
            'min_stars': min_stars,
            'max_stars': max_stars,
            'min_daily': min_daily,
            'max_daily': max_daily,
            'limit': limit,
            'offset': offset
        }

# path /hotels?city=Toronto&min_stars=4&daily_max=300
path_params = reqparse.RequestParser()
path_params.add_argument('location', type=str)
path_params.add_argument('min_stars', type=float)
path_params.add_argument('max_stars', type=float)
path_params.add_argument('min_daily', type=float)
path_params.add_argument('max_daily', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parameters = normalize_path_params(**dados_validos)

        if parameters.get('location'):
            hotels = (HotelModel.query.filter(
                HotelModel.location==parameters['location'],
                HotelModel.daily>=parameters['min_daily'],
                HotelModel.daily<=parameters['max_daily'],
                HotelModel.stars>=parameters['min_stars'],
                HotelModel.stars<=parameters['max_stars'])
                .order_by(HotelModel.daily)
                .offset(parameters['offset'])
                .limit(parameters['limit']))

        else:
            hotels = (HotelModel.query.filter(
                HotelModel.daily>=parameters['min_daily'],
                HotelModel.daily<=parameters['max_daily'],
                HotelModel.stars>=parameters['min_stars'],
                HotelModel.stars<=parameters['max_stars'])
                .order_by(HotelModel.daily)
                .offset(parameters['offset'])
                .limit(parameters['limit']))

        resp_hotels = [h.json() for h in hotels]

        return {
            "query_datetime": str(datetime.datetime.now()),
            "count": len(resp_hotels),
            "hotels": resp_hotels
            }

        # conn = sqlite3.connect('database.db')
        # cursor = conn.cursor()

        # if not parameters.get('location'):
        #     query = "SELECT * FROM hotels \
        #      WHERE (stars > ? and stars < ?) \
        #      and (daily > ? and daily < ?) \
        #      LIMIT ? OFFSET ?"

        #     tuple_r = tuple([parameters[k] for k in parameters])
        #     result = cursor.execute(query, tuple_r)
        # else:
        #     query = "SELECT * FROM hotels \
        #      WHERE (stars > ? and stars < ?) \
        #      and (daily > ? and daily < ?) \
        #      and location = ? \
        #      LIMIT ? OFFSET ?"

        #     tuple_r = tuple([parameters[k] for k in parameters])
        #     result = cursor.execute(query, tuple_r)
            
        # hotels = []
        # for line in result:
        #     hotels.append({
        #         "hotel_id": line[0],
        #         "name": line[1],
        #         "stars": line[2],
        #         "daily": line[3],
        #         "location": line[4]
        #     })
        
        # return {
        #     "query_datetime": str(datetime.datetime.now()),
        #     "hotels_in_query": len(hotels),
        #     "hotels": hotels
        #     }


class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type=str, required=True, help="The field 'nome' cannot be left blank.")
    arguments.add_argument('stars', type=float, required=True, help="The field 'stars' cannot be left blank.")
    arguments.add_argument('daily', type=float, required=True, help="The field 'daily' cannot be left blank.")
    arguments.add_argument('location', type=str, required=True, help="The field 'nome' location be left blank.")
    arguments.add_argument('site_id', type=str, required=True, help="The field 'site_id' location be left blank.")

    def get(self, hotel_id: str):
        hotel = HotelModel.find_hotel(hotel_id=hotel_id)
        if hotel:
            return hotel.json()
        return {'message': f"Hotel id '{hotel_id}' not found"}, 404  # not found

    @jwt_required
    def post(self, hotel_id: str):
        # if hotel exists
        if HotelModel.find_hotel(hotel_id):
            return {'message': f"Hotel id '{hotel_id}' already exists."}, 400  # bad request

        # if hotel not exists, then create one
        dados = Hotel.arguments.parse_args()
        hotel_obj = HotelModel(**dados)

        if not SiteModel.find_site_by_id(dados.get('site_id')):
            return {'message', f"Site '{dados.get('site_id')}' not exists."}, 400

        try:
            hotel_obj.save()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500  # internal server error
        return hotel_obj.json(), 200  # status OK
        
    @jwt_required
    def put(self, hotel_id: str):
        dados = Hotel.arguments.parse_args()
        
        # try to find hotel and update
        hotel = HotelModel.find_hotel(hotel_id=hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            hotel.save()  # persist the data
            return hotel.json(), 200   # status OK
        
        # if hotel not exists, then create a new hotel
        new_hotel = HotelModel(hotel_id=str(uuid4()), **dados)

        try:
            new_hotel.save()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500  # internal server error
        return new_hotel.json(), 201  # created
    
    @jwt_required
    def delete(self, hotel_id: str):
        hotel = HotelModel.find_hotel(hotel_id=hotel_id)
        if hotel:
            try:
                hotel.delete()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel'}, 500  # internal server error
            return {'message': f"Hotel '{hotel_id}' deleted."}
        return {'message': f"Hotel '{hotel_id}' not found."}
