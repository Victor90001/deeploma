from flask import Flask, request, render_template, redirect
from markupsafe import escape


flask_app = Flask(__name__)


@flask_app.route("/")
def flask_main():
    return render_template("index.html")


@flask_app.route("/contactus")
def read_form():
    if request.method == 'GET':
        return redirect("/")
    if request.method == 'POST':
        data = request.form
        return data


@flask_app.route("/detection")
def detection_page():
    if request.method == 'GET':
        return render_template("detection.html")