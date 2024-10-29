from app import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    producer = db.Column(db.String(100))
    rank = db.Column(db.Integer)
    key_signature = db.Column(db.String(10))
    tempo = db.Column(db.Float)
    time_signature = db.Column(db.String(10))
    chord_progression = db.Column(db.String(200))
    group = db.Column(db.Integer)  # 1 for Billboard, 2 for user-uploaded
