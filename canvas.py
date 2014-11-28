import requests, base64, lxml.html, os, pickle, logging, datetime

logging.getLogger("requests").setLevel(logging.DEBUG)

SESSION_EXPIRED = "Your Code Critic session has been closed."
PASSWORD_INVALID = "The NetID and/or password you entered was invalid."

state = lambda response, state_string: state_string in response.text

def auth(override=False):
  if not os.path.isfile("canvas.pickle") or override:
    print "DEBUG", "redownloading session"
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
    if state(response, PASSWORD_INVALID):
      raise Exception(PASSWORD_INVALID + "\nYou might be missing the NETID and PASSWORD environment variables.")
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
    print "DEBUG", "using cached session"
    s = pickle.load(open("canvas.pickle", "rb"))
  return s

def get_page(s):
  return s.get("https://lyonesse.cs.northwestern.edu:8443/Submitter/student/reviewer.do")  

def parse_page(response):
    doc = lxml.html.fromstring(response.content)
    queue_size = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[0].text_content().split("; ")[-1].replace(" (all)", "")
    you_can_submit = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[1].text_content().replace("\r\n", "").replace(" ", "")
    most_recent_review_time = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[2].text_content()
    return (queue_size, you_can_submit, most_recent_review_time)

def check_queue(s=None):
  print "holler"
  if not s: s = auth()
  response = get_page(s)

  while state(response, SESSION_EXPIRED):
    os.remove("canvas.pickle")
    s = auth(override=False)
    response = get_page()

  queue_size, you_can_submit, most_recent_review_time = parse_page(response)

  print "DEBUG", (queue_size, you_can_submit, most_recent_review_time)

  return (queue_size, you_can_submit, most_recent_review_time)

if __name__ == "__main__":
    check_queue()