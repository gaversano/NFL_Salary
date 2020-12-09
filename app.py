# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

import pandas as pd
#from joblib import load
import pickle
from tensorflow import keras
import sklearn

#Read data and format
#Purpose is to (1) get list of available players/teams and (2) look up player details for the model prediction 
data = pd.read_csv("madden21_ratings.csv")
#Formatting
data.rename(columns={' Total Salary ': 'Total Salary', ' Signing Bonus ': 'Signing Bonus'}, inplace=True)
data['Total Salary'] = data['Total Salary'].replace({'\$': '', ',': '','-':'0'}, regex=True).astype(float)
data['Signing Bonus'] = data['Signing Bonus'].replace({'\$': '', ',': '','-':'0'}, regex=True).astype(float)

# A welcome message to test our server
@app.route('/')
def index():  
    #Player names and NFL teams for drop down menu 
    names = data["Full Name"].unique()
    teams = data["Team"].unique()
    
    return render_template('index.html', names = names, teams = teams)

@app.route('/results.html', methods=['POST'])
def results():
    if request.method == 'POST':
             
        name = request.form['player_name']
        team = request.form['player_team']
        
        #Filter data for Player of choice
        player_stats = data[data["Full Name"] == name]
        
        #Get the current salary from the dataset 
        current_salary = round(player_stats["Total Salary"].values[0]/1_000_000,2)
        
        #Extract relevant features from the dataset
        #Team and all numeric features
        #Future improvement: user can change these
        X = player_stats[["Team","Overall Rating", "Age", "Speed",'Strength', 'Throw Power', 'Release', 'Stamina', 'Pursuit', 'Toughness', 'Kick Accuracy', 'Injury', 'Signing Bonus']]
        X["Signing Bonus"] = X["Signing Bonus"]/1_000_000
        
        #Set the team as per drop down choice 
        X["Team"] = team
        
        
        #Load data processing pipline
        #Scaling and one hot encoding
        pipline_file = open('final_data_pipeline.pkl', 'rb')
        data_pipline = pickle.load(pipline_file)
        pipline_file.close()
        
        #transform the data to prep for prediction
        X_prepared = data_pipline.transform(X)
        
        #Load the model 
        model = keras.models.load_model('final_NN_model.h5')
        
        #Make prediction 
        predicted_salary = round(model.predict(X_prepared)[0][0],2)
        
        return render_template('results.html', name=name, team=team, predicted_salary=predicted_salary,current_salary=current_salary)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
