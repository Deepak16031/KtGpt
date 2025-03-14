from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client():
    """Create and return a Supabase client for direct API access"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL and API key must be set in environment variables")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)