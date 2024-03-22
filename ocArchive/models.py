from ocArchive import db


class User(db.Model):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(15), unique=True, nullable=False)
    user_chars = db.relationship("Character", backref="user", cascade="all, delete", lazy=True)

    def __repr__(self):
        return self.user_name


class Genre(db.Model):
    #schema for the Genre model
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), unique=True, nullable=False)
    characters = db.relationship("Character", backref="genre", cascade="all, delete", lazy=True)

    def __repr__(self):
        return self.genre_name


class Character(db.Model):
    # schema for the Character model
    id = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(125), unique=True, nullable=False)
    char_blurb = db.Column(db.Text, unique=True, nullable=False)
    char_descript = db.Column(db.Text, unique=True)
    char_is_usable = db.Column(db.Boolean, default=False, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return self.char_name