from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate 
from models import db, Clan, Trener, Oprema, Trening
from datetime import datetime
from sqlalchemy import or_  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/aup1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/api/clanovi', methods=['GET', 'POST'])
def handle_clanovi():
    if request.method == 'POST':
        data = request.json
        db.session.add(Clan(ime=data['ime'], prezime=data['prezime'], email=data['email']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '', type=str)

    upit = Clan.query
    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Clan.ime.ilike(pojam),
            Clan.prezime.ilike(pojam),
            Clan.email.ilike(pojam)
        ))
    
    upit = upit.order_by(Clan.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [c.to_dict() for c in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })

@app.route('/api/clanovi/<int:id>', methods=['DELETE'])
def delete_clan(id):
    clan = Clan.query.get_or_404(id)
    db.session.delete(clan)
    db.session.commit()
    return jsonify({"msg": "Clan obrisan"}), 200

@app.route('/api/clanovi/<int:id>', methods=['PUT'])
def update_clan(id):
    clan = Clan.query.get_or_404(id)
    data = request.json
    clan.ime = data.get('ime', clan.ime)
    clan.prezime = data.get('prezime', clan.prezime)
    clan.email = data.get('email', clan.email)
    db.session.commit()
    return jsonify({"msg": "Član ažuriran"}), 200

@app.route('/api/treneri', methods=['GET', 'POST'])
def handle_treneri():
    if request.method == 'POST':
        data = request.json
        db.session.add(Trener(ime=data['ime'], prezime=data['prezime'], email=data['email']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '', type=str)

    upit = Trener.query
    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Trener.ime.ilike(pojam),
            Trener.prezime.ilike(pojam),
            Trener.email.ilike(pojam)
        ))
    
    upit = upit.order_by(Trener.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [t.to_dict() for t in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })

@app.route('/api/treneri/<int:id>', methods=['DELETE'])
def delete_trener(id):
    trener = Trener.query.get_or_404(id)
    db.session.delete(trener)
    db.session.commit()
    return jsonify({"msg": "Trener obrisan"}), 200

@app.route('/api/treneri/<int:id>', methods=['PUT'])
def update_trener(id):
    trener = Trener.query.get_or_404(id)
    data = request.json
    trener.ime = data.get('ime', trener.ime)
    trener.prezime = data.get('prezime', trener.prezime)
    trener.email = data.get('email', trener.email)
    db.session.commit()
    return jsonify({"msg": "Trener ažuriran"}), 200

@app.route('/api/oprema', methods=['GET', 'POST'])
def handle_oprema():
    if request.method == 'POST':
        data = request.json
        db.session.add(Oprema(naziv=data['naziv'], stanje=data['stanje']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '', type=str)

    upit = Oprema.query
    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Oprema.naziv.ilike(pojam),
            Oprema.stanje.ilike(pojam)
        ))
    
    upit = upit.order_by(Oprema.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [o.to_dict() for o in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })

@app.route('/api/oprema/<int:id>', methods=['DELETE'])
def delete_oprema(id):
    oprema = Oprema.query.get_or_404(id)
    db.session.delete(oprema)
    db.session.commit()
    return jsonify({"msg": "Oprema obrisana"}), 200

@app.route('/api/oprema/<int:id>', methods=['PUT'])
def update_oprema(id):
    oprema = Oprema.query.get_or_404(id)
    data = request.json
    oprema.naziv = data.get('naziv', oprema.naziv)
    oprema.stanje = data.get('stanje', oprema.stanje)
    db.session.commit()
    return jsonify({"msg": "Oprema ažurirana"}), 200


@app.route('/api/treninzi', methods=['GET', 'POST'])
def handle_treninzi():
    if request.method == 'POST':
        data = request.json
        dt = datetime.strptime(data['datum'], '%Y-%m-%dT%H:%M')
        db.session.add(Trening(naziv=data['naziv'], datum=dt, clan_id=data['clan_id'], trener_id=data['trener_id']))
        db.session.commit()
        return jsonify({"msg": "Dodano"}), 201
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '', type=str)

    upit = Trening.query
    if q:
        pojam = f"%{q}%"
        upit = upit.filter(Trening.naziv.ilike(pojam))
    
    upit = upit.order_by(Trening.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [t.to_dict() for t in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })

@app.route('/api/treninzi/<int:id>', methods=['DELETE'])
def delete_trening(id):
    trening = Trening.query.get_or_404(id)
    db.session.delete(trening)
    db.session.commit()
    return jsonify({"msg": "Trening obrisan"}), 200

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

@app.route('/api/statistika', methods=['GET'])
def get_statistika():
    return jsonify({
        "clanovi": Clan.query.count(),
        "treneri": Trener.query.count(),
        "oprema": Oprema.query.count(),
        "treninzi": Trening.query.count()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)