from blacklist import BLACKLIST
from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserLogin, UserLogout, UserRegister, Users
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Jbs8aGbbAyt7iMa878Pnsj'
app.config['JWT_BLACKLIST_ENABLED'] = True


api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_db():
    db.create_all()

@jwt.token_in_blacklist_loader
def verify_block_list(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_access_token():
    return jsonify({'message': "You have been logged out."}), 401  # Unautorized

# Hotels resource
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

# Users resource
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:user_id>')

# User register resource
api.add_resource(UserRegister, '/register')

# Login resource
api.add_resource(UserLogin, '/login')

# Logout resource
api.add_resource(UserLogout, '/logout')

# Sites resource
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:site_url>')

if __name__ == '__main__':
    from database.sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)
