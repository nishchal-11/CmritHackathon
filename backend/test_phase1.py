"""
Quick test script to verify Phase 1 setup
"""
import sys
print("=" * 60)
print("Operation Gridlock - Phase 1 Verification")
print("=" * 60)

# Test imports
try:
    import fastapi
    print("✓ FastAPI:", fastapi.__version__)
except ImportError as e:
    print("✗ FastAPI:", e)
    sys.exit(1)

try:
    import uvicorn
    print("✓ Uvicorn: Available")
except ImportError as e:
    print("✗ Uvicorn:", e)
    sys.exit(1)

try:
    import requests
    print("✓ Requests:", requests.__version__)
except ImportError as e:
    print("✗ Requests:", e)
    sys.exit(1)

try:
    import PIL
    print("✓ Pillow:", PIL.__version__)
except ImportError as e:
    print("✗ Pillow:", e)
    sys.exit(1)

try:
    import numpy
    print("✓ NumPy:", numpy.__version__)
except ImportError as e:
    print("✗ NumPy:", e)
    sys.exit(1)

try:
    import httpx
    print("✓ HTTPX:", httpx.__version__)
except ImportError as e:
    print("✗ HTTPX:", e)
    sys.exit(1)

try:
    from pydantic_settings import BaseSettings
    print("✓ Pydantic Settings: Available")
except ImportError as e:
    print("✗ Pydantic Settings:", e)
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ Phase 1 Environment Setup: COMPLETE")
print("=" * 60)
print("\nNext steps:")
print("1. Run backend: cd backend && python -m uvicorn app.main:app --reload")
print("2. Test API: http://127.0.0.1:8000/docs")
print("3. Move to Phase 2: Frontend setup with React + Leaflet")
