from flask import Flask, render_template, url_for, request, redirect, session, sessions, flash
from flask_session import Session
from werkzeug.utils import secure_filename
import os
from hashlib import md5, sha256
import random
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["freesend"]

users = db["users"]

app = Flask(__name__)

app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



font = "blocktrain.ttf"



@app.route('/')
def main():
    
    return render_template("main.html", font = url_for('static', filename=font))




@app.route("/logout")
def logout():
    session["username"] = None
    session["password"] = None
    return redirect("/")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html", font = url_for('static', filename=font))
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        if(users.find_one({'username': username})):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            
            password_digest = sha256(password.encode()).hexdigest()
            local_user_upload_directory = sha256(os.urandom(64)).hexdigest()
            users.insert_one({'username': username, 'password': password_digest, 'luod':local_user_upload_directory})
            os.system("cd local && mkdir "+local_user_upload_directory+" && cd "+local_user_upload_directory+" && mkdir download && mkdir send")
            return redirect('/login')
            
        
        
        
        


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", failed = False)
    if request.method == "POST":
        
        username = request.form['username']
        password = request.form['password']
        
        check_pw = sha256(password.encode()).hexdigest()
        
        user_sesh = users.find_one({'username': username, 'password': check_pw})
        
        if user_sesh:
            session["username"] = username
            session["password"] = check_pw
            #session["password"] = password
            return redirect('/home')
        
        else:
            return render_template("login.html", failed = True)
        
    
    
@app.route('/home')
def home():
    
    if (session["username"] == None and session["password"] == None):
        return redirect('/')
    return render_template("home.html", un = session["username"])


@app.route('/send')
def send():
    try:
        dix = users.find_one({'username': session["username"], 'password': session["password"]})
        
        dir = dix["luod"]
        session["dir"] = dix["luod"]
        return render_template("upload.html", directory = dir)
    except TypeError:
        return redirect('/')
        

        


@app.route('/download')
def download():
    try:
        dix = users.find_one({'username': session["username"], 'password': session["password"]})
        
        dir = dix["luod"]
        
        return render_template("download.html", directory = dir)
    except TypeError:
        return redirect('/')

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        upload_dir = ("local/"+session["dir"]+"/send")
        f = request.files['file']
        #f.save(f.filename)
        f.save(os.path.join(upload_dir), f.filename)
        #return f.filename
        return upload_dir
#TODO - except keyerror 'username'/redirect to login
        

            
            
    

    

if __name__ == "__main__":
    
    app.run(debug=True)