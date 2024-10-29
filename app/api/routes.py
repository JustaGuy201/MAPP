from flask import jsonify, request
from app.api import bp
from app.models import Song
from app import db
import librosa

@bp.route('/analyze', methods=['POST'])
def analyze_song():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Load the audio file
        y, sr = librosa.load(file)
        
        # Extract features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        key = librosa.key.estimate_key(y, sr)
        
        # Create and save the song
        song = Song(
            title=request.form.get('title'),
            artist=request.form.get('artist'),
            year=request.form.get('year'),
            producer=request.form.get('producer'),
            key_signature=key,
            tempo=tempo,
            time_signature='4/4',  # Assuming 4/4 for simplicity
            chord_progression='Not implemented',
            group=2
        )
        db.session.add(song)
        db.session.commit()
        
        # Placeholder logic to determine if lyrics were detected
        lyrics_detected = False  # Replace this with actual logic later
        
        return jsonify({
            'lyrics_detected': lyrics_detected,
            'message': 'Song analyzed and saved successfully',
            'id': song.id,
            'key': key,
            'tempo': tempo
        }), 201

@bp.route('/submit_lyrics', methods=['POST'])
def submit_lyrics():
    lyrics = request.json.get('lyrics')
    # Process the manually submitted lyrics
    # ...
    
    return jsonify({'success': True, 'message': 'Lyrics received and processed'})
