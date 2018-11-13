from flask import Flask, render_template, Response, request, flash, jsonify
# from script.parseImg import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    nama = request.form['nama']    
    ulasan = request.form['ulasan']    
    return jsonify({'rating' : 4})
