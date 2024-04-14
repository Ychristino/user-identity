import requests
from flask import Flask, render_template
from application.backend.controllers.activity_controller import ActivityController

app = Flask(__name__)


def get_activity_list_from_api():
    response = requests.get('http://127.0.0.1:5000/activities')
    if response.status_code == 200:
        data = response.json()['data']
        return [(item['label'], item['value']) for item in data]
    else:
        return []


def get_user_list_from_api():
    response = requests.get('http://127.0.0.1:5000/users_list')
    if response.status_code == 200:
        data = response.json()['data']
        return [(item['username']) for item in data]
    else:
        return []


def get_model_list_from_api():
    response = requests.get('http://127.0.0.1:5000/models')
    if response.status_code == 200:
        data = response.json()['data']
        return [(item['label'], item['value']) for item in data]
    else:
        return []


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/record')
def record():
    return render_template('record_data.html', activities_list=get_activity_list_from_api())


@app.route('/view')
def view():
    return render_template('view_data.html', user_list=get_user_list_from_api())


@app.route('/execute_model')
def execute_model():
    return render_template('execute_model.html', model_list=get_model_list_from_api(), activities_list=get_activity_list_from_api())


if __name__ == '__main__':
    app.run(port=5001, debug=True)
