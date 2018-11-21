from flask import Flask, render_template, Response, request, flash, jsonify
import re
import pickle
import sklearn
import pandas as pd
# from script.parseImg import *

app = Flask(__name__)

def bin_count(x):
    if x >= 48:
        return 1
    return 5

def word_count(x):
    return x.apply(lambda x: bin_count(len(x.split()))).values.reshape(-1, 1).astype(int)

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def remove_truk(x):
    return re.sub(r'(\w)\1+', r'\1', x)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    nama = request.form['nama']    
    ulasan = request.form['ulasan']
    
    model_nama = pickle.load(open('model/model_nama.pkl', 'rb'))
    model_rating = pickle.load(open('model/model_rating.pkl', 'rb'))
    kamus_emot = pickle.load(open('kamus_emot.pkl', 'rb'))
    # kamus_oov = pickle.load(open('kamus_oov.pkl', 'rb'))

    ulasan = replace_all(ulasan, kamus_emot)
    # ulasan = replace_all(ulasan, kamus_oov)

    ulasan = remove_truk(ulasan)
    
    gender = model_nama.predict([nama])

    if gender[0] == 1.0 :
        gender = 'male'
        ulasan += ' MMAALLEE'
    else :
        gender = 'female'
        ulasan += ' FFEEMMAALLEE'

    rating = model_rating.predict(pd.Series([ulasan]))

    return jsonify({'rating' : int(rating[0]), 'gender' : gender})

@app.route('/predict_gender', methods=['POST'])
def predict_gender():
    nama = request.form['nama']    
    model_nama = pickle.load(open('model/model_nama.pkl', 'rb'))
    gender = model_nama.predict([nama])
    if gender[0] == 1.0 :
        gender = 'male'
    else :
        gender = 'female'
    return jsonify({'gender' : gender})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8111)
