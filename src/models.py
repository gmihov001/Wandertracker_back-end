from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(20), unique=True, nullable=False)
    stamps = db.relationship('Stamp')
    countries = db.relationship('Country')
    documents = db.relationship('Document')
    emergencyContacs = db.relationship('EmergencyContac')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "stamps": list(map(lambda x: x.serialize(), self.stamps)),
            "countries": list(map(lambda x: x.serialize(), self.countries)),
            "documents": list(map(lambda x: x.serialize(), self.documents)),
            "emergencyContacs ": list(map(lambda x: x.serialize(), self.emergencyContacs)),

        }


class Stamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(2000), nullable=False)
    country_label = db.Column(db.String(100), nullable=False)
    country_value = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def serialize(self):
        return{
          "id": self.id,
          "photo": self.photo,
          "country_label": self.country_label,
          "country_value": self.country_value
        }

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    country_label = db.Column(db.String(100), nullable=True)
    country_value = db.Column(db.String(5), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def serialize(self):
        return{
          "id": self.id,
          "latitude": self.latitude,
          "country_label": self.country_label,
          "country_value": self.country_value,
          "longitude": self.longitude
        }


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255), nullable=False)
    country_label = db.Column(db.String(100), nullable=True)
    country_value = db.Column(db.String(5), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def serialize(self):
        return{
          "id": self.id,
          "photo": self.photo,
          "country_label": self.country_label,
          "country_value": self.country_value
        }

class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000), nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def serialize(self):
        return{
          "id": self.id,
          "name": self.name,
          "phone_number": self.phone_number
        }

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000), nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def serialize(self):
        return{
          "id": self.id,
          "name": self.name,
          "phone_number": self.phone_number
        }        

