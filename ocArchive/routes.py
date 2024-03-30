from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required 
from ocArchive import app, db
from ocArchive.models import User, Genre, Character
import bcrypt


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
@login_required
def create_character():
    # add characters, including their genres
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    users = list(User.query.order_by(User.id).all())
    if request.method == "POST":
        character = Character(
            char_name=request.form.get("character_name"),
            char_blurb=request.form.get("character_blurb"),
            char_descript=request.form.get("character_description"),
            char_is_usable=request.form.get("character_is_usable"),
            genre_id=request.form.get("genre_id"),
            user_id=current_user.id
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_character.html", genres=genres, users=users)


@app.route("/characters")
def characters():
    # list of characters
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    chars = list(Character.query.order_by(Character.char_name).all()) # puts all characters in a list
    return render_template("characters.html", chars=chars, genres=genres)


@app.route("/id_gain", methods=["GET", "POST"])
def id_gain():
    # page to create a username and password to use in handling characters
    users = list(User.query.order_by(User.id).all())
    if request.method == "POST":
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(request.form.get("user_password").encode('utf-8'), bcrypt.gensalt())
        user = User(
            user_name=request.form.get("user_name"),
            user_password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("id_gain.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user_name")
        password = request.form.get("user_password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.user_password_hash.encode('utf-8')):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))