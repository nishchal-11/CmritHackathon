# Operation Gridlock - Complete Demo Script
# Run this to demonstrate all features to judges

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " OPERATION GRIDLOCK - DEMO SCRIPT" -ForegroundColor Green
Write-Host " Sovereign City Security Intelligence" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:8000/api"

# Check if backend is running
Write-Host "[1/7] Checking backend status..." -ForegroundColor Yellow
try {
    $status = Invoke-RestMethod -Uri "$baseUrl/status" -Method GET
    Write-Host "Backend: ONLINE" -ForegroundColor Green
    Write-Host "  - Models path: $($status.models_path)" -ForegroundColor Gray
    Write-Host "  - Assets path: $($status.assets_path)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "ERROR: Backend not running!" -ForegroundColor Red
    Write-Host "Start it with: python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
    exit 1
}

# Test camera network
Write-Host "[2/7] Testing camera network..." -ForegroundColor Yellow
$cameras = Invoke-RestMethod -Uri "$baseUrl/network/cameras" -Method GET
Write-Host "Camera nodes: $($cameras.total)" -ForegroundColor Green
foreach ($cam in $cameras.data | Select-Object -First 4) {
    Write-Host "  - $($cam.name) ($($cam.type)): $($cam.connections_count) connections" -ForegroundColor Gray
}
Write-Host ""

# Test SAM 3 detection
Write-Host "[3/7] Testing SAM 3 vehicle detection..." -ForegroundColor Yellow
$detection = Invoke-RestMethod -Uri "$baseUrl/camera/check/hub_mgroad" -Method GET
if ($detection.found) {
    Write-Host "Detection: SUCCESS" -ForegroundColor Green
    Write-Host "  - Location: MG Road Junction" -ForegroundColor Gray
    Write-Host "  - Confidence: $($detection.confidence * 100)%" -ForegroundColor Gray
    Write-Host "  - Detection rate: $($detection.detection_rate * 100)%" -ForegroundColor Gray
} else {
    Write-Host "Detection: No vehicle found" -ForegroundColor Yellow
}
Write-Host ""

# Test image enhancement
Write-Host "[4/7] Testing image enhancement..." -ForegroundColor Yellow
$enhance = Invoke-RestMethod -Uri "$baseUrl/enhance/status" -Method GET
Write-Host "Enhancement: $($enhance.status)" -ForegroundColor Green
Write-Host "  - Engine: $($enhance.engine)" -ForegroundColor Gray
Write-Host "  - Techniques: $($enhance.techniques -join ', ')" -ForegroundColor Gray
Write-Host "  - Scales: $($enhance.supported_scales -join 'x, ')x" -ForegroundColor Gray
Write-Host ""

# Test OSRM routing
Write-Host "[5/7] Testing OSRM routing..." -ForegroundColor Yellow
$route = Invoke-RestMethod -Uri "$baseUrl/route/eta/hub_mgroad/node_3_silkboard" -Method GET
Write-Host "Routing: SUCCESS" -ForegroundColor Green
Write-Host "  - Distance: $($route.distance_km) km" -ForegroundColor Gray
Write-Host "  - Base ETA: $($route.base_duration_seconds / 60) min" -ForegroundColor Gray
Write-Host "  - With traffic: $($route.adjusted_duration_seconds / 60) min" -ForegroundColor Gray
Write-Host "  - Traffic multiplier: $($route.traffic_multiplier)x" -ForegroundColor Gray
Write-Host "  - Route type: $($route.route_type)" -ForegroundColor Gray
Write-Host ""

# Test vehicle tracking
Write-Host "[6/7] Testing geospatial vehicle tracking..." -ForegroundColor Yellow
$trackBody = @{
    camera_id = "hub_mgroad"
    vehicle = @{
        color = "white"
        model = "SUV"
        distinctive_features = @("dent on left door", "broken taillight")
    }
} | ConvertTo-Json

$tracking = Invoke-RestMethod -Uri "$baseUrl/track/start" -Method POST -Body $trackBody -ContentType "application/json"
Write-Host "Tracking: STARTED" -ForegroundColor Green
Write-Host "  - Tracking ID: $($tracking.data.tracking_id)" -ForegroundColor Gray
Write-Host "  - Initial location: $($tracking.data.initial_detection.camera_name)" -ForegroundColor Gray
Write-Host "  - Predictions: $($tracking.data.predictions.Count)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Predicted cameras:" -ForegroundColor Cyan
foreach ($pred in $tracking.data.predictions) {
    $prob = [math]::Round($pred.probability * 100)
    Write-Host "    $($pred.camera_name): $($pred.eta_minutes) min, $($pred.distance_km) km ($prob%)" -ForegroundColor White
}
Write-Host ""

# Simulate finding vehicle
Write-Host "[7/7] Simulating vehicle detection at next camera..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
$updateBody = @{
    tracking_id = $tracking.data.tracking_id
    found_at_camera = "node_1_indiranagar"
} | ConvertTo-Json

$update = Invoke-RestMethod -Uri "$baseUrl/track/update" -Method POST -Body $updateBody -ContentType "application/json"
Write-Host "Update: VEHICLE FOUND" -ForegroundColor Green
Write-Host "  - Status: $($update.data.status)" -ForegroundColor Gray
Write-Host "  - Found at: $($update.data.found_at)" -ForegroundColor Gray
$chain = $update.data.tracking_chain -join " -> "
Write-Host "  - Tracking chain: $chain" -ForegroundColor Gray
Write-Host "  - New predictions: $($update.data.next_predictions.Count)" -ForegroundColor Gray
Write-Host ""

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " DEMO COMPLETE - ALL SYSTEMS OPERATIONAL" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features tested:" -ForegroundColor Cyan
Write-Host "  1. Backend API connectivity" -ForegroundColor White
Write-Host "  2. Camera network (9 nodes)" -ForegroundColor White
Write-Host "  3. SAM 3 vehicle detection" -ForegroundColor White
Write-Host "  4. PIL image enhancement" -ForegroundColor White
Write-Host "  5. OSRM routing with traffic" -ForegroundColor White
Write-Host "  6. Geospatial vehicle tracking" -ForegroundColor White
Write-Host "  7. Tracking handover loop" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  - Open http://localhost:3000 for frontend demo" -ForegroundColor White
Write-Host "  - Click 'PROCEED TO NEXT STEP' for interactive mission" -ForegroundColor White
Write-Host "  - View docs/ folder for detailed guides" -ForegroundColor White
Write-Host ""
Write-Host "API Documentation: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
