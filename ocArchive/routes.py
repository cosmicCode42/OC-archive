from flask import render_template, request, redirect, url_for
from ocArchive import app, db
from ocArchive.models import User, Genre, Character


@app.route("/")
def home():
    # home page
    return render_template("index.html")