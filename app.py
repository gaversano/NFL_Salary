# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

import pandas as pd

# A welcome message to test our server
@app.route('/')
def index():
    
    data = pd.read_csv("madden21_ratings.csv")
    
    names = data["Full Name"].unique()
    teams = data["Team"].unique()
    
    return render_template('index.html', names = names, teams = teams)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
