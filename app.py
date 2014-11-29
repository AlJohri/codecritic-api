import os
from flask import Flask
app = Flask(__name__)

from canvas import login, check_queue

s = login()

@app.route("/")
def hello():
    queue_size, you_can_submit, most_recent_review_time = check_queue(s)
    return "<br/>".join([queue_size, you_can_submit, most_recent_review_time])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)