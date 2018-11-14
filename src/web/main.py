from flask import Flask, render_template, Response, request, flash, jsonify
import pickle
import sklearn
# from script.parseImg import *

app = Flask(__name__)

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
    rating = model_rating.predict([ulasan])
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
