import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, '/var/www/dashboard/')
from app import app as application
