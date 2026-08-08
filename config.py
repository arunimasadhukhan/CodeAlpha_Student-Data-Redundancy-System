import os
from dotenv import load_dotenv

# Developer Identity Profile
DEVELOPER_NAME = "Arunima Sadhukhan"
DEVELOPER_LINKEDIN = "https://www.linkedin.com/in/arunima-sadhukhan-7a1368315"
DEVELOPER_GITHUB = "https://github.com/arunimasadhukhan"

# Load environmental variables from the local .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Safety health check for database credentials
if not SUPABASE_URL or not SUPABASE_KEY or "your-project-id" in SUPABASE_URL:
    print("\n[!] WARNING: Database keys are missing or still using fallback placeholder strings in the .env file.")
else:
    print(f"\n[+] Configurations loaded successfully for {DEVELOPER_NAME}'s system.")