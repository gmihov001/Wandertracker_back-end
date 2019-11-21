"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import User, Stamp, Country, Document, EmergencyContac
from flask_jwt_simple import (JWTManager, jwt_required, create_jwt, get_jwt_identity)


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)


# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    # if username != 'test' or password != 'test':
    #     return jsonify({"msg": "Bad username or password"}), 401
    usercheck = User.query.filter_by(username=username, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or password"}), 401
    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username)}
    return jsonify(ret), 200


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_users():
    all_people = User.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

@app.route('/adduser', methods=['POST'])
def handle_user():
    body = request.get_json()

    user1 = User(username=body['username'], email=body['email'], password=body['password'])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200


@app.route('/user/<int:id>/stamp', methods=['GET','POST'])
def handle_stamp(id):
    
    if request.method == 'POST':
        body = request.get_json() #{ 'username': 'new_username'}
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'photo' not in body:
            raise APIException('You need to specify the photo', status_code=400)
        if 'country_label' not in body:
            raise APIException('You need to specify the country_label', status_code=400)
        if 'country_value' not in body:
            raise APIException('You need to specify the country_value', status_code=400)
        
        user1 = User.query.get(id)
        if user1 is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        try:
            stamp = Stamp(photo=body['photo'] ,country_value=body['country_value'], country_label=body['country_label'])
            user1.stamps.append(stamp)
            db.session.add(user1)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify({"error": str(e.__dict__['orig'])}), 409
        return jsonify({"message": "success"}), 200

    

    return "Invalid Method", 404
        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'username' not in body:
        #     raise APIException('You need to specify the username', status_code=400)
        # if 'email' not in body:
        #     raise APIException('You need to specify the email', status_code=400)

    stamp1 = Stamp(user_id=body['user_id'],photo=body['photo'] ,country_value=body['country_value'], country_label=body['country_label'])
    db.session.add(stamp1)
    db.session.commit()
    return "ok", 200

@app.route('/documents', methods=['POST'])
def handle_document():
    body = request.get_json()

        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'username' not in body:
        #     raise APIException('You need to specify the username', status_code=400)
        # if 'email' not in body:
        #     raise APIException('You need to specify the email', status_code=400)

    document1 = Document(user_id=body['user_id'], photo=body['photo'], country_value=body['country_value'], country_label=body['country_label'])
    db.session.add(document1)
    db.session.commit()
    return "ok", 200


@app.route('/addCountry', methods=['POST'])
def handle_country():
    body = request.get_json()

        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'username' not in body:
        #     raise APIException('You need to specify the username', status_code=400)
        # if 'email' not in body:
        #     raise APIException('You need to specify the email', status_code=400)

    country1 = Country(user_id=body['user_id'],latitude=body['latitude'],longitude=body['longitude'] ,country_value=body['country_value'], country_label=body['country_label'])
    db.session.add(country1)
    db.session.commit()
    return "ok", 200


@app.route('/user/<int:id>/emergencyContact', methods=['GET','POST'])
def handle_emergencyContac(id):
    
    if request.method == 'POST':
        body = request.get_json() #{ 'username': 'new_username'}
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'phone_number' not in body:
            raise APIException('You need to specify the phone_number', status_code=400)
        
        
        user1 = User.query.get(id)
        if user1 is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        try:
            emergencyContact = EmergencyContact(name=body['name'] ,phone_number=body['phone_number'])
            user1.emergencyContacts.append(emergencyContact)
            db.session.add(user1)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify({"error": str(e.__dict__['orig'])}), 409
        return jsonify({"message": "success"}), 200

    

    return "Invalid Method", 404
        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'username' not in body:
        #     raise APIException('You need to specify the username', status_code=400)
        # if 'email' not in body:
        #     raise APIException('You need to specify the email', status_code=400)

    emergencyContact1 = EmergencyContact(user_id=body['user_id'],name=body['name'] ,phone_number=body['phone_number'])
    db.session.add(emergencyContact1)
    db.session.commit()
    return "ok", 200

@app.route('/users/0', methods=['GET'])
def handle_single():
    all_photo = User.query.all()
    all_photo = list(map(lambda x: x.serialize(), all_photo))
    return jsonify(all_photo), 200

@app.route('/user/1/document/<int:did>', methods=['DELETE'])
def handle_delete(did):
    document = Document.query.get(did)
    db.session.delete(document)
    db.session.commit()
    return jsonify({"message": "ok"}), 200





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



