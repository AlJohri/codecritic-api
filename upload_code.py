import json
from canvas import authenticated_request

exercises = json.load(open("exercises.json"))

AUTHOR_ID = 899
EXNAME = ""
CODE = """
"""

payload = {
	"cmd": "submit-ex",
	"author": AUTHOR_ID,
	"exname": EXNAME,
	"exid": exercises[EXNAME],
	"code": CODE
}

response = authenticated_request("https://lyonesse.cs.northwestern.edu:8443/Submitter/student/reviewer.do", data=payload)
print response.content