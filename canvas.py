import requests, base64, lxml.html, os, pickle, logging

logging.getLogger("requests").setLevel(logging.DEBUG)

if not os.path.isfile("canvas.pickle"):
  s = requests.Session()
  response = s.get("https://canvas.northwestern.edu")
  login_payload = {
    "IDToken0": "",
    "IDToken1": os.getenv('NETID'),
    "IDToken2": os.getenv('PASSWORD'),
    "IDButton": "Log In",
    "goto": base64.b64encode("https://fed.it.northwestern.edu/idp/Authn/RemoteUser"),
    "SunQueryParamsString": "",
    "encoded": "true",
    "gx_charset": "UTF-8"
  }
  response = s.post("https://websso.it.northwestern.edu/amserver/UI/Login", data=login_payload)
  doc = lxml.html.fromstring(response.content)
  saml_payload = {
    "SAMLResponse": doc.cssselect("input[name=SAMLResponse]")[0].get('value')
  }
  response = s.post("https://canvas.northwestern.edu/saml_consume", data=saml_payload)
  response = s.get("https://canvas.northwestern.edu/courses/3107/modules/items/28628")
  doc = lxml.html.fromstring(response.content)
  codecritic = doc.cssselect("#tool_form")[0]
  codecritic_payload = {i.get('name'):i.get('value') for i in codecritic.cssselect("input")}
  response = s.post("https://lyonesse.cs.northwestern.edu:8443/Submitter/", data=codecritic_payload)
  pickle.dump(s, open("canvas.pickle", "wb"))
else:
  s = pickle.load(open("canvas.pickle", "rb"))

SESSION_EXPIRED = "Your Code Critic session has been closed."
state = lambda response, state_string: state_string in response.text

response = s.get("https://lyonesse.cs.northwestern.edu:8443/Submitter/student/reviewer.do")
doc = lxml.html.fromstring(response.content)

queue_size = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[0].text_content().split("; ")[-1].replace(" (all)", "")
you_can_submit = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[1].text_content()
most_recent_review_time = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[2].text_content()

print queue_size
print you_can_submit
print most_recent_review_time

if state(response, SESSION_EXPIRED):
  s = None
  os.remove("canvas.pickle")

with open("test.html", "w") as f:
  f.write(response.text.encode('utf-8'))
