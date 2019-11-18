from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(20), unique=True, nullable=False)
    images = db.relationship('Image', backref="user", lazy=True)
    stamps = db.relationship('Stamp')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "images": list(map(lambda x: x.serialize(), self.images)),
            "stamps": list(map(lambda x: x.serialize(), self.stamps))
        }
class Stamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(2000), nullable=False)
    country_label = db.Column(db.String(500), nullable=True)
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