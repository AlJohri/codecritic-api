import os
from flask import Flask, jsonify
app = Flask(__name__)

from codecritic import do_cmd

@app.route("/")
@app.route("/home")
def home():
    return jsonify(**do_cmd("home")['statistics'])

@app.route("/remaining")
def remaining():
    return jsonify(**do_cmd("show-exerciselist"))

@app.route("/exercises")
def exercises():
    remaining_exercises = do_cmd("show-exerciselist")
    completed_exercises = {exercise['Ex Name']:-1 for exercise in do_cmd("home")['submissions']}
    return jsonify(**dict(remaining_exercises.items() + completed_exercises.items()))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)