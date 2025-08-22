from flask import Flask, render_template



'''Set up for user log in and registrstion as well as user dashboard'''
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)