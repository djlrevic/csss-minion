import psycopg2
import urllib.parse
import pickle
from datetime import date , timedelta
import configparser
import plotly
from plotly.graph_objs import Bar, Layout

def saveToFile(obj):
    with open("stats.pck",'wb') as f:
        pickle.dump(obj,f)

def readFromFile():
    with open("stats.pck","rb") as f:
        return pickle.load(f)

def newArrsDict(newDict,oldDict):
    xVals = []
    yVals = []

    for key in newDict:

        if(newDict[key] == oldDict[key]):
            continue

        xVals.append(key)
        #We use the get function so if the person doenst exist yet we just return 0
        yVals.append(newDict[key] - oldDict.get(key,0))

    retArr = sorted(zip(xVals,yVals),key=lambda x : x[1],reverse=True)

    return retArr

def takeSecond(el):
    return el[1]

config = configparser.ConfigParser()
config.read("botMain.settings")

postgrespass = config.get("Postgres", "Password")

database = "experience"  # database name used for exp

urllib.parse.uses_netloc.append("postgres")
conn = psycopg2.connect(
    "port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='" + postgrespass + "'")
cur = conn.cursor()

cur.execute('SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter')
res = list(cur.fetchall())

saveObj = []
saveObj.append([{}])

saveObj = readFromFile();

newVals = {}

#Create a dict/hash
#Key is the id of the user
#Value is the exp
for item in res:
    newVals[item[1]] = item[3]

#Now we draw the graphs
if(len(saveObj) > 0):

    arrVals = newArrsDict(newVals,saveObj[-1])
    xVals,yVals = zip(*arrVals)

    plotly.offline.plot({
        "data": [Bar(x=xVals, y=yVals)],
        "layout": Layout(title="1 Day Diff from : " + str((date.today() - timedelta(1))) + "  to  " + str(date.today()))

    }, filename="oneDayDiff.html")

if(len(saveObj) > 7):
    arrVals = newArrsDict(newVals, saveObj[-7])
    xVals, yVals = zip(*arrVals)

    plotly.offline.plot({
        "data": [Bar(x=xVals, y=yVals)],
        "layout": Layout(title="1 Day Diff from : " + str((date.today() - timedelta(7))) + "  to  " + str(date.today()))

    }, filename="oneWeekDiff.html")

if(len(saveObj) > 30):
    arrVals = newArrsDict(newVals, saveObj[-30])
    xVals, yVals = zip(*arrVals)

    plotly.offline.plot({
        "data": [Bar(x=xVals, y=yVals)],
        "layout": Layout(title="1 Day Diff from : " + str((date.today() - timedelta(30))) + "  to  " + str(date.today()))

    }, filename="oneMonthDiff.html")

saveObj.append(newVals);

saveToFile(saveObj)


