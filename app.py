import os, re
from flask import Flask, jsonify
app = Flask(__name__)

from codecritic import do_cmd

from dateutil.parser import parse

@app.route("/")
@app.route("/home")
def home():
    personal_statistics = do_cmd("home")['statistics']
    last_review = parse(personal_statistics["Instructor's most recent review"]).strftime("%-m/%-d/%y %-I:%M%p")
    queue_size = int(re.findall(r".*; (\d+) \(all\)", personal_statistics["Number of submissions in queue"])[0])
    return jsonify(**{"Instructor's most recent review": last_review, "Number of submissions in queue": queue_size})

@app.route("/remaining")
def remaining():
    return jsonify(**do_cmd("show-exerciselist"))

@app.route("/exercises")
def exercises():
    remaining_exercises = do_cmd("show-exerciselist")
    completed_exercises = {exercise['Ex Name']:-1 for exercise in do_cmd("home")['submissions']}
    return jsonify(**dict(remaining_exercises.items() + completed_exercises.items()))

@app.route("/statistics")
def statistics():
	return jsonify(items=do_cmd("show-student-statistics"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)