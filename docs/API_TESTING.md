# Backend API Testing

## Test Endpoints

### 1. Status Check
```powershell
curl http://127.0.0.1:8000/api/status
```

### 2. Camera Status
```powershell
curl http://127.0.0.1:8000/api/camera/status
```

### 3. Check Specific Camera
```powershell
curl http://127.0.0.1:8000/api/camera/check/node1
```

### 4. Scan All Cameras
```powershell
curl -X POST http://127.0.0.1:8000/api/camera/scan-all
```

### 5. Get ETA Between Nodes
```powershell
curl http://127.0.0.1:8000/api/route/eta/node1/node3
```

### 6. Enhancement Status
```powershell
curl http://127.0.0.1:8000/api/enhance/status
```

### 7. View API Docs
Open browser: http://127.0.0.1:8000/docs

## Expected Results

**Without SAM 3 data (before Colab finishes):**
- Camera endpoints return `found: false`
- Route endpoints work with OSRM
- Enhancement ready (placeholder)

**After SAM 3 data extracted:**
- Camera endpoints return detection results
- Mask and overlay paths available
- Confidence scores visible
