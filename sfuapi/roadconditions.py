import json
import requests
import html
import re
#Module for reading from the SFU Road Conditions API
#Returns pretty formatted plaintext strings for whatever use.
#API URL: http://www.sfu.ca/security/sfuroadconditions/api/2/current


def get():
    #returns a dictionary with the data retrieved from the api call
    response = requests.get("http://www.sfu.ca/security/sfuroadconditions/api/2/current")
    return response.json()


def announcements():
    #fetch data
    data = get()
    #extract string
    str = data["announcements"][0]
    #fix html entities
    str = html.unescape(str)
    #fix html tags
    str = re.sub('<[^<]+?>', '', str)
    return str


def conditions(campus = "burnaby"):
    #fetch data
    data = get()
    #start building return string
    doc = "{0} road conditions\n".format(campus.capitalize())
    try:
        for aspect, status in data["conditions"][campus].items():
            doc += "{0}: ".format(aspect.capitalize())
            for name, condition in status.items():
                 doc += "{0} => {1}, ".format(name, condition)
            doc = doc[:-2]
            doc += "\n"
    except KeyError:
        doc = "Campus {0} not found.".format(campus.capitalize())

    return doc
