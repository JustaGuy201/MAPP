from app.supabase_client import get_supabase
from flask import current_app
import jwt
from time import time
from flask_login import UserMixin
from datetime import datetime
from app import login

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self._email = user_data.get('email')
        self._username = user_data.get('username')
        self._is_active = user_data.get('is_active', True)
        self._subscription_type = user_data.get('subscription_type', 'free')
        self._subscription_end = user_data.get('subscription_end')
        self._created_at = user_data.get('created_at')

    @property
    def email(self):
        return self._email

    @property
    def username(self):
        return self._username

    @property
    def is_active(self):
        return self._is_active

    @property
    def subscription_type(self):
        return self._subscription_type

    @staticmethod
    def get_by_id(user_id):
        try:
            supabase = get_supabase()
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            if response.data:
                return User(response.data[0])
            return None
        except Exception as e:
            print(f"Error getting user by ID: {str(e)}")
            return None

    @staticmethod
    def get_by_email(email):
        try:
            supabase = get_supabase()
            response = supabase.table('users').select('*').eq('email', email).execute()
            if response.data:
                return User(response.data[0])
            return None
        except Exception as e:
            print(f"Error getting user by email: {str(e)}")
            return None

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    def get_verification_token(self, expires_in=3600):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
            return User.get_by_id(id)
        except:
            return None

    @staticmethod
    def verify_email_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['verify_email']
            return User.get_by_id(id)
        except:
            return None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

@login.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

class Song:
    def __init__(self, song_data):
        self.id = song_data.get('id')
        self.title = song_data.get('title')
        self.artist = song_data.get('artist')
        self.year = song_data.get('year')
        self.producer = song_data.get('producer')
        self.rank = song_data.get('rank')
        self.key_signature = song_data.get('key_signature')
        self.tempo = song_data.get('tempo')
        self.time_signature = song_data.get('time_signature')
        self.chord_progression = song_data.get('chord_progression')
        self.group_type = song_data.get('group_type')
        self.user_id = song_data.get('user_id')
        self.created_at = song_data.get('created_at')
        self.updated_at = song_data.get('updated_at')

    @staticmethod
    def create(song_data, user_id):
        supabase = get_supabase()
        data = {
            'title': song_data['title'],
            'artist': song_data['artist'],
            'year': song_data.get('year'),
            'producer': song_data.get('producer'),
            'rank': song_data.get('rank'),
            'key_signature': song_data.get('key_signature'),
            'tempo': song_data.get('tempo'),
            'time_signature': song_data.get('time_signature'),
            'chord_progression': song_data.get('chord_progression'),
            'group_type': song_data.get('group_type', 2),
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        response = supabase.table('songs').insert(data).execute()
        return Song(response.data[0]) if response.data else None

    @staticmethod
    def get_by_user(user_id):
        supabase = get_supabase()
        response = supabase.table('songs').select('*').eq('user_id', user_id).execute()
        return [Song(song_data) for song_data in response.data]

    @staticmethod
    def get_by_id(song_id):
        supabase = get_supabase()
        response = supabase.table('songs').select('*').eq('id', song_id).execute()
        return Song(response.data[0]) if response.data else None
