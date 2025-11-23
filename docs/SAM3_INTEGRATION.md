# SAM 3 Integration Guide

## 🎉 Your SAM 3 Processing is Working!

You now have working SAM 3 detection code in Google Colab that:
- ✅ Loads SAM 3 model with trust_remote_code
- ✅ Detects red cars using HSV color detection
- ✅ Generates segmentation masks with bounding boxes
- ✅ Saves masks, overlays, and metadata JSON files
- ✅ Creates downloadable ZIP file

---

## 📥 Step-by-Step Integration

### Step 1: Download the ZIP from Colab

Once your Colab finishes processing, it will download `gridlock_precomputed_masks.zip`. Save it to your Downloads folder.

### Step 2: Extract to Project

**Option A: Automatic Extraction (Recommended)**

Open PowerShell in your project root and run:

```powershell
cd "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss"

# Run extraction script
.\scripts\extract_sam3_data.ps1
```

If the ZIP is in a different location:

```powershell
.\scripts\extract_sam3_data.ps1 -ZipPath "C:\Path\To\gridlock_precomputed_masks.zip"
```

**Option B: Manual Extraction**

1. Right-click `gridlock_precomputed_masks.zip` → Extract All
2. Find the `gridlock_outputs` folder inside
3. Copy all node folders (hub_mgroad, node_1_indiranagar, etc.) to:
   ```
   gridlock-operation-foss\models\precomputed\
   ```

### Step 3: Verify the Data Structure

Your directory should look like this:

```
gridlock-operation-foss/
├── models/
│   └── precomputed/
│       ├── hub_mgroad/
│       │   ├── metadata.json
│       │   ├── frame_00000_mask.png
│       │   ├── frame_00000_overlay.png
│       │   └── ...
│       ├── node_1_indiranagar/
│       │   └── ...
│       ├── node_2_koramangala/
│       │   └── ...
│       └── node_3_silkboard/
│           └── ...
```

### Step 4: Test the Data

Run the test script:

```powershell
.\scripts\test_sam3_data.ps1
```

This will:
- ✅ Check if all node directories exist
- ✅ Verify metadata.json files
- ✅ Count mask and overlay files
- ✅ Test backend API endpoints (if backend is running)

### Step 5: Restart Backend

If your backend is already running, restart it to pick up the new data:

```powershell
# Stop the current backend (Ctrl+C in the terminal)

# Restart it
cd "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss\backend"
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 6: Test Detection Endpoints

With the backend running, test the detection:

```powershell
# Test hub
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/camera/check/hub_mgroad" -UseBasicParsing | Select-Object -ExpandProperty Content

# Test node 1
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/camera/check/node_1_indiranagar" -UseBasicParsing | Select-Object -ExpandProperty Content

# Test all nodes
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/camera/status" -UseBasicParsing | Select-Object -ExpandProperty Content
```

Expected response (if detection found):

```json
{
  "found": true,
  "node": "hub_mgroad",
  "confidence": 0.78,
  "detection_rate": 0.89,
  "frames": [
    {
      "frame_idx": 0,
      "confidence": 0.82,
      "bbox": [120, 340, 580, 720],
      "mask_url": "/static/models/hub_mgroad/frame_00000_mask.png"
    }
  ]
}
```

### Step 7: Test Frontend Integration

1. Open http://localhost:3000 (make sure frontend is running)
2. Status badge should show "SYSTEM OPERATIONAL" (green)
3. Click "🎯 Start Demo" button
4. Watch the console for API calls
5. You should now see **REAL SAM 3 detection data** instead of "No precomputed data available"

---

## 🔍 Understanding the Metadata Format

Each node's `metadata.json` contains:

```json
{
  "node_name": "hub_mgroad",
  "total_frames": 100,
  "detected_frames": 45,
  "detection_rate": 0.45,
  "frames": [
    {
      "frame_idx": 0,
      "confidence": 0.82,
      "bbox": [120, 340, 580, 720],
      "mask_path": "frame_00000_mask.png",
      "overlay_path": "frame_00000_overlay.png"
    }
  ]
}
```

**Fields:**
- `node_name`: Camera node identifier
- `total_frames`: Total frames processed
- `detected_frames`: Frames where red car was detected
- `detection_rate`: Percentage (0.0 to 1.0)
- `frames`: Array of detection results per frame
  - `frame_idx`: Frame number
  - `confidence`: Detection confidence (0.0 to 1.0)
  - `bbox`: Bounding box [x1, y1, x2, y2]
  - `mask_path`: Relative path to mask PNG
  - `overlay_path`: Relative path to overlay PNG

---

## 🎯 What Happens Next

Once the data is extracted:

1. **Backend automatically serves it** via `/api/camera/check/{node_name}`
2. **Frontend displays real detection data** when you click "Start Demo"
3. **Mask images are accessible** at `/static/models/{node_name}/{mask_file}`
4. **No code changes needed** - everything is already wired up!

---

## 🐛 Troubleshooting

### Issue: "No precomputed data available"

**Solution:**
1. Check if `models/precomputed/` exists
2. Run `.\scripts\test_sam3_data.ps1` to verify structure
3. Ensure metadata.json files are present
4. Restart backend server

### Issue: "Models path: False"

**Solution:**
```powershell
# Verify directory exists
Test-Path "c:\Users\Nishc\OneDrive\Desktop\cmrit hacakthon\gridlock-operation-foss\models\precomputed"

# Create if missing
New-Item -ItemType Directory -Path "models\precomputed" -Force
```

### Issue: Masks not displaying on frontend

**Solution:**
1. Check browser Network tab for 404 errors
2. Verify mask files exist in node directories
3. Check backend logs for static file mounting errors
4. Ensure filenames in metadata.json match actual files

### Issue: Low detection rate

**Possible causes:**
- Video doesn't contain red cars
- Red car detection threshold too strict
- Video quality too low

**Solution:**
- Upload a video with clear red vehicles
- Adjust HSV color ranges in Colab code
- Use higher quality videos

---

## 📊 Demo Flow with Real SAM 3 Data

1. **User clicks "Start Demo"**
2. **Frontend calls:** `GET /api/camera/check/node_1_indiranagar`
3. **Backend reads:** `models/precomputed/node_1_indiranagar/metadata.json`
4. **Backend returns:** Detection confidence, bbox, frame count
5. **Frontend displays:** "✅ Target Detected: Indiranagar (Confidence: 78%)"
6. **Route calculation continues** with real detection coordinates
7. **User sees:** Real mask overlays and detection statistics

---

## 🎉 You're Done!

Your Operation Gridlock demo now has:
- ✅ Real SAM 3 vehicle detection
- ✅ Precomputed masks for fast playback
- ✅ Metadata with confidence scores
- ✅ Full frontend-backend integration
- ✅ Professional demo flow

**Next:** Run `.\scripts\extract_sam3_data.ps1` and watch the magic happen! 🚀
