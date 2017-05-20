import json
import requests
import html
import re
from datetime import date

#Module for handling queries to the SFU Course Outlines API.
#API URL: http://www.sfu.ca/bin/wcm/course-outlines

#fetches data and returns a dictionary
def get_outline(dept, num, sec, year = 'current', term = 'current'):
    #setup params
    params = "?{0}/{1}/{2}/{3}/{4}".format(year, term, dept, num, sec)
    #api request
    response = requests.get("http://www.sfu.ca/bin/wcm/course-outlines" + params)
    return response.json()

#fetches sections and returns a dictionary
def get_sections(dept, num, year = 'current', term = 'current'):
    #setup params
    params = "?{0}/{1}/{2}/{3}/".format(year, term, dept, num)
    #api request
    response = requests.get("http://www.sfu.ca/bin/wcm/course-outlines" + params)
    return response.json()

#returns a string containing the first section number with "LEC" as the sectionCode
def find_section(dept, num, year = 'current', term = 'current'):
    #fetch data
    data = get_sections(dept, num, year, term)
    try:
        for sec in data:
            if sec['sectionCode'] == "LEC":
                return sec['value']
    except TypeError:
        return None
    except KeyError:
        return None

#returns a course outline JSON Dictionary
def get_outline(dept, num, sec='placeholder', year = 'current', term = 'current'):
    if sec == 'placeholder':
        sec = find_section(dept, num, year, term)
        if sec == None:
            return "Error finding section"

    data = get_outline(dept, num, sec, year, term)
    return data

#formats the outline JSON into readable string
def format_outline(data:dict):
    if data['info']['deliveryMethod'] == "In Person":
        return format_outline_inperson(data)
    else:
        return format_outline_distance(data)

#formatter for distance ed courses
def format_outline_distance(data:dict):
    #data aliases
    info = data['info']
    instructor = data['instructor']
    exam = data['examSchedule']

    #set up variable strings
    outlinepath = info['outlinePath'].upper()
    courseTitle = "{} ({})".format(info['title'], info['units'])
    prof = ""
    for i in instructor:
        prof += "{} ({})\n".format(i['name'], i['email'])
    examtime = ""
    for time in exam:
        try:
            if time['isExam']:
                examtime += "{} {} - {}\n{} {}, {}\n".format(
                    time['startDate'].split(" 00", 1)[0],
                    time['startTime'],
                    time['endTime'],
                    time['buildingCode'],
                    time['roomNumber'],
                    time['campus'])
        except KeyError:
            #TBA I guess
            examtime = "TBA\n"
            break
    description = info['description']

    #setup final formatting
    doc = """Outline for: {}
Course Title: {}
Instructor: {}
Exam Time:
{}
Description: {}""".format(\
        outlinepath,
        courseTitle,
        prof,
        examtime,
        description)
    return doc


#formatter for inperson courses
def format_outline_inperson(data:dict):
    #data aliases
    info = data['info']
    instructor = data['instructor']
    schedule = data['courseSchedule']
    exam = data['examSchedule']

    #set up variable strings
    outlinepath = info['outlinePath'].upper()
    courseTitle = "{} ({})".format(info['title'], info['units'])
    prof = ""
    for i in instructor:
        prof += "{} ({})\n".format(i['name'], i['email'])
    classtimes = ""
    for time in schedule:
        classtimes += "{} {} - {}\n{} {}, {}\n".format(
            time['days'],
            time['startTime'],
            time['endTime'],
            time['buildingCode'],
            time['roomNumber'],
            time['campus'])
    examtime = ""
    for time in exam:
        try:
            if time['isExam']:
                examtime += "{} {} - {}\n{} {}, {}\n".format(
                    time['startDate'].split(" 00", 1)[0],
                    time['startTime'],
                    time['endTime'],
                    time['buildingCode'],
                    time['roomNumber'],
                    time['campus'])
        except KeyError:
            #TBA I guess
            examtime = "TBA\n"
            break
    description = info['description']

    #setup final formatting
    doc = """Outline for: {}
Course Title: {}
Instructor: {}
Class Times:
{}
Exam Time:
{}
Description: {}""".format(\
        outlinepath,
        courseTitle,
        prof,
        classtimes,
        examtime,
        description)
    return doc
