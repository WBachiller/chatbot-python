
import random
import json
import pickle


import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

def clean_up_sentece(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, name_chatbot):
    words = pickle.load(open('words/'+name_chatbot+'-words.pkl', 'rb'))
    sentence_words = clean_up_sentece(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(filename, sentence, name_chatbot):
    classes = pickle.load(open('classes/'+name_chatbot+'-classes.pkl', 'rb'))

    model = load_model('models/'+name_chatbot+'.model')


    bow = bag_of_words(sentence, name_chatbot)

    res = model.predict(np.array([bow]))[0]
    ERROR_TRESHOLD = 0.25

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_TRESHOLD]
    results.sort(key= lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if i['tag'] == tag:
            result = {}
            result['items'] = i
            result['items']['responses'] = random.choice(i['responses'])
            result['items'].pop('patterns')
            break
    return result

def conversation(filename, message, name_chatbot):
    intents = json.loads(filename)
    ints = predict_class(filename, message, name_chatbot)
    return get_response(ints, intents)

