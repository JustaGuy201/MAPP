import os
from mutagen import File
from mutagen.easyid3 import EasyID3
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_metadata(file_path):
    """Extract metadata from audio file"""
    try:
        metadata = {}
        current_app.logger.info(f"Attempting to extract metadata from: {file_path}")
        
        audio = File(file_path, easy=True)
        current_app.logger.info(f"Audio file loaded: {audio}")
        
        if audio is not None:
            # Try to get metadata using EasyID3 for MP3s
            if isinstance(audio, EasyID3):
                current_app.logger.info("File is MP3 with ID3 tags")
                metadata['title'] = audio.get('title', [''])[0]
                metadata['artist'] = audio.get('artist', [''])[0]
                metadata['year'] = audio.get('date', [''])[0][:4]  # Get just the year
                metadata['producer'] = audio.get('producer', [''])[0]
            else:
                current_app.logger.info("File is not MP3 or doesn't have ID3 tags")
                # For other formats or MP3s without ID3, try filename
                filename = os.path.basename(file_path)
                name_parts = os.path.splitext(filename)[0].split(' - ')
                if len(name_parts) >= 2:
                    metadata['artist'] = name_parts[0].strip()
                    metadata['title'] = name_parts[1].strip()
                
        current_app.logger.info(f"Extracted metadata: {metadata}")
        return metadata
        
    except Exception as e:
        current_app.logger.error(f"Metadata extraction error: {str(e)}")
        return {}

def handle_audio_upload(file, user_id):
    """Handle audio file upload and metadata extraction"""
    if not allowed_file(file.filename):
        return None, None, "Invalid file type. Only MP3 and WAV files are allowed."
        
    try:
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(current_app.root_path, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        # Extract metadata
        metadata = extract_metadata(temp_path)
        
        return temp_path, metadata, None
        
    except Exception as e:
        current_app.logger.error(f"File upload error: {str(e)}")
        return None, None, str(e) 