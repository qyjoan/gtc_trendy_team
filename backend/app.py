from flask import Flask, jsonify, render_template, request, url_for
from flask.ext.pymongo import PyMongo
from config import init_users_db, init_journeys_db
import json

app = Flask(__name__) 

@app.route('/')
def hello_world():
        print('asdf')
        return 'Hello, World!'

@app.route('/new_user', methods=['POST'])
def create_user(user_key):
    survey_results = request.form['survey_results']

    new_user = json.load('user_profile_template.json')
    new_user['survey_results'] = survey_results
    new_user['journeys'] = []

    i_results = mongo.db.users.insert_one(new_user)
    return i_results.inserted_id


@app.route('/journeys', methods=['GET'])
def get_all_journeys():
    journeys = list(journeys_db.db.test.find())
    for entry in journeys:
        entry.pop('_id')
    return jsonify(journeys)

@app.route('/add_journey', methods=['POST'])
def add_journey():
    username = request.form['user_id']
    journey_id = request.form['journey_id']
    journey = journeys_db.db.test.find_one({'_id': journey_id})
    users_db.db.journeys.update( {'user': username}
                         , {'$push': {'journeys': { "journey": journey
                                                  , "complete": False
                           }}}
                         )

@app.route('/create_journey')
def journey_form():
    return render_template('journey_form.html')

@app.route('/user_journey/<user_id>', methods=['GET'])
def get_user(user_id):
    journey = users_db.db.journey.find_one_or_404({'user': user_id})
    #null check
    journey.pop('_id')
    result = json.dumps(journey)
    return result

@app.route('/user/steve', methods=['GET'])
def get__test_user():
    print("in steve")
    json_data=open('../json_mocks/user_w_journey.json').read()    
    print json_data
    return json_data

@app.route('/update_journey_status', methods=['POST'])
def update_user_status():
    user_id = request.form['user_id']
    user_status = request.form['status']
    mongo.db.users.replace_one({'_id': user_id}, user_status)

if __name__ == "__main__":
    users_db=init_users_db(app)
    journeys_db=init_journeys_db(app)
    app.run(host='0.0.0.0',port=27020, debug=True)

