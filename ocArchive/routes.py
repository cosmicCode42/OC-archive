from flask import render_template, request, redirect, url_for
from ocArchive import app, db
from ocArchive.models import User, Genre, Character


@app.route("/")
def home():
    # home page
    genres = list(Genre.query.order_by(Genre.genre_name).all()) #puts all genres in a list
    return render_template("index.html", genres=genres)


@app.route("/genres")
def genres():
    # list of genres with characters
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    return render_template("genres.html", genres=genres)
    

@app.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    # page for adding genres directly
    if request.method == "POST":
        genre = Genre(genre_name=request.form.get("genre_name"))
        db.session.add(genre)
        db.session.commit()
        return redirect(url_for("genres"))
    return render_template("add_genre.html")
    

@app.route("/create_character", methods=["GET", "POST"])
def create_character():
    # add characters, including their genres
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    if request.method == "POST":
        character = Character(
            char_name=request.form.get("character_name"),
            char_blurb=request.form.get("character_blurb"),
            char_descript=request.form.get("character_description"),
            char_is_usable=request.form.get("character_is_usable"),
            genre_id=request.form.get("genre_id")
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_character.html", genres=genres)


@app.route("/characters")
def characters():
    # list of characters
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    chars = list(Character.query.order_by(Character.char_name).all()) # puts all characters in a list
    return render_template("characters.html", chars=chars, genres=genres)