import os
from datetime import datetime, timedelta
from supabase import create_client
from flask import current_app
import librosa
import numpy as np

def analyze_and_store_song(file_path, user_id, song_data):
    """Analyze song and store results, then delete the file"""
    try:
        # Load and analyze audio file
        y, sr = librosa.load(file_path)
        
        # Extract features
        analysis_data = {
            'tempo': float(librosa.beat.tempo(y=y, sr=sr)[0]),
            'key': int(librosa.feature.chroma_stft(y=y, sr=sr).mean()),
            'duration': float(librosa.get_duration(y=y, sr=sr)),
            # Add other analysis features here
            'user_id': user_id,
            'title': song_data.get('title'),
            'artist': song_data.get('artist'),
            'year': song_data.get('year'),
            'producer': song_data.get('producer'),
            'analyzed_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(days=15)).isoformat()
        }
        
        # Store analysis results in Supabase
        supabase = create_client(
            current_app.config['SUPABASE_URL'],
            current_app.config['SUPABASE_SERVICE_KEY']
        )
        
        response = supabase.table('song_analyses').insert(analysis_data).execute()
        
        # Delete the temporary file
        os.remove(file_path)
        
        return response.data[0] if response.data else None
        
    except Exception as e:
        current_app.logger.error(f"Analysis error: {str(e)}")
        # Ensure file is deleted even if analysis fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise 

def cleanup_expired_analyses():
    """Clean up expired analyses"""
    try:
        supabase = create_client(
            current_app.config['SUPABASE_URL'],
            current_app.config['SUPABASE_SERVICE_KEY']
        )
        
        supabase.rpc('cleanup_expired_analyses').execute()
        
    except Exception as e:
        current_app.logger.error(f"Cleanup error: {str(e)}")