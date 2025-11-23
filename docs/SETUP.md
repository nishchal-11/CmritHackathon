# 🛠️ Setup Guide - Operation Gridlock

## Phase 1: Environment Setup ✅ COMPLETE

### What Was Done:
1. ✅ Created project structure (`frontend/`, `backend/`, `models/`, `assets/`, `docs/`)
2. ✅ Created Python virtual environment (`.venv`)
3. ✅ Installed all Phase 1 dependencies:
   - FastAPI 0.121.3
   - Uvicorn 0.38.0
   - Requests 2.32.5
   - Pillow 12.0.0
   - NumPy 2.3.5
   - HTTPX 0.28.1
   - Pydantic Settings 2.12.0
   - Python-Jose 3.5.0
4. ✅ Created FastAPI backend skeleton (`backend/app/main.py`)
5. ✅ Verified all imports and packages

---

## 🚀 How to Run Phase 1

### Backend Server:
```powershell
# Navigate to project root
cd "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Navigate to backend
cd backend

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test the API:
- Open browser: http://127.0.0.1:8000/
- Swagger docs: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

Expected response from root `/`:
```json
{
  "status": "operational",
  "project": "Operation Gridlock",
  "version": "1.0.0",
  "stack": "100% FOSS"
}
```

---

## 📦 Installed Packages

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.121.3 | Web framework |
| uvicorn | 0.38.0 | ASGI server |
| requests | 2.32.5 | HTTP client |
| httpx | 0.28.1 | Async HTTP client |
| Pillow | 12.0.0 | Image processing |
| numpy | 2.3.5 | Numerical operations |
| pydantic-settings | 2.12.0 | Config management |
| python-jose | 3.5.0 | JWT tokens |

---

## 🔍 Verify Installation

Run the test script:
```powershell
cd backend
python test_phase1.py
```

You should see all green checkmarks ✓

---

## 📂 Project Structure Created

```
gridlock-operation-foss/
├── .venv/                     # Virtual environment ✅
├── backend/                   # Python FastAPI backend ✅
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app ✅
│   │   ├── routes/           # API endpoints (empty for now)
│   │   └── cv/               # Computer vision modules (empty)
│   ├── requirements.txt      # Dependencies ✅
│   ├── .env.example          # Config template ✅
│   ├── test_phase1.py        # Verification script ✅
│   └── run.ps1               # Run script
├── frontend/                  # React app (Phase 2)
├── models/
│   └── precomputed/          # SAM 2 masks (from Colab)
├── assets/
│   └── videos/               # Pexels traffic videos
├── docs/                      # Documentation
├── README.md                  # Main README ✅
└── LICENSE                    # MIT License ✅
```

---

## 🎯 Next Phase: Frontend Setup

When you're ready, say **"move to Phase 2"** and I'll:
1. Initialize React app with `create-react-app`
2. Install `leaflet`, `react-leaflet`, `axios`
3. Create Map component with dark CartoDB tiles
4. Add Bangalore nodes (MG Road, Indiranagar, Koramangala, Silk Board)
5. Set up map markers and basic UI

---

## 🧪 Google Colab for SAM 2

While we build the frontend, you can run the Colab notebook I provided earlier to:
- Process your 4 Pexels videos
- Generate precomputed masks
- Download the ZIP to `models/precomputed/`

---

## ⚡ Quick Commands Reference

### Activate Environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Deactivate Environment:
```powershell
deactivate
```

### Install New Package:
```powershell
pip install <package-name>
```

### Update requirements.txt:
```powershell
pip freeze > backend\requirements.txt
```

### Check Python Version:
```powershell
python --version
```

---

**Status**: Phase 1 ✅ COMPLETE  
**Next**: Phase 2 - Frontend Setup (React + Leaflet)
