from flask import Flask, render_template, url_for, request,redirect
import os
from DbClass import DbClass
import uuid
import hashlib

app = Flask(__name__)

#GLOBALE VARIABLE
naam=""
# lstData =[]

@app.route('/',methods=["GET","POST"])
def Register():
    return render_template('Register.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/Info')
def Info():
    return render_template('Info.html')

@app.route('/Contact')
def Contact():
    return render_template('Contact.html')

@app.route('/Dashboard')
def Dashboard():
    # dbdashboard= DbClass()
    # lstData = dbdashboard.invoegen_data_charts()
    # #eerste waarde moe geconverteerd worden naar string
    # #tweede waarde moet geconverteerd worden naar een date format
    # for waarde in lstData:
    #     lichtsensor=waarde[0]
    #     tijdstip=waarde[1]
    #     print(lichtsensor)
    #     print(tijdstip)
    return render_template('Dashboard.html')

#REGISTREREN
@app.route('/sentRegistreer', methods=["POST"])
def sentRegistreer():
    db = DbClass()
    db_controleren = DbClass()
    email = request.form['email']
    naam = request.form['naam']
    password = request.form['password']
    hashed_password = hash_password(password)
    print(password)
    print(hashed_password)
    aantal = db_controleren.naamcontroleren(naam)
    if aantal == 1:
        return render_template('Register.html')
    else:
        db.gebruikerToevoegen(email,naam,hashed_password)
        return render_template('Login.html')

#INLOGGEN
@app.route('/inloggen_controleren', methods=["POST"])
def inloggen_controleren():
    dbnaam= DbClass()
    dbtest = DbClass()
    naam= request.form['naam']
    wachtwoord = request.form['password']
    hashed_password = dbnaam.login_controleren(naam)
    print(hashed_password)
    print(wachtwoord)
    test = dbtest.test_login(naam)
    if test == 1:
        print("goed")
    else:
        print("slecht")
    if check_password(hashed_password[0], wachtwoord):
        return render_template('Dashboard.html')
    else:
        return render_template('Login.html')

#CONTACTPAGINA
@app.route('/contactform', methods=["POST"])
def contactform():
    db = DbClass()
    naam = request.form['naam']
    email = request.form['email']
    bericht = request.form['bericht']
    db.invoegen_bericht(naam,email,bericht)
    return render_template('Contact.html')

#PASSWORD HASHING AND DEHASHING
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host,port=port,debug=True)
