from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Clan(db.Model):
    __tablename__ = "clan"  
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    treninzi = db.relationship('Trening', backref='clan', cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ime": self.ime,
            "prezime": self.prezime,
            "email": self.email
        }


class Trener(db.Model):
    __tablename__ = "treneri"
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    treninzi = db.relationship('Trening', backref='trener', cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ime": self.ime,
            "prezime": self.prezime,
            "email": self.email
        }


class Oprema(db.Model):
    __tablename__ = "oprema"
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    stanje = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "naziv": self.naziv,
            "stanje": self.stanje
        }


class Trening(db.Model):
    __tablename__ = "treninzi"
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    datum = db.Column(db.DateTime, nullable=False)
    
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'), nullable=False)
    trener_id = db.Column(db.Integer, db.ForeignKey('treneri.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "naziv": self.naziv,
            "datum": self.datum.isoformat() if self.datum else "",
            "clan_id": self.clan_id,
            "trener_id": self.trener_id,
            "clan_ime_prezime": f"{self.clan.ime} {self.clan.prezime}" if self.clan else "",
            "trener_ime_prezime": f"{self.trener.ime} {self.trener.prezime}" if self.trener else ""
        }