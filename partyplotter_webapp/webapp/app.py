from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = "your_secret_key"  #Needs replacing later on

#Configure the SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#
#User Database configuration
class User(db.Model):
    #Class variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(330), nullable=True)
    birthday = db.Column(db.Date, nullable=False)
    dateJoined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)




'''Set up for user log in and registrstion as well as user dashboard'''

#Home page route
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


#Login route
@app.route("/login", methods=["POST"])
def login():
    #Get form data
    username = request.form['username']
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    #Check if user exists
    if user and user.checkPassword(password):
        session['username'] = username
        return redirect(url_for("dashboard"))
    #show home page if not
    else:
        return render_template("register.html", error="User not found, Please register")



#Register route
@app.route("/signup", methods=["GET"])
def show_signup():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    #Check for user in db
    username = request.form["newusername"]
    password = request.form["newpassword"]
    userEmail = request.form["newemail"]
    userBirthday = request.form["newbirthday"]
    user = User.query.filter_by(username=username).first()
    #Create new user
    if user is None:
        birthday_obj = datetime.strptime(userBirthday, '%Y-%m-%d').date()
        newUser = User(
                        username=username, 
                        birthday=birthday_obj, 
                        email=userEmail
                       )
        newUser.setPassword(password)
        db.session.add(newUser)
        db.session.commit()
        session["username"] = username
        return redirect(url_for("dashboard"))
    #Check for user
    else:
        return render_template("index.html", error="User already exists, Please login")
    

#Dashboard route
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html",username=session["username"])
    return redirect(url_for("home"))



#Logout route
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("home"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)