from flask import Flask, render_template, make_response
import os
import time
from flask_cors import CORS, cross_origin
from Workout import Workout
from flask import request

app = Flask(__name__, template_folder='template')
cors = CORS(app)


def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)


@app.route('/getAllLaps', methods=['POST'])
def all():
    req_body = request.json
    workout = Workout(req_body)
    workout.setup_sets()
    laps = workout.get_laps()
    return laps


@app.route('/getAvgLaps', methods=['POST'])
def avg():
    req_body = request.json
    avg_workout = Workout(req_body)

    avg_workout.setup_sets()
    avg_workout.do_workout_analisys()

    return avg_workout.make_json()


@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
