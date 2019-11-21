from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template
from flask_bootstrap import Bootstrap
import os



#from dashapp import server as application

app = Flask(__name__)
bootstrap = Bootstrap(app)

import pandas as pd
from operator import add
from datetime import datetime

data1 = pd.read_csv("csv/Quality_1.csv")
data2 = pd.read_csv("csv/Quality_2.csv")
data3 = pd.read_csv("csv/Quality_3.csv")

data1 = data1.append(data2)
data1 = data1.append(data3)

Q1Count = 0
Q2Count = 0
Q3Count = 0

dt = []

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/analysis')
def analysis():
    soil = pd.read_csv("csv/soil.csv")
    x1 = int(request.args.get('x1'))
    y1 = int(request.args.get('y1'))
    x2 = int(request.args.get('x2'))
    y2 = int(request.args.get('y2'))

    pixels = []
    for i in range(x1, x2):
        for j in range(y1, y2):
            p = "p_" + str(i) + "_" + str(j)
            pixels.append(p)

    data = data1[data1["Pixel ID"].isin(pixels)]
    data["Time Series"][:1]
    data = data.reset_index()
    data = data.drop(columns=['index'])

    print(data)
    dataframe = getData(data)
    d = dataframe.to_json(orient="columns")

    Q1pro = round(Q1Count/(len(data))*10000)/100
    Q2pro = round(Q2Count /(len(data))*10000)/100
    Q3pro = round(Q3Count /(len(data))*10000)/100


    Q1_yeild = (25 / (512 * 512)) * Q1Count * 121
    Q2_yeild = (25 / (512 * 512)) * Q2Count * 119
    Q3_yeild = (25 / (512 * 512)) * Q3Count * 112

    Q1_rate = 430 * 0.009 * (15.5 - 4) + 0.6
    Q2_rate = 430 * 0.009 * (14.5 - 4) + 0.6
    Q3_rate = 430 * 0.009 * (13.5 - 4) + 0.6

    Q1_PE = round(Q1_rate * Q1_yeild*100)/100
    Q2_PE = round(Q2_rate * Q2_yeild*100)/100
    Q3_PE = round(Q3_rate * Q3_yeild*100)/100
    PE = round((Q1_PE + Q2_PE + Q3_PE)*100)/100
    data = data.merge(soil, how="left", on="Pixel ID")

    dataWithDataframe = pd.DataFrame(data.groupby(['Quality Band_x']).mean())
    WithDataframe = dataWithDataframe.to_json(orient="columns")

    return render_template('analysis.html', x1=x1, x2=x2, y1=y1, y2=y2,
                           w =request.args.get('w'), h = request.args.get('h'), d = d, Q1=Q1pro,Q2=Q2pro,Q3=Q3pro, dataframe = WithDataframe,
                           Q1_PE = Q1_PE,
                           Q2_PE = Q2_PE,
                           Q3_PE = Q3_PE,
                           total = PE,
                           TotalLength = len(data))

def ser(x):
    x = x[1:-1]
    x = x.replace(" ", "")
    x = x.split(",")
    x = list(map(float, x))
    return x

def mean_ser(x):
    l1=x["Time Series"][0]

    for i in range(1,len(l1)):
        l2=x["Time Series"][i]
        l1=list(map(add, l1, l2))
    le=len(l1)
    l1 = [x / le for x in l1]
    return l1





def getData(data):
    data["Time Series"] = data["Time Series"].apply(ser)

    Q1 = data[data["Quality Band"] == 1]
    global Q1Count
    Q1Count = len(Q1)
    Q1 = Q1.reset_index()
    Q1 = Q1.drop(columns=['index'])

    Q2 = data[data["Quality Band"] == 2]
    global Q2Count
    Q2Count = len(Q2)
    Q2 = Q2.reset_index()
    Q2 = Q2.drop(columns=['index'])

    Q3 = data[data["Quality Band"] == 3]
    global Q3Count
    Q3Count = len(Q3)
    Q3 = Q3.reset_index()
    Q3 = Q3.drop(columns=['index'])

    Q1_TS = mean_ser(Q1)
    Q2_TS = mean_ser(Q2)
    Q3_TS = mean_ser(Q3)




    dateTime = pd.read_csv("csv/sample.csv")
    date = dateTime['Date'].values

    d = pd.DataFrame({"Date": date,
                      "Q1_TS": Q1_TS,
                      "Q2_TS": Q2_TS,
                      "Q3_TS": Q3_TS})

    # d.plot(x='Date', y=['Q1_TS', 'Q2_TS', 'Q3_TS'])
    d.to_csv("dataframe.csv")
    return d











@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
   
    
if __name__=='__main__':
    app.run(debug=True)
