# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

import pandas as pd

data = pd.read_csv("madden21_ratings.csv")

# A welcome message to test our server
@app.route('/')
def index():    
    names = data["Full Name"].unique()
    teams = data["Team"].unique()
    
    return render_template('index.html', names = names, teams = teams)

@app.route('/results.html', methods=['POST'])
def results():
    if request.method == 'POST':
        
        name = request.form['player_name']
        team = request.form['player_team']
        
        return render_template('results.html', name = name, team = team)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
