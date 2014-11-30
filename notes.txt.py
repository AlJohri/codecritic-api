# TODO: 
# - differentiate between parameters of a request or URL path ie. /path/x vs /path?cmd=x
# - add default values for parameters
# - mark whether parameters are required

API = [{
  "student": [{
    "reviewer.do": [
      ('GET', "show-student-statistics"), 
      ('GET', "show-exerciselist"), 
      ('GET', {"show-submitter": ["exid", "exname"]}), # both required
      ('GET', {"show-critiques": ["code_id", "user", "exid", "exname"]}), # only code_id required
      ('GET', {"show-code": ["code_id"]}), # only code_id required
      ('POST', {"show-exs": [("code_id", -1), ("address", "al.johri@gmail.edu")]})
      ('POST', {"submit-ex": ["author", "exname", "exname", "exid", "code"]}),
      ('POST', {"retract": ["code_id"]}), # only code_id required
      ('POST', {"update-email": ["address"]}),
    ]
  }],
  "instructor": [{
    "reviewer.do": [
      ('GET', "show-critique-manager"),
      ('GET', "show-assessments"),
      ('GET', "show-student-statistics"),
      ('GET', "show-history"),
      ('GET', "show-exmgr")
    ],
    "critique-topics.jsp"
  }],
  "courseadmin": [{
    "admin.do": [
      ('GET', "view-courses")
    ]
  }]
}]

