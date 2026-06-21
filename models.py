from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Clan(db.Model):
    __tablename__ = "clan"
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    treninzi = db.relationship('Trening', backref='clan', cascade="all, delete-orphan")

class Trener(db.Model):
    __tablename__ = "treneri"
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    treninzi = db.relationship('Trening', backref='trener', cascade="all, delete-orphan")

class Oprema(db.Model):
    __tablename__ = "oprema"
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    stanje = db.Column(db.String(50), nullable=False)

class Trening(db.Model):
    __tablename__ = "treninzi"
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    datum = db.Column(db.DateTime, nullable=False)
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'), nullable=False)
    trener_id = db.Column(db.Integer, db.ForeignKey('treneri.id'), nullable=False)