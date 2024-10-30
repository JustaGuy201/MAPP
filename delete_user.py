from app.supabase_client import get_supabase

def delete_user(email):
    try:
        supabase = get_supabase()
        
        # First get the user from auth system
        users = supabase.auth.admin.list_users()
        user = next((u for u in users if u.email == email), None)
        
        if user:
            # Delete from auth system
            supabase.auth.admin.delete_user(user.id)
            print(f"Deleted user {email} from auth system")
            
            # Delete from users table
            response = supabase.table('users').delete().eq('email', email).execute()
            print(f"Deleted user {email} from users table")
        else:
            print(f"User {email} not found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    email = "othonielj@gmail.com"  # Replace with the email you want to delete
    delete_user(email) 
