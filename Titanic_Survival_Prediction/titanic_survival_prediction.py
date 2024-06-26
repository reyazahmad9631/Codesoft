# -*- coding: utf-8 -*-
"""Titanic Survival Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1whCQCQrWczzZOBLgI5AlCZyxvlyyWhyW

Importing the Dependencies
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

"""Data Collection"""

# load the data from csv file to pandas DataFrame
titanic_data = pd.read_csv('/content/Titanic-Dataset.csv')

# printing the first 5 rows of the dataframe
titanic_data.head()

# number of rows and columns
titanic_data.shape

# geeting some informations about the data
titanic_data.info()

# check the number of missing values in each column
titanic_data.isnull().sum()

"""Handling the Missing Values"""

# drop the cabin column from the dataframe
titanic_data = titanic_data.drop(columns='Cabin', axis=1)

# replacing the missing values in "Age" column with mean values
titanic_data['Age'].fillna(titanic_data['Age'].mean(), inplace=True)

# finding the mode values of "Embarked" column
print(titanic_data['Embarked'].mode())

print(titanic_data['Embarked'].mode()[0])

# replacinf the missing values in "Embaerked" column with mode value
titanic_data['Embarked'].fillna(titanic_data['Embarked'].mode()[0], inplace=True)

# check the number of missing values in each column
titanic_data.isnull().sum()

"""Data Analysis"""

# getting some statistical measures about the data
titanic_data.describe()

# finding the number of peoples have survived & not survived
titanic_data['Survived'].value_counts()

"""Data Visualization"""

sns.set()

sns.countplot(x='Survived', data=titanic_data)
plt.show()

titanic_data['Sex'].value_counts()

# making a count plot for "sex" cplumns
sns.countplot(x='Sex', data=titanic_data)
plt.show()

#number of Survivors based on gender
sns.countplot(x='Sex', hue='Survived', data=titanic_data)
plt.show()

# making a count plot for "Pclass" column
sns.countplot(x='Pclass', data=titanic_data)
plt.show()

sns.countplot(x='Pclass', hue='Survived', data=titanic_data)
plt.show()

sns.countplot(x='Embarked', hue='Survived', data=titanic_data)
plt.show()

sns.countplot(x='Age', hue='Survived', data=titanic_data)
plt.show()

"""Encoding the catagorical column  

"""

titanic_data['Sex'].value_counts()

titanic_data['Embarked'].value_counts()

titanic_data.replace({'Sex':{'male':0, 'female':1}, 'Embarked':{'S':0, 'C':1, 'Q':2}}, inplace=True)

titanic_data.head()

"""Seperating features & Target"""

x = titanic_data.drop(columns=['PassengerId', 'Name', 'Ticket', 'Survived'], axis=1)
y = titanic_data['Survived']

print(x)

print(y)

"""Splitting the data into training data & test data"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

print(x.shape, x_train.shape, x_test.shape)

"""Logistic Regression"""

model = LogisticRegression()

# btraing the Logistic Regression model with training data
model.fit(x_train, y_train)

"""Model Evaluvation

Accuracy Score
"""

# accuracy of training data
x_train_prediction = model.predict(x_train)

print(x_train_prediction)

training_data_accuracy = accuracy_score(y_train, x_train_prediction)
print('Accuracy score of training data: ', training_data_accuracy)

# accuracy of test data
x_test_prediction = model.predict(x_test)

print(x_test_prediction)

test_data_accuracy = accuracy_score(y_test, x_test_prediction)
print('Accuracy score of test data: ', test_data_accuracy)

import joblib
joblib.dump(model, 'logistic_regression_model.pkl')

!pip install pyngrok
import subprocess
import os
from pyngrok import ngrok
# setup ngrok with authtoken
ngrok.set_auth_token("2haqDHHZcTzEDY6HjkRFxFB6iU5_4D3B5JtMtt3jtuBh9ZDK")
# running flask app
os.system("nohup python -m flask run --no-reload&")
# opening ngrok tunnel to flask app using http protocol
proc = subprocess.Popen(["ngrok", "http", "5000"])
#Retrive ngrok's public url here
public_url = ngrok.connect(addr="5000", proto="http")
print("Public URL:", public_url)

from flask import Flask, request, jsonify
import joblib
from pyngrok import ngrok
from IPython.display import display, HTML

# Load the trained model
model = joblib.load('logistic_regression_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    # HTML form to take inputs
    html_form = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titanic Survival Prediction</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        #predictionForm {
            display: inline-block;
            text-align: left;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h2>Titanic Survival Prediction</h2>
    <form id="predictionForm" method="post" action="/predict">
        <label for="pclass">Pclass:</label>
        <input type="text" id="pclass" name="pclass"><br><br>

        <label for="sex">Sex (0 for male, 1 for female):</label>
        <input type="text" id="sex" name="sex"><br><br>

        <label for="age">Age:</label>
        <input type="text" id="age" name="age"><br><br>

        <label for="sibsp">SibSp:</label>
        <input type="text" id="sibsp" name="sibsp"><br><br>

        <label for="parch">Parch:</label>
        <input type="text" id="parch" name="parch"><br><br>

        <label for="fare">Fare:</label>
        <input type="text" id="fare" name="fare"><br><br>

        <label for="embarked">Embarked (0 for S, 1 for C, 2 for Q):</label>
        <input type="text" id="embarked" name="embarked"><br><br>

        <button type="button" onclick="predictSurvival()">Predict</button>
    </form>

    <p id="predictionResult"></p>

    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Titanic-Cobh-Harbour-1912.JPG/450px-Titanic-Cobh-Harbour-1912.JPG">

    <script>
        function predictSurvival() {
            var xhr = new XMLHttpRequest();
            var url = "/predict";
            var data = new FormData(document.getElementById("predictionForm")); // Changed to FormData

            xhr.open("POST", url, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    document.getElementById("predictionResult").innerHTML = "Survival Prediction: " + response.prediction;
                }
            };
            xhr.send(data);
        }
    </script>
</body>
</html>

    """
    return html_form

@app.route('/predict', methods=['POST'])
def predict():
    # Access form data
    pclass = request.form['pclass']
    sex = request.form['sex']
    age = request.form['age']
    sibsp = request.form['sibsp']
    parch = request.form['parch']
    fare = request.form['fare']
    embarked = request.form['embarked']

    # Convert data to appropriate types
    pclass = int(pclass)
    sex = int(sex)
    age = float(age)
    sibsp = int(sibsp)
    parch = int(parch)
    fare = float(fare)
    embarked = int(embarked)

    # Make prediction
    features = [[pclass, sex, age, sibsp, parch, fare, embarked]]
    prediction = model.predict(features)[0]

    return jsonify({'prediction': int(prediction)})

def run_flask_app():
    # Run Flask app on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

# Start ngrok tunnel
public_url = ngrok.connect(addr="5000", proto="http")
print("Public URL:", public_url)

# Display ngrok tunnel URL
display(HTML(f"<h2>Open this link in your browser to access the application:</h2><p>{public_url}</p>"))

try:
    # Keep the Flask app running
    run_flask_app()
except KeyboardInterrupt:
    # Shutdown ngrok and Flask app
    ngrok.kill()

