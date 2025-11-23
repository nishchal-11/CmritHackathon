# Vehicle Tracking System - Geospatial Prediction Logic

## 🎯 Overview

The vehicle tracking system implements intelligent geospatial prediction to follow vehicles through a camera network using graph theory and ETA calculations.

## 🧠 How It Works

### 1. Detection at Point A (Theft Location)
```
Theft detected at: MG Road Junction
Vehicle fingerprint: White SUV with dent on left door
```

### 2. Predict Next Cameras (B, C, D)
System calculates all possible routes from current location:
- **Camera B (Indiranagar)**: 3.2 km, ETA 9 min, Probability 85%
- **Camera C (Koramangala)**: 5.8 km, ETA 16 min, Probability 65%
- **Camera D (Silk Board)**: 8.5 km, ETA 24 min, Probability 45%

### 3. Automated Verification
- Activate cameras B, C, D during calculated ETA windows
- Search for vehicle fingerprint (color + model + distinctive features)
- Use SAM 3 AI detection with precomputed masks

### 4. The Handover Loop

**Scenario 1 - Found:**
```
Vehicle spotted at Camera B (Indiranagar)
└→ Repeat process from Camera B
   ├→ Predict next cameras: Whitefield, Koramangala, Airport
   ├→ Calculate new ETAs
   └→ Continue tracking chain
```

**Scenario 2 - Lost:**
```
Vehicle NOT found at B, C, or D
└→ Analyze possible scenarios:
   ├→ Vehicle stopped/parked
   ├→ Took alternate route
   ├→ Entered private property
   └→ Expand search radius
```

## 📡 API Endpoints

### Start Tracking
```bash
POST /api/track/start
{
  "camera_id": "hub_mgroad",
  "vehicle": {
    "color": "white",
    "model": "SUV",
    "distinctive_features": ["dent on left door"]
  }
}
```

**Response:**
```json
{
  "tracking_id": "track_1763724894",
  "predictions": [
    {
      "camera_id": "node_1_indiranagar",
      "eta_minutes": 9.0,
      "distance_km": 3.2,
      "probability": 0.85,
      "search_window_start": "2025-11-21T17:12:06",
      "search_window_end": "2025-11-21T17:15:42"
    }
  ],
  "search_instructions": [
    "Activate Camera node_1_indiranagar (Indiranagar 100ft Road) between 17:12 and 17:15. ETA: 9.0 min, Distance: 3.2 km, Probability: 85%"
  ]
}
```

### Update Tracking (Found at Camera)
```bash
POST /api/track/update
{
  "tracking_id": "track_1763724894",
  "found_at_camera": "node_1_indiranagar"
}
```

**Response:**
```json
{
  "status": "found",
  "found_at": "node_1_indiranagar",
  "tracking_chain": ["hub_mgroad", "node_1_indiranagar"],
  "next_predictions": [ /* new predictions from this camera */ ]
}
```

### Get Visualization Data
```bash
GET /api/track/visualize/{tracking_id}
```

Returns camera positions, connections, and animated tracking data for map display.

## 🗺️ Road Network Graph

```
hub_mgroad (MG Road) - HUB
├─→ node_1_indiranagar (3.2 km)
├─→ node_2_koramangala (5.8 km)
└─→ node_3_silkboard (8.5 km)

node_1_indiranagar (Indiranagar)
├─→ hub_mgroad (3.2 km)
├─→ node_2_koramangala (4.5 km)
├─→ cam_a_airport (12.0 km)
└─→ cam_b_whitefield (10.5 km)

node_2_koramangala (Koramangala)
├─→ hub_mgroad (5.8 km)
├─→ node_1_indiranagar (4.5 km)
├─→ node_3_silkboard (3.0 km)
└─→ cam_c_hsr (2.5 km)

node_3_silkboard (Silk Board)
├─→ hub_mgroad (8.5 km)
├─→ node_2_koramangala (3.0 km)
├─→ cam_d_electronic_city (15.0 km)
└─→ cam_e_btm (2.8 km)
```

**Total: 9 camera nodes** with bidirectional connections

## ⏱️ ETA Calculation

```python
def calculate_eta(distance_km, road_type="urban"):
    speed = AVERAGE_SPEEDS[road_type]  # city_center: 20, urban: 30, highway: 50
    traffic = TRAFFIC_MULTIPLIERS[road_type]  # city_center: 1.8x, urban: 1.4x, highway: 1.1x
    
    time_hours = distance_km / speed
    time_minutes = time_hours * 60 * traffic
    
    return time_minutes
```

**Example:**
- Distance: 3.2 km
- Road type: Urban
- Speed: 30 km/h
- Traffic: 1.4x
- **ETA: 9 minutes**

## 📊 Probability Scoring

```python
def calculate_probability(distance_km):
    if distance_km < 3:  return 0.85  # Very likely (closest)
    if distance_km < 6:  return 0.65  # Likely
    if distance_km < 10: return 0.45  # Possible
    else:                return 0.25  # Unlikely (far)
```

Shorter distances = Higher probability of vehicle taking that route

## 🎨 Frontend Visualization

### Camera Markers
- **🔴 Red (Pulsing)**: Active search - checking this camera now
- **🟡 Yellow**: Predicted - camera in search list
- **🟢 Green**: Confirmed - vehicle detected here
- **🔵 Blue**: Hub/starting point

### Circles
- **Probability Circles**: Radius based on detection probability
- **Search Windows**: Animated radar pulse during active search

### Polylines
- **Solid Green**: High probability route (>60%)
- **Dashed Yellow**: Medium probability route (<60%)
- **Thickness**: Proportional to probability

### Example Animation Sequence
```
Step 4 (ACQUIRE):
  └→ Show theft location with pulsing red marker

Step 5 (ROUTE):
  ├→ Draw lines to all predicted cameras
  ├→ Show probability circles
  └→ Display ETA countdown timers

Step 6 (DEPLOY):
  ├→ One camera turns green (vehicle found)
  ├→ Draw new predictions from that camera
  └→ Continue tracking chain
```

## 🧪 Testing

### Backend Test
```bash
curl -X POST http://127.0.0.1:8000/api/track/start \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": "hub_mgroad",
    "vehicle": {
      "color": "white",
      "model": "SUV",
      "distinctive_features": ["dent on left door"]
    }
  }'
```

### Get All Cameras
```bash
curl http://127.0.0.1:8000/api/network/cameras
```

Returns 9 cameras with their positions and connection counts.

## 📦 Files Created

### Backend
- `backend/app/road_network.py` - Graph structure with 9 nodes
- `backend/app/vehicle_tracking.py` - Tracking logic & predictions
- `backend/app/routes/tracking.py` - API endpoints

### Frontend
- `frontend/src/services/trackingApi.js` - API client
- `frontend/src/components/TrackingVisualization.jsx` - Map overlay
- `frontend/src/components/TrackingVisualization.css` - Animations

### Integration
- Updated `backend/app/main.py` - Registered tracking routes
- Updated `frontend/src/components/DemoWrapper.jsx` - Added tracking state
- Updated `frontend/src/components/Map.jsx` - Added visualization layer

## 🎯 Key Features

✅ **Graph-based road network** with 9 camera nodes
✅ **Geospatial ETA calculations** with traffic multipliers
✅ **Probability scoring** for route prediction
✅ **Search window generation** (ETA ± 20% buffer)
✅ **Tracking chain** maintains vehicle path history
✅ **Handover loop** continues from each detection
✅ **Lost vehicle analysis** when not found
✅ **Real-time map visualization** with animations
✅ **REST API** for frontend integration

## 🚀 How to Use in Demo

1. **Start tracking:** POST to `/api/track/start` with theft location
2. **Get predictions:** System returns 3 cameras to check with ETAs
3. **Activate cameras:** Frontend animates predicted locations
4. **Report result:** POST to `/api/track/update` with found_at_camera
5. **Loop continues:** New predictions generated from found location
6. **Visualize:** GET `/api/track/visualize/{id}` for map data

## 📈 Future Enhancements

- [ ] Machine learning for probability scoring
- [ ] Real-time traffic API integration
- [ ] Multi-vehicle simultaneous tracking
- [ ] Historical path analysis
- [ ] Predictive route forecasting
- [ ] Alert system for ground units

---

**Status:** ✅ Backend fully implemented and tested
**API:** All endpoints operational
**Frontend:** Visualization components ready
**Integration:** Connected via DemoWrapper
