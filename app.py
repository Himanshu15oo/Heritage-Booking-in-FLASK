import sys
from flask import Flask, redirect, url_for, render_template, request, session
from pymongo import MongoClient
import pyqrcode
import string
import random

app = Flask(__name__)
app.secret_key = "Himanshu"

client = MongoClient('localhost', 27017)
db = client.Heritage_db
hc = db.heritage
uc = db.visitors

pi = db.payment_info


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form['action'] == "book":
    
            # print(dict, file=sys.stderr)


            return redirect(url_for("bookingForm"))

        if request.form['action'] == "search":
            # p_no = request.form.get('no', "08766436534")
           return redirect(url_for("search"))
    else:
        return render_template("index.html")


@app.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")
    

@app.route("/sites", methods=["POST", "GET"])
def sites():
    return render_template("tours.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    return render_template("contact.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        p_no    = request.form['v_email']
        history = uc.find({ 'email' : p_no})
        date = session["date"]
        return render_template("history.html", data = history, dt = date)
    else:
        return render_template("search.html", )



@app.route("/payment", methods=["POST", "GET"])
def payment():
    userDict    = session["userDict"]
    month       = session["month"]
    date        = session["date"]
    cost        = session["cost"]
    monument    = session["heritage"]
    totalCount  = session["totalCount"]
    if request.method == "POST":
        res = ''.join(random.choices(string.ascii_letters, k=10))
        dict = {
                "name"      : session["name"],
                "email"     : session["email"],
                "phone"     : session["phone"],
                "heritage"  : session["heritage"],
                "visitors"  : session["visitors"],
                "date"      : session["fullDate"],
                "transactionId"   : res,
                "cost"      : cost
        }

        pi.insert_one(dict)

        # USER ENTRY IN DB 
        uc.insert_one(userDict)

        # UPDATING HERITAGE COLLECTION
        hc.update_one(
        { "name": monument  },
        { "$set": { month + '.'+ str(date) : totalCount }}
        )
        return  redirect(url_for("home"))
    else:
        upi_string = "Put your UPI string" + str(cost) + "&tn=Booking_For_" + monument + ""
        qr_url = pyqrcode.create(upi_string)
        qr_url.png("./static/img/pay.png", scale=8)
        return render_template('payment.html')

        

@app.route("/bookingForm", methods=["POST", "GET"])
def bookingForm():
    if request.method == "POST":
        YMD = request.form['v_date'].split("-")
        session["date"]     = int(YMD[2])
        if session["date"] > 25:
            message = "Booking not available for this date!"
            return render_template("booking.html", msg = message)
        session["month"]    = YMD[1]
        monument            = request.form['heritage']
        people              = int(request.form['v_count'])
        h_info              = hc.find_one({'name' : monument})
        exisiting_count     = h_info[session["month"]][session["date"]]
        rate                = h_info['rate']

        session["totalCount"] = exisiting_count + people

        # CALCULATING COST OF VISIT
        session["cost"]     = rate * people

        session["name" ]    = request.form['v_name']
        session["email"]    = request.form['v_email']
        session["phone"]    = request.form['v_phone']
        session["heritage"] = request.form['heritage']
        session["visitors"] = request.form['v_count']
        session["fullDate"] = request.form['v_date']

        if (exisiting_count > 300) or ((exisiting_count + people) > 300):
            message = "Booking full for the Date!"
            return render_template("booking.html", msg = message)
        else:
            dict = {
                "name"      : session["name"],
                "email"     : session["email"],
                "phone"     : session["phone"],
                "heritage"  : session["heritage"],
                "visitors"  : session["visitors"],
                "date"      : session["fullDate"]
            }
            session["userDict"] = dict
            print(session["date"], file=sys.stderr)
            

            return redirect(url_for("payment"))
    else:
        return render_template('booking.html')


if __name__ == "__main__":
    app.run(debug=True)
