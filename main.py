#from bson.json_util import dumps, ObjectId

from flask import Flask, request, make_response
from flask import jsonify
from training import *
from chatbot import *
from firebase import firebase
import json
from flask_cors import CORS, cross_origin
import requests



firebase = firebase.FirebaseApplication("https://chatbot-ba490-default-rtdb.firebaseio.com/", None)
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/api": {"origins": "http://localhost:4200"}})




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
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def initials(id):
    firebasejson = firebase.get('/intents', '')
    data = json.dumps(firebasejson[id])
    jsondata = request.get_json(force=True)
    if jsondata['next_param'].lower() == '':
        message = jsondata['message'].lower()
        respuesta = conversation(data, jsondata['message'].lower(), id)
    else:
        message = jsondata['next_param'].lower()
        respuesta = conversation(data, jsondata['next_param'].lower(), id)
        print(respuesta['items']['webhook'])
        if respuesta['items']['webhook']:
            res = requests.post(f"http://inventario.test/api/v1/{respuesta['items']['url']}", json={'message': jsondata['message'].lower()})
            como_json = res.json()
            respuesta['items']['type']  = como_json['type']
            respuesta['items']['options']  = como_json['options']
            respuesta['items']['responses'] = como_json['message']
            respuesta['items']['next_patterns'] = como_json['next_patterns']



    return jsonify({'success': 200, "message": "services ok", "data": {"response": respuesta, "question": jsondata['message']}})

