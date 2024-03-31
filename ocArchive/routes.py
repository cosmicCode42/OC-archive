from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required 
from ocArchive import app, db
from ocArchive.models import User, Genre, Character
import bcrypt


@app.route("/")
def home():
    # home page
    return render_template("index.html")


@app.route("/genres")
def genres():
    # list of genres with characters
    genres = list(Genre.query.order_by(Genre.genre_name).all()) #puts all genres in a list
    chars = list(Character.query.order_by(Character.char_name).all()) # puts all characters in a list
    return render_template("genres.html", genres=genres, chars=chars)
    

@app.route("/create_character", methods=["GET", "POST"])
@login_required
def create_character():
    # add characters, including their genres
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    users = list(User.query.order_by(User.id).all()) # puts all users in a list
    if request.method == "POST":
        genre_id = request.form.get("genre_id")
        genre_name = request.form.get("new_genre_name")

        if genre_id and genre_id != 'new_genre':
            genre_id = int(genre_id)
        elif genre_name:
            # Check if the genre already exists
            existing_genre = Genre.query.filter_by(genre_name=genre_name).first()
            if existing_genre:
                genre_id = existing_genre.id
            else:
                # Create a new genre
                new_genre = Genre(genre_name=genre_name)
                db.session.add(new_genre)
                db.session.commit()
                genre_id = new_genre.id

        character = Character(
            char_name=request.form.get("character_name"),
            char_blurb=request.form.get("character_blurb"),
            char_descript=request.form.get("character_description"),
            char_is_usable=bool(True if request.form.get("character_is_usable") else False),
            genre_id=genre_id,
            user_id=current_user.id
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for("characters"))
    return render_template("create_character.html", genres=genres, users=users)


@app.route("/edit_character/<int:char_id>", methods=["GET", "POST"])
@login_required
def edit_character(char_id):
    # edit an existing character
    char = Character.query.get_or_404(char_id)
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    users = list(User.query.order_by(User.id).all())
    if char.user_id != current_user.id:
        abort(403)
    if request.method == "POST":
        genre_id = request.form.get("genre_id")
        genre_name = request.form.get("new_genre_name")

        if genre_id and genre_id != 'new_genre':
            genre_id = int(genre_id)
        elif genre_name:
            existing_genre = Genre.query.filter_by(genre_name=genre_name).first()
            if existing_genre:
                genre_id = existing_genre.id
            else:
                new_genre = Genre(genre_name=genre_name)
                db.session.add(new_genre)
                db.session.commit()
                genre_id = new_genre.id

        char.char_name=request.form.get("character_name")
        char.char_blurb=request.form.get("character_blurb")
        char.char_descript=request.form.get("character_description")
        char.char_is_usable=bool(True if request.form.get("character_is_usable") else False)
        char.genre_id=genre_id
        char.user_id=current_user.id
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_character.html", char=char, genres=genres, users=users)


@app.route("/confirm_character_delete/<int:char_id>", methods=["GET", "POST"])
@login_required
def confirm_character_delete(char_id):
    # warning before user deletes their character
    char = Character.query.get_or_404(char_id)
    if char.user_id != current_user.id:
        abort(403)
    return render_template("confirm_character_delete.html", char=char)


@app.route("/delete_character/<int:char_id>", methods=["GET", "POST"])
@login_required
def delete_character(char_id):
    # allows a user to delete their character
    char = Character.query.get_or_404(char_id)
    db.session.delete(char)
    db.session.commit()
    flash("Character successfully deleted.", "success")
    return redirect(url_for("home"))


@app.route("/characters")
def characters():
    # list of characters
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    chars = list(Character.query.order_by(Character.char_name).all()) # puts all characters in a list
    users = list(User.query.order_by(User.id).all())
    return render_template("characters.html", chars=chars, genres=genres, users=users)


@app.route("/id_gain", methods=["GET", "POST"])
def id_gain():
    # page to create a username and password to use in handling characters
    users = list(User.query.order_by(User.id).all())
    if request.method == "POST":
        # Hash the password before storing it in the database
        user = User(user_name=request.form.get("user_name"))
        user.set_password(request.form.get("user_password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("id_gain.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("user_password")
        user = User.query.filter_by(user_name=user_name).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.user_name}!", "success")
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


@app.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    # User profile page
    genres = list(Genre.query.order_by(Genre.genre_name).all())
    chars = list(Character.query.filter_by(user_id=user_id).order_by(Character.char_name).all())
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", chars=chars, genres=genres, user=user)