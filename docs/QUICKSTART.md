# Quick Start Guide - Operation Gridlock

## 🚀 Current Status

### Running Services
- **Backend:** http://127.0.0.1:8000 ✅
- **Frontend:** http://localhost:3000 ✅
- **API Docs:** http://127.0.0.1:8000/docs ✅

### Integration Complete ✅
- React frontend communicates with FastAPI backend
- Real-time route calculation using OSRM
- Traffic simulation with realistic multipliers
- Backend health monitoring with visual status badge

---

## 🎮 How to Use the Demo

### 1. Open the Application
Navigate to: **http://localhost:3000**

You should see:
- Header: "🚨 OPERATION GRIDLOCK"
- Status badge: "SYSTEM OPERATIONAL" (green pulse)
- Dark map with 4 Bangalore nodes marked

### 2. Start the Demo
Click the **"🎯 Start Demo"** button in the top-left control panel

### 3. Watch the Sequence
1. **Sector Highlight** (2 seconds)
   - Green polygon appears around Indiranagar (East Sector)
   
2. **Detection Phase** (auto)
   - Backend calls: `GET /api/camera/check/node1`
   - Status panel shows: "✅ Target Detected: Indiranagar"
   
3. **Route Calculation** (auto)
   - Backend calls: `GET /api/route/eta/node1/node3`
   - OSRM calculates real route from Indiranagar → Silk Board
   - Red dotted line appears on map (actual OSRM geometry)
   
4. **Status Display**
   - Distance: "9.37 km"
   - Traffic: "city_center (1.8x)" 
   - ETA countdown: "24:00" (minutes:seconds)
   
5. **Police Dispatch** (3 seconds)
   - Green police car marker appears at MG Road Metro
   - Animates toward Silk Board intercept point

---

## 🔍 Understanding the Map

### Node Types
- **Blue Marker (MG Road Metro)** - Hub / Police HQ
- **Red Markers (Indiranagar, Koramangala)** - Checkpoints with cameras
- **Orange Marker (Silk Board)** - Exit point / Intercept zone

### Visual Elements
- **Red Dotted Line** - Predicted suspect route (real OSRM data)
- **Detection Circles** - 500m camera surveillance radius (dashed)
- **Intercept Circle** - 800m police deployment zone (solid green)
- **Green Polygon** - Active sector alert area

### Control Panel (Top-Left)
- **Start Demo Button** - Trigger detection simulation
- **Status Panel** - Real-time updates:
  - Target detection confirmation
  - Distance to intercept
  - Traffic conditions
  - Countdown timer

---

## 🧪 Testing API Integration

### Browser Console Tests
Open Developer Tools (F12) → Console, then run:

```javascript
// Import API services (works if on localhost:3000)
const response = await fetch('http://127.0.0.1:8000/api/status');
const data = await response.json();
console.log(data);
// Should show: {backend: "online", models_path: "True", ...}
```

### Check Backend Status
The status badge in the header automatically pings the backend every 30 seconds:
- **Green "SYSTEM OPERATIONAL"** → Backend connected
- **Red "BACKEND OFFLINE"** → Backend unavailable

### View Network Calls
1. Open Dev Tools → Network tab
2. Click "Start Demo"
3. Watch for XHR requests:
   - `GET /api/camera/check/node1`
   - `GET /api/route/eta/node1/node3`

Expected response for route:
```json
{
  "distance_km": 9.37,
  "adjusted_duration_seconds": 1438,
  "eta_minutes": 24.0,
  "route_type": "city_center",
  "traffic_multiplier": 1.8,
  "geometry": [[12.9755, 77.6066], [12.9753, 77.6074], ...]
}
```

---

## 📊 What's Working vs. What's Pending

### ✅ Fully Operational
| Feature | Status |
|---------|--------|
| Backend API server | Running on port 8000 |
| Frontend React app | Running on port 3000 |
| CORS configuration | Allows localhost:3000 |
| OSRM route calculation | Real-time queries working |
| Traffic simulation | 1.8x city center, 1.4x urban, 1.1x highway |
| Map rendering | Dynamic geometry from backend |
| Health monitoring | 30-second interval checks |
| Error handling | Graceful fallback to demo mode |

### ⏳ Waiting for SAM 3 Data
| Feature | Status |
|---------|--------|
| Vehicle detection | Endpoint ready, no data yet |
| Confidence scores | API returns 0.0 until SAM 3 completes |
| Frame previews | Placeholder responses |
| Mask visualization | Needs `models/precomputed/` data |

### 🔜 Next Phase (Real-ESRGAN)
| Feature | Status |
|---------|--------|
| Image enhancement | Placeholder endpoint exists |
| CLI integration | Not started |
| Upscaling workflow | Planned for Phase 6 |

---

## 🐛 Troubleshooting

### Issue: Map doesn't load
**Solution:**
1. Check browser console for errors
2. Verify Leaflet CSS is loading
3. Clear browser cache and refresh

### Issue: Status badge shows "BACKEND OFFLINE"
**Solution:**
1. Verify backend is running:
   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/status"
   ```
2. Check terminal running `uvicorn` for errors
3. Restart backend if needed

### Issue: Route doesn't appear on map
**Solution:**
1. Open browser console and look for API errors
2. Check if OSRM public API is accessible:
   ```powershell
   Invoke-WebRequest -Uri "http://router.project-osrm.org/route/v1/driving/77.6066,12.9756;77.6233,12.9177"
   ```
3. If OSRM is down, demo falls back to hardcoded route

### Issue: Demo button stuck on "Processing..."
**Solution:**
1. Check browser console for JavaScript errors
2. Verify axios is installed: `npm list axios`
3. Check Network tab for failed API calls
4. Restart frontend: `npm start`

---

## 🎯 Next Steps

### For You (User)
1. **Wait for SAM 3 Colab to finish** (~10-15 minutes remaining)
2. **Download `gridlock_precomputed_masks.zip`** from Colab
3. **Extract to:** `models/precomputed/`
4. **Test detection endpoint:**
   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/camera/check/hub_mgroad"
   ```
5. **Click "Start Demo"** again to see real SAM 3 detection data

### For Phase 6 (Real-ESRGAN)
1. Clone Real-ESRGAN repository
2. Integrate CLI into backend `/api/enhance/upload`
3. Test image enhancement workflow
4. Add to demo sequence

### For Final Demo
1. Download 4 Pexels traffic videos
2. Run SAM 3 processing on all videos
3. Create demo script UI with stepper controls
4. Write README.md for judges
5. Full end-to-end testing

---

## 📖 Additional Documentation

- **Integration Details:** `docs/INTEGRATION.md`
- **Setup Instructions:** `docs/SETUP.md`
- **API Reference:** http://127.0.0.1:8000/docs

---

## 🎉 Integration Success!

You now have a fully functional sovereign city security platform with:
- ✅ React frontend with interactive map
- ✅ FastAPI backend with real-time routing
- ✅ OSRM integration for traffic-aware routes
- ✅ Health monitoring and error handling
- ✅ Ready for SAM 3 detection data

**Enjoy the demo!** 🚨🚓🗺️
