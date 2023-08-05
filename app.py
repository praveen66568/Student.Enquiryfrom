from flask import *  # flask is framework # port default 5000
import pymongo

app = Flask(__name__)


@app.route('/')
def myhomepage():
    return render_template("home.html")


@app.route('/viewresult')
def vr():
    return render_template("viewstd.html")


@app.route('/reg')
def registration():
    return render_template("registration.html")


@app.route('/submittodb', methods=['POST', 'GET'])
def getdetails():
    try:
        if request.method == 'POST':

            a = request.form['fname']
            b = request.form['number']
            c = request.form['Email']
            d = request.form['address']
            e = request.form['Course']
            f = request.form['batch']
            g = request.form['ads']
            h = request.form['opt']
            i = request.form['degree']
            j = request.form['job']
            k = request.form['Experince']
            l = request.form['Comments']

            if j == '0':
                jobvalue = "Job Needed"
            elif j == '1':
                jobvalue = "No job needed"
            else:
                jobvalue = "Invalid job selection"

            if f == '0':
                batchvalue = "Weekdays"
            elif f == '1':
                batchvalue = "Weekend"
            else:
                batchvalue = "Invalid batch selection"

            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["mydatabase"]
            mycol = mydb["reg"]
            x = {'User Name': a, 'Mobile No': b, 'Email': c, 'Address': d, 'Course Interested': e,
                 'Batch Preferred': batchvalue, 'How You Came To Knew us': g, 'Passed Out Year': h, 'Degree': i,
                 'JOB': jobvalue, 'Preview Experinces & Domain': k, 'Comments': l}
            print(x)
            y = mycol.insert_one(x)
            msg = "sucesfully insert"
    except:
        msg = "not insert"

    return render_template("success.html", msg=msg)


@app.route('/onsubmit', methods=['POST', 'GET'])
def fetchdetails():
    if request.method == 'POST':
        a = request.form['Course']
        b = request.form['year']
        c = request.form['degree']
        print(a, b, c)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["reg"]
        if a == "select" and b == "select1" and c == "select2":
            rows = mycol.find({})
        elif a != "select" and b == "select1" and c == "select2":
            rows = mycol.find({'Course Interested': a})

        elif a == "select" and b != "select1" and c == "select2":
            rows = mycol.find({'Passed Out Year': b})

        elif a == "select" and b == "select1" and c != "select2":
            rows = mycol.find({'Degree': c})

        elif a != "select" and b != "select1" and c == "select2":
            rows = mycol.find({"$and": [{'Course Interested': a}, {'Passed Out Year': b}]})

        elif a != "select" and b == "select1" and c != "select2":
            rows = mycol.find({"$and": [{'Course Interested': a}, {'Degree': c}]})

        elif a == "select" and b != "select1" and c != "select2":
            rows = mycol.find({"$and": [{'Passed Out Year': b}, {'Degree': c}]})
        else:
            rows = mycol.find({"$and": [{'Course Interested': a}, {'Passed Out Year': b}, {'Degree': c}]})

        # o=mycol.find({'Course Interested':a})
        # print(o)

        # s=f"$and:[{'Course Intersted':{a}},{'Passed Out':{b}},{'Degree':{c}}]"
        # print(s)
        # o=mycol.find({s})
    if request.method == 'GET':
        for a in rows:
            print(a)
    return render_template('viewstd.html', rows=rows)







if __name__ == '__main__':
    app.run(port=5000)
