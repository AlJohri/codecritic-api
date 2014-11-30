import requests, lxml.html, os, pickle, json, logging, datetime, argparse
from urlparse import urlparse, parse_qsl
from pprint import pprint as pp
from canvas import authenticated_request

# http://stackoverflow.com/a/2990151/1667241
from itertools import izip_longest
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def parse_home(response, *args):
  doc = lxml.html.fromstring(response.content)
  queue_size = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[0].text_content().split("; ")[-1].replace(" (all)", "")
  you_can_submit = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[1].text_content().replace("\r\n", "").replace(" ", "")
  most_recent_review_time = doc.cssselect("h2")[0].getnext().cssselect("tr:nth-child(3) th")[2].text_content()

  statistics_table = doc.cssselect("table")[0]
  statistics = {}
  for row in statistics_table.cssselect("tr"):
    for header, cell in grouper(2, row.getchildren()):
      if unicode(header.text_content()) in [u"", u"\xa0"]: continue
      statistics[header.text_content()] = cell.text_content().strip()

  submissions_table = doc.cssselect("table#submissions")[0]
  headers = [header.text_content() for header in submissions_table.cssselect("thead tr th")]
  submissions = []
  for row in submissions_table.cssselect("tbody tr"):
    result = {}
    for i, cell in enumerate(row.cssselect("td")):
      result[headers[i]] = cell.text_content().strip()
      if cell.cssselect("a"):
        result[headers[i] + " Link"] = cell.cssselect('a')[0].get('href')
      submissions.append(result)

  return {"statistics": statistics, "submissions": submissions}

def parse_exerciselist(response, *args):
  doc = lxml.html.fromstring(response.content)
  exercises_list = [dict(parse_qsl(urlparse(x.get('href')).query)) for x in doc.cssselect("table tr td a")]
  exercises_dict = {exercise['exname']:exercise['exid'] for exercise in exercises_list}
  json.dump(exercises_dict, open("exercises.json", "w"), sort_keys=True, indent=4)
  return exercises_dict

def parse_student_statistics(response, *args):
  doc = lxml.html.fromstring(response.content)
  table = doc.cssselect("#stats_table")[0]
  headers = [header.text_content() for header in table.cssselect("thead tr th")]
  results = [{headers[i]: cell.text_content() for i, cell in enumerate(row.cssselect("td"))} for row in table.cssselect("tbody tr")]
  return results

def parse_code(response, *args):
  doc = lxml.html.fromstring(response.content)
  return unicode(doc.cssselect("blockquote")[0].text_content())

# see notes.txt.py
parse = {
  "home": parse_home,
  "show-student-statistics": parse_student_statistics,
  "show-exerciselist": parse_exerciselist,
  "show-code": parse_code,
}

def do_cmd(cmd, *args):
  params = {name: value for name, value in grouper(2, args)}
  url = "https://lyonesse.cs.northwestern.edu:8443/Submitter/student/reviewer.do?cmd=%s" % (cmd if cmd != "home" else "")
  response = authenticated_request(url, params=params)
  result = parse[cmd](response, *args)
  return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_known_args()

    result = do_cmd(args[0].cmd, *args[1])
    if type(result) in [str, unicode]: print(result)
    else: pp(result)
