"""
Vercel Serverless Function Entry Point
This file adapts the FastAPI app for Vercel's serverless environment
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Export the FastAPI app as a Vercel handler
handler = app
