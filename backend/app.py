import bs4
import requests
import logging

from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError

app = Sanic()
URL = "http://222.194.15.1:7777/pls/wwwbks/bks_login2.login?jym2005=9774.750628820788"
ALL_COURSES = "http://222.194.15.1:7777/pls/wwwbks/bkscjcx.yxkc"
COLS = ["number", "name", "sid", "credit", "test_date", "expt_score", "daily_work", "midterm_score", "exam_results", \
        "total_mark", "alt_c_number", "course_type", "ps"]

def filter_by_class(element):
    for children in element.children:
        if isinstance(children, bs4.element.Tag):
            if children.name == "td":
                try:
                    _class = children['class']
                    if _class[0] == "td_biaogexian":
                        return True
                except KeyError as e:
                    return False

def scriping(params):
    try:
        session = requests.Session()
        session.post(URL, data=params)
        request = session.get(ALL_COURSES)
        return bs4.BeautifulSoup(request.text, 'lxml')
    except Exception as e:
        logging.exception(e)
        raise

def parser_course(element, all_courses):

    s_course = dict()
    index = 0
    for i in element.children:
        if isinstance(i, bs4.element.Tag):
            for j in i.contents:
                s_course[COLS[index]] = j.string if j.string else 0
                index += 1
    dup = all_courses.get(s_course['number'], False)
    if not dup:
        all_courses[s_course['number']] = {
            "number":s_course['number'],
            "name":s_course['name'],
            "_checked": True,
            "credit": s_course['credit'],
            "test_date": s_course['test_date'],
            "score":s_course['total_mark'],
            "course_type": 1 if s_course['course_type'] == "考试" else 0,
        }
    else:
        if int(s_course['total_mark']) >= int(all_courses[s_course['number']]['score']):
            all_courses[s_course['number']]['test_date'] = s_course['test_date']
            all_courses[s_course['number']]['score'] = s_course['total_mark']


def get_courses(params):
    all_courses = dict()
    try:
        for course in scriping(params).find_all("tr"):
            if filter_by_class(course):
                parser_course(course, all_courses)
        response = sorted(list(all_courses.values()), key=lambda item: int(item['test_date']))
        response.reverse()

    except Exception as e:
        reponse = "Failed to get the data."
        logging.exception(e)
    finally:
        return response

@app.post("/v1/courses")
async def test(request): 
    try:
        params = request.json
    except Exception as e:
        raise ServerError("Invlid request", status_code=500)   
    return json({
	    "courses":get_courses(params)
	})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181)

