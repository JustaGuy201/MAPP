import os
from flask import request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.api import bp
from app.utils.audio import handle_audio_upload
from app.supabase_client import get_supabase

@bp.route('/analyze', methods=['POST'])
@login_required
def analyze_song():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    try:
        # Handle file upload and get metadata
        temp_path, metadata, error = handle_audio_upload(file, current_user.id)
        if error:
            return jsonify({'error': error}), 400
            
        # Get form data, use metadata as fallback
        song_data = {
            'title': request.form.get('title') or metadata.get('title', ''),
            'artist': request.form.get('artist') or metadata.get('artist', ''),
            'year': request.form.get('year') or metadata.get('year', ''),
            'producer': request.form.get('producer') or metadata.get('producer', ''),
            'user_id': current_user.id
        }
        
        # Validate required fields
        if not song_data['title'] or not song_data['artist']:
            return jsonify({'error': 'Title and artist are required'}), 400
            
        # Store in Supabase
        supabase = get_supabase()
        response = supabase.table('song_analyses').insert(song_data).execute()
        
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({
            'data': response.data[0],
            'metadata': metadata  # Return metadata for form autofill
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/songs', methods=['GET'])
@login_required
def get_user_songs():
    songs = Song.get_by_user(current_user.id)
    return jsonify([{
        'id': song.id,
        'title': song.title,
        'artist': song.artist,
        'key_signature': song.key_signature,
        'tempo': song.tempo
    } for song in songs]), 200

@bp.route('/subscription/change', methods=['POST'])
@login_required
def change_subscription():
    try:
        plan = request.json.get('plan')
        if plan not in ['free', 'premium']:
            return jsonify({'error': 'Invalid plan type'}), 400

        supabase = get_supabase()
        
        # Set subscription end date (1 month from now for premium)
        subscription_end = datetime.utcnow() + timedelta(days=30) if plan == 'premium' else None
        
        # Update user subscription in Supabase
        response = supabase.table('users').update({
            'subscription_type': plan,
            'subscription_end': subscription_end.isoformat() if subscription_end else None,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', current_user.id).execute()

        if response.data:
            return jsonify({'success': True, 'message': f'Successfully changed to {plan} plan'})
        return jsonify({'error': 'Failed to update subscription'}), 500

    except Exception as e:
        current_app.logger.error(f'Subscription change error: {str(e)}')
        return jsonify({'error': 'Failed to process subscription change'}), 500

@bp.route('/submit_lyrics', methods=['POST'])
@login_required
def submit_lyrics():
    try:
        lyrics = request.json.get('lyrics')
        if not lyrics:
            return jsonify({'error': 'No lyrics provided'}), 400

        # Here you would typically update the song with the lyrics
        # For now, we'll just return success
        return jsonify({
            'success': True,
            'message': 'Lyrics received and processed'
        })
    except Exception as e:
        current_app.logger.error(f'Lyrics submission error: {str(e)}')
        return jsonify({'error': 'Failed to process lyrics'}), 500
