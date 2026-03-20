from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

# TODO Type the URL for your MongoDB cluster
client = MongoClient('mongodb+srv://<user>:<pass>@cluster0.mongodb.net/')
db = client.gettingStarted
collection = db.people

@app.route('/entries', methods=['GET'])
def get_all_entries():
    entries = collection.find()
    return dumps(entries), 200

@app.route('/entries', methods=['POST'])
def add_entry():
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)
