"""
WSGI entry point for Gunicorn (Render.com)
"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.app import server

# Gunicorn will look for 'app' variable
app = server

if __name__ == "__main__":
    app.run()
