import lxml.html, os, json
from canvas import login, state, SESSION_EXPIRED
from urlparse import urlparse, parse_qsl

s = login()
response = s.get("https://lyonesse.cs.northwestern.edu:8443/Submitter/student/reviewer.do?cmd=show-exerciselist")
doc = lxml.html.fromstring(response.content)
exercises_list = [dict(parse_qsl(urlparse(x.get('href')).query)) for x in doc.cssselect("table tr td a")]
exercises_dict = {exercise['exname']:exercise['exid'] for exercise in exercises}
json.dump(exercises_dict, open("exercises.json", "w"), sort_keys=True, indent=4)
print exercises_dict