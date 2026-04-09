from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY_SERVICE_ROLE

supabase = create_client(SUPABASE_URL, SUPABASE_KEY_SERVICE_ROLE)
