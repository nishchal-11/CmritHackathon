# Frontend-Backend Integration Guide

## Overview
Operation Gridlock now has full frontend-backend integration using React + FastAPI.

## Architecture

```
Frontend (React)
├── src/services/api.js          → API service layer
├── src/components/Map.jsx        → Main map with API calls
├── src/App.js                    → App with backend health check
└── src/utils/testAPI.js          → API testing utility

Backend (FastAPI)
├── app/main.py                   → Main app with CORS
├── app/routes/camera.py          → Camera detection endpoints
├── app/routes/route.py           → OSRM routing endpoints
└── app/routes/enhance.py         → Image enhancement endpoints
```

## API Integration Details

### 1. API Service Layer (`src/services/api.js`)

**Camera API:**
- `cameraAPI.getStatus()` → GET `/api/camera/status`
- `cameraAPI.checkNode(nodeName)` → GET `/api/camera/check/{node_name}`
- `cameraAPI.scanAll()` → POST `/api/camera/scan-all`

**Routing API:**
- `routingAPI.getETA(startNode, endNode)` → GET `/api/route/eta/{start}/{end}`
- `routingAPI.calculateRoute(params)` → POST `/api/route/calculate`
- `routingAPI.predictEscape(node, exits)` → POST `/api/route/predict-escape`

**Enhancement API:**
- `enhancementAPI.getStatus()` → GET `/api/enhance/status`
- `enhancementAPI.uploadImage(file)` → POST `/api/enhance/upload`
- `enhancementAPI.getHistory()` → GET `/api/enhance/history`

**System API:**
- `systemAPI.getStatus()` → GET `/api/status`
- `systemAPI.healthCheck()` → GET `/`

### 2. Map Component Integration

**New Features:**
- Real-time backend connectivity check
- API calls for route calculation using OSRM
- Dynamic route geometry rendering from backend
- Traffic multiplier display (city_center: 1.8x, urban: 1.4x, highway: 1.1x)
- Error handling with fallback to demo mode
- Loading states during API calls

**Demo Flow:**
1. User clicks "Start Demo" button
2. Frontend calls `cameraAPI.checkNode('node1')`
3. Backend returns detection status (currently no SAM 3 data yet)
4. Frontend calls `routingAPI.getETA('node1', 'node3')`
5. Backend queries OSRM and returns real route geometry + ETA
6. Map renders actual route polyline with traffic-adjusted duration
7. Countdown timer shows real ETA from backend

### 3. App Component Integration

**Features:**
- Automatic backend health check on mount
- Status badge shows "SYSTEM OPERATIONAL" (green) or "BACKEND OFFLINE" (red)
- Periodic health checks every 30 seconds
- Visual feedback with color-coded status indicator

## Testing the Integration

### Option 1: Use the Demo Button
1. Open http://localhost:3000
2. Check the status badge (should be green if backend is running)
3. Click "🎯 Start Demo" button
4. Watch the console for API calls and responses
5. Observe the map showing real OSRM route geometry

### Option 2: Browser Console Testing
Open the browser console and run:

```javascript
// Test individual API endpoints
const { cameraAPI, routingAPI, systemAPI } = await import('./services/api.js');

// Check system status
await systemAPI.getStatus();

// Check camera node
await cameraAPI.checkNode('hub');

// Get route with real OSRM data
await routingAPI.getETA('hub', 'node3');
```

### Option 3: PowerShell Testing
From the backend directory:

```powershell
# Test camera endpoint
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/camera/status" -UseBasicParsing | Select-Object -ExpandProperty Content

# Test route endpoint
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/route/eta/hub/node3" -UseBasicParsing | Select-Object -ExpandProperty Content
```

## Current State

### ✅ Working
- Backend server running on http://127.0.0.1:8000
- Frontend running on http://localhost:3000
- CORS configured for localhost:3000
- All API endpoints operational
- Real OSRM route calculation
- Traffic simulation with multipliers
- Map rendering with real geometry
- Health check and status monitoring

### ⏳ Pending (requires SAM 3 Colab completion)
- Actual vehicle detection data
- Precomputed mask loading
- Confidence scores from SAM 3
- Frame preview images

### 🔄 Fallback Behavior
If backend is unavailable or SAM 3 data not ready:
- App shows "BACKEND OFFLINE" status
- Demo mode uses hardcoded route geometry
- No errors thrown, graceful degradation

## Next Steps

1. **Wait for SAM 3 Processing**
   - Download `gridlock_precomputed_masks.zip` from Colab
   - Extract to `models/precomputed/`
   - Test `/api/camera/check/hub_mgroad` endpoint

2. **Test Real Detection Data**
   - Once SAM 3 data is ready, demo will show actual detection results
   - Map will display confidence scores
   - Frame previews will be available

3. **Real-ESRGAN Integration (Phase 6)**
   - Clone Real-ESRGAN repo
   - Integrate CLI into `/api/enhance/upload`
   - Test image enhancement workflow

## API Response Examples

### Route ETA Response
```json
{
  "distance_meters": 9371.5,
  "distance_km": 9.37,
  "base_duration_seconds": 799,
  "adjusted_duration_seconds": 1438,
  "eta_minutes": 24.0,
  "route_type": "city_center",
  "traffic_multiplier": 1.8,
  "geometry": [[12.975523, 77.60658], ...],
  "steps": 19,
  "start_node": "MG Road Metro",
  "end_node": "Silk Board"
}
```

### Camera Check Response
```json
{
  "found": false,
  "node": "hub_mgroad",
  "message": "No precomputed data available. Run SAM 3 processing in Colab first.",
  "confidence": 0.0
}
```

## Troubleshooting

**Issue: Status badge shows BACKEND OFFLINE**
- Verify backend is running: http://127.0.0.1:8000/api/status
- Check CORS settings in `backend/app/main.py`
- Ensure `API_BASE_URL` in `frontend/src/constants.js` is correct

**Issue: Route doesn't render**
- Check browser console for API errors
- Verify OSRM public API is accessible
- Check network tab for failed requests

**Issue: Demo button shows "Processing..." forever**
- Check browser console for errors
- Verify axios is installed: `npm list axios`
- Check backend logs for errors

## Integration Complete! 🎉

The frontend now communicates with the backend for:
- ✅ System health monitoring
- ✅ Real-time route calculation via OSRM
- ✅ Camera node checking (ready for SAM 3 data)
- ✅ Traffic simulation with realistic ETAs
- ✅ Dynamic map rendering with API data

Ready for Phase 5 completion (SAM 3 data) and Phase 6 (Real-ESRGAN)!
