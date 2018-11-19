from flask import Flask, render_template, Response, request, flash, jsonify
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    nama = request.form['nama']    
    ulasan = request.form['ulasan']
    model_nama = pickle.load(open('model/model_nama.pkl', 'rb'))
    model_rating = pickle.load(open('model/model_rating.pkl', 'rb'))
    gender = model_nama.predict([nama])
    if gender[0] == 1.0 :
        gender = 'male'
    else :
        gender = 'female'
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
