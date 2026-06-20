from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate 
from models import db, Clan, Trener, Oprema, Trening
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/aup1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

CORS(app)
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/api/clanovi', methods=['GET', 'POST'])
def handle_clanovi():
    if request.method == 'POST':
        data = request.json
        db.session.add(Clan(ime=data['ime'], prezime=data['prezime'], email=data['email']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    return jsonify([{"id": c.id, "ime": c.ime, "prezime": c.prezime} for c in Clan.query.all()])

@app.route('/api/clanovi/<int:id>', methods=['DELETE'])
def delete_clan(id):
    clan = Clan.query.get_or_404(id)
    db.session.delete(clan)
    db.session.commit()
    return jsonify({"msg": "Clan obrisan"}), 200

@app.route('/api/treneri', methods=['GET', 'POST'])
def handle_treneri():
    if request.method == 'POST':
        data = request.json
        db.session.add(Trener(ime=data['ime'], prezime=data['prezime'], email=data['email']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    return jsonify([{"id": t.id, "ime": t.ime, "prezime": t.prezime} for t in Trener.query.all()])

@app.route('/api/treneri/<int:id>', methods=['DELETE'])
def delete_trener(id):
    trener = Trener.query.get_or_404(id)
    db.session.delete(trener)
    db.session.commit()
    return jsonify({"msg": "Trener obrisan"}), 200

@app.route('/api/oprema', methods=['GET', 'POST'])
def handle_oprema():
    if request.method == 'POST':
        data = request.json
        db.session.add(Oprema(naziv=data['naziv'], stanje=data['stanje']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    return jsonify([{"id": o.id, "naziv": o.naziv, "stanje": o.stanje} for o in Oprema.query.all()])

@app.route('/api/oprema/<int:id>', methods=['DELETE'])
def delete_oprema(id):
    oprema = Oprema.query.get_or_404(id)
    db.session.delete(oprema)
    db.session.commit()
    return jsonify({"msg": "Oprema obrisana"}), 200

@app.route('/api/treninzi', methods=['GET', 'POST'])
def handle_treninzi():
    if request.method == 'POST':
        data = request.json
        dt = datetime.strptime(data['datum'], '%Y-%m-%dT%H:%M')
        db.session.add(Trening(naziv=data['naziv'], datum=dt, clan_id=data['clan_id'], trener_id=data['trener_id']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    return jsonify([{"id": t.id, "naziv": t.naziv, "datum": t.datum.isoformat(), "clan_id": t.clan_id, "trener_id": t.trener_id} for t in Trening.query.all()])

@app.route('/api/treninzi/<int:id>', methods=['DELETE'])
def delete_trening(id):
    trening = Trening.query.get_or_404(id)
    db.session.delete(trening)
    db.session.commit()
    return jsonify({"msg": "Trening obrisan"}), 200

@app.route('/api/clanovi/<int:id>', methods=['PUT'])
def update_clan(id):
    clan = Clan.query.get_or_404(id)
    data = request.json
    clan.ime = data.get('ime', clan.ime)
    clan.prezime = data.get('prezime', clan.prezime)
    clan.email = data.get('email', clan.email)
    db.session.commit()
    return jsonify({"msg": "Član ažuriran"}), 200

@app.route('/api/treneri/<int:id>', methods=['PUT'])
def update_trener(id):
    trener = Trener.query.get_or_404(id)
    data = request.json
    trener.ime = data.get('ime', trener.ime)
    trener.prezime = data.get('prezime', trener.prezime)
    trener.email = data.get('email', trener.email)
    db.session.commit()
    return jsonify({"msg": "Trener ažuriran"}), 200

@app.route('/api/oprema/<int:id>', methods=['PUT'])
def update_oprema(id):
    oprema = Oprema.query.get_or_404(id)
    data = request.json
    oprema.naziv = data.get('naziv', oprema.naziv)
    oprema.stanje = data.get('stanje', oprema.stanje)
    db.session.commit()
    return jsonify({"msg": "Oprema ažurirana"}), 200

@app.route('/api/treninzi/<int:id>', methods=['PUT'])
def update_trening(id):
    trening = Trening.query.get_or_404(id)
    data = request.json
    trening.naziv = data.get('naziv', trening.naziv)
    if 'datum' in data:
        trening.datum = datetime.strptime(data['datum'], '%Y-%m-%dT%H:%M')
    trening.clan_id = data.get('clan_id', trening.clan_id)
    trening.trener_id = data.get('trener_id', trening.trener_id)
    db.session.commit()
    return jsonify({"msg": "Trening ažuriran"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)