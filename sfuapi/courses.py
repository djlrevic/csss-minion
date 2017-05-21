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
            if sec['sectionCode'] == "LEC" or sec['sectionCode'] == "LAB":
                return sec['value']
    except Exception:
        return None

#returns a course outline JSON Dictionary
def find_outline(dept, num, sec='placeholder', year = 'current', term = 'current'):
    if sec == 'placeholder':
        sec = find_section(dept, num, year, term)
        if sec == None:
            return None

    #print("sec = "  + sec)
    data = get_outline(dept, num, sec, year, term)
    return data

#pulls data from outline JSON Dict
def extract(data:dict):
    #data aliases
    try:
        info = data['info']

        schedule = data['courseSchedule']

    except Exception:
        return ["Error: Maybe the class doesn't exist? \nreturned data:\n" + json.dumps(data)]

    #set up variable strings
    outlinepath = "{}".format(info['outlinePath'].upper())
    courseTitle = "{} ({})".format(info['title'], info['units'])
    prof = ""
    try:
        for i in data['instructor']:
            prof += "{} ({})\n".format(i['name'], i['email'])
    except Exception:
        prof = "Unknown"

    classtimes = ""
    for time in schedule:
        classtimes += "[{}] {} {} - {}, {} {}, {}\n".format(
            time['sectionCode'],
            time['days'],
            time['startTime'],
            time['endTime'],
            time['buildingCode'],
            time['roomNumber'],
            time['campus'])
    examtime = ""
    try:
        for time in data['examSchedule']:
            if time['isExam']:
                examtime += "{} {} - {}\n{} {}, {}\n".format(
                    time['startDate'].split(" 00", 1)[0],
                    time['startTime'],
                    time['endTime'],
                    time['buildingCode'],
                    time['roomNumber'],
                    time['campus'])
    except Exception:
        #TBA I guess
        examtime = "TBA\n"
    description = info['description']
    try:
        details = info['courseDetails']
        #fix html entities
        details = html.unescape(details)
        #fix html tags
        details = re.sub('<[^<]+?>', '', details)
        #truncate
        limit = 200
        details = (details[:limit] + " (...)") if len(details) > limit else details

    except Exception:
        details = ""
    try:
        prereq = info['prerequisites']
    except Exception:
        prereq = ""

    try:
        coreq = info['corequisites']
    except Exception:
        coreq = ""
    return [outlinepath, courseTitle, prof, classtimes, examtime, description, details, prereq, coreq]

#formats the outline JSON into readable string
def format_outline(data:dict):
    strings= extract(data)

    if len(strings) == 1:
        return strings[0]

    outlinepath, courseTitle, prof, classtimes, examtime, description, details, prereq, coreq = strings
    #setup final formatting
    doc = ""
    doc += "Outline for: {}\n".format(outlinepath)
    doc += "Course Title: {}\n".format(courseTitle)
    doc += "Instructor: {}\n".format(prof)
    if classtimes != "":
        doc += "Class Times:\n{}\n".format(classtimes)
    doc += "Exam Time:\n{}\n".format(examtime)

    doc += "Description:\n{}\n\n".format(description)
    if details != "":
        doc += "Details:\n{}\n\n".format(details)
    if prereq != "":
        doc += "Prerequisites: {}\n".format(prereq)
    if coreq != "":
        doc += "Corequisites: {}\n".format(prereq)

    return doc

#returns a fairly nicely formatted string for easy reading
def print_outline(dept, num, sec='placeholder', year = 'current', term = 'current'):
    data = find_outline(dept, num, sec, year, term)
    return format_outline(data)

#returns a dictionary with relevant information or a string if something went wrong
def dict_outline(dept, num, sec='placeholder', year = 'current', term = 'current'):
    data = find_outline(dept, num, sec, year, term)
    #print(data)
    strings = extract(data)
    #print(strings)
    if len(strings) == 1:
        return {
            'Error': strings[0]
        }
    #if

    ret = {
        'outline': strings[0],
        'title': strings[1],
        'instructor': strings[2],
        'class times':strings[3],
        'exam time':strings[4],
        'description':strings[5],
        'details':strings[6],
        'prerequisites':strings[7],
        'corequisites':strings[8]
    }
    return ret
