from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

# TODO Type the URL for your MongoDB cluster
client = MongoClient('mongodb+srv://raresnica85_db_user:mbDWJ1KXhAkWnzA5@cluster0.iemrgjk.mongodb.net/?appName=Cluster0')
db = client["magazin"]
produse = db["produse"]
clienti = db["clienti"]


def _parse_object_id(id_str: str):
    try:
        return ObjectId(id_str), None
    except Exception:
        return None, jsonify({"error": "Invalid ObjectId"}), 400


def _json_body_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, jsonify({"error": "Body must be a JSON object"}), 400
    data.pop("_id", None)
    return data, None


def _get_one(coll, oid):
    entry = coll.find_one({"_id": oid})
    if not entry:
        return jsonify({"error": "Not found"}), 404
    return dumps(entry), 200


def _get_all(coll):
    return dumps(coll.find()), 200


def _add_one(coll):
    data, err = _json_body_object()
    if err:
        return err
    result = coll.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201


def _update_one(coll, oid):
    data, err = _json_body_object()
    if err:
        return err
    if not data:
        return jsonify({"error": "No fields to update"}), 400

    result = coll.update_one({"_id": oid}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Not found"}), 404

    return dumps(coll.find_one({"_id": oid})), 200


def _delete_one(coll, oid, id_str):
    result = coll.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True, "_id": id_str}), 200


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'REST API is running',
        'endpoints': {
            'produse': {
                'GET': ['/produse'],
                'POST': ['/produse'],
                'GET (one)': ['/produse/<id>'],
                'PUT/PATCH': ['/produse/<id>'],
                'DELETE': ['/produse/<id>'],
            },
            'clienti': {
                'GET': ['/clienti'],
                'POST': ['/clienti'],
                'GET (one)': ['/clienti/<id>'],
                'PUT/PATCH': ['/clienti/<id>'],
                'DELETE': ['/clienti/<id>'],
            },
        }
    }), 200

@app.route('/produse', methods=['GET'])
def get_all_produse():
    return _get_all(produse)

@app.route('/produse/<id>', methods=['GET'])
def get_one_produs(id):
    oid, err = _parse_object_id(id)
    if err:
        return err
    return _get_one(produse, oid)

@app.route('/produse', methods=['POST'])
def add_produs():
    return _add_one(produse)

@app.route('/produse/<id>', methods=['PUT', 'PATCH'])
def update_produs(id):
    oid, err = _parse_object_id(id)
    if err:
        return err
    return _update_one(produse, oid)

@app.route('/produse/<id>', methods=['DELETE'])
def delete_produs(id):
    oid, err = _parse_object_id(id)
    if err:
        return err
    return _delete_one(produse, oid, id)


@app.route('/clienti', methods=['GET'])
def get_all_clienti():
    return _get_all(clienti)

@app.route('/clienti/<id>', methods=['GET'])
def get_one_client(id):
    oid, err = _parse_object_id(id)
    if err:
        return err
    return _get_one(clienti, oid)

@app.route('/clienti', methods=['POST'])
def add_client():
    return _add_one(clienti)

@app.route('/clienti/<id>', methods=['PUT', 'PATCH'])
def update_client(id):
    oid, err = _parse_object_id(id)
    if err:
        return err
    return _update_one(clienti, oid)

@app.route('/clienti/<id>', methods=['DELETE'])
def delete_client(id):
    oid, err = _parse_object_id(id)
    if err:
        return err
    return _delete_one(clienti, oid, id)

if __name__ == '__main__':
    app.run(debug=True)
