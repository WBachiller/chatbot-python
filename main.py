#from bson.json_util import dumps, ObjectId

from flask import Flask, request
from flask import jsonify
from training import *
from chatbot import *
from firebase import firebase
import json



firebase = firebase.FirebaseApplication("https://chatbot-ba490-default-rtdb.firebaseio.com/", None)
app = Flask(__name__)

@app.route('/api/v1/intents',  methods=['GET'])
def index():
    response = firebase.get('/intents', '')
    return jsonify(response)


@app.route('/api/v1/intents',  methods=['POST'])
def store():
    json = request.get_json(force=True)
    resultado = firebase.post('intents', json)
    return jsonify(resultado)

@app.route('/api/v1/intents/<id>',  methods=['GET'])
def show(id):
    response = firebase.get(f"/intents/{id}", '')
    return jsonify(response)

@app.route('/api/v1/intents/<id>',  methods=['PUT'])
def update(id):
    json = request.get_json(force=True)
    response = firebase.put(f"/intents/{id}/intents", 'intents', f"{json['intents']}")
    return response




@app.route('/api/v1/intents/traning/<id>',  methods=['GET'])
def load(id):
    response = firebase.get('/intents', '')
    data = json.dumps(response[id])
    training(data, id)
    return jsonify({'success':  200, "message": "services ok" })

@app.route('/api/v1/intents/converstion/<id>',  methods=['POST'])
def initials(id):
    response = firebase.get('/intents', '')
    data = json.dumps(response[id])
    jsondata = request.get_json(force=True)
    respusta = conversation(data, jsondata['message'], id)
    return jsonify({'success':  200, "message": "services ok", "data" : {"response": respusta, "question": jsondata['message'] } })

