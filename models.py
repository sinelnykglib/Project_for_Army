from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    number = db.Column(db.Integer, primary_key=True)
    machinery = db.Column(db.String(50))
    count = db.Column(db.Integer)
    fuel = db.Column(db.Integer)
    manpower = db.Column(db.Integer)
    num_rota = db.Column(db.Integer)
    bk = db.Column(db.String(255))

class persons(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(255))
    size_clothes = db.Column(db.Integer)
    size_shoes = db.Column(db.Integer)
    serial_num = db.Column(db.BigInteger)
    name_weapon = db.Column(db.String(50))
    num_rota = db.Column(db.Integer)
    rank = db.Column(db.String(50))

class ito(db.Model):
    __tablename__ = 'ito'
    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(50))
    num_rota = db.Column(db.Integer)
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)

class Electro(db.Model):
    __tablename__ = 'electro'
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.BigInteger, nullable=True)
    num_rota = db.Column(db.Integer)
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    count = db.Column(db.String(50))
    num_rota = db.Column(db.Integer)
