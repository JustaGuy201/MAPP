from supabase import create_client
from flask import current_app
import logging
import os
from dotenv import load_dotenv

def get_supabase():
    """Get Supabase client with service role key."""
    # Force reload environment variables
    load_dotenv()
    
    # Get values directly from environment
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    
    # Verify we're using the correct URL
    expected_url = 'https://fidoehfdaqepvlsovtcl.supabase.co'
    if url != expected_url:
        print(f"Warning: URL mismatch. Expected {expected_url}, got {url}")
        url = expected_url
    
    # Debug logging
    print(f"Supabase URL: {url}")
    print(f"Supabase Key (first 10 chars): {key[:10] if key else 'None'}...")
    
    if not url or not key:
        raise ValueError("Missing Supabase URL or key")
    
    try:
        client = create_client(url, key)
        return client
    except Exception as e:
        print(f"Error creating Supabase client: {str(e)}")
        raise