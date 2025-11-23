# Test Vehicle Tracking System
# Demonstrates the geospatial prediction logic

Write-Host "=== OPERATION GRIDLOCK - Vehicle Tracking System Test ===" -ForegroundColor Green
Write-Host ""

# Test 1: Start tracking from MG Road
Write-Host "[STEP 1] Vehicle detected at MG Road (theft location)" -ForegroundColor Cyan
$startTracking = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/track/start" -Method POST -Body (@{
    camera_id = "hub_mgroad"
    vehicle = @{
        color = "white"
        model = "SUV"
        distinctive_features = @("dent on left door", "broken taillight")
    }
} | ConvertTo-Json) -ContentType "application/json"

Write-Host "✓ Tracking started: $($startTracking.data.tracking_id)" -ForegroundColor Green
Write-Host "✓ Initial detection: $($startTracking.data.initial_detection.camera_name)" -ForegroundColor Green
Write-Host ""

# Show predictions
Write-Host "[PREDICTIONS] System is checking these cameras:" -ForegroundColor Yellow
foreach ($pred in $startTracking.data.predictions) {
    Write-Host "  📹 $($pred.camera_name)" -ForegroundColor White
    Write-Host "     - Distance: $($pred.distance_km) km" -ForegroundColor Gray
    Write-Host "     - ETA: $($pred.eta_minutes) minutes" -ForegroundColor Gray
    Write-Host "     - Probability: $([math]::Round($pred.probability * 100))%" -ForegroundColor Gray
    Write-Host "     - Road: $($pred.road_name)" -ForegroundColor Gray
    Write-Host ""
}

# Simulate finding vehicle at Indiranagar (highest probability)
$tracking_id = $startTracking.data.tracking_id
Start-Sleep -Seconds 2

Write-Host "[STEP 2] Vehicle FOUND at Indiranagar!" -ForegroundColor Green
$updateTracking = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/track/update" -Method POST -Body (@{
    tracking_id = $tracking_id
    found_at_camera = "node_1_indiranagar"
} | ConvertTo-Json) -ContentType "application/json"

Write-Host "Status: $($updateTracking.data.status)" -ForegroundColor Green
Write-Host "Found at: $($updateTracking.data.found_at)" -ForegroundColor Green
$chain = $updateTracking.data.tracking_chain -join " -> "
Write-Host "Tracking chain: $chain" -ForegroundColor Cyan
Write-Host ""

# Show next predictions
Write-Host "[NEW PREDICTIONS] Now checking from Indiranagar:" -ForegroundColor Yellow
foreach ($pred in $updateTracking.data.next_predictions) {
    Write-Host "  📹 $($pred.camera_name)" -ForegroundColor White
    Write-Host "     - Distance: $($pred.distance_km) km" -ForegroundColor Gray
    Write-Host "     - ETA: $($pred.eta_minutes) minutes" -ForegroundColor Gray
    Write-Host "     - Probability: $([math]::Round($pred.probability * 100))%" -ForegroundColor Gray
    Write-Host ""
}

# Test visualization data
Write-Host "[VISUALIZATION] Getting map data..." -ForegroundColor Cyan
$vizData = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/track/visualize/$tracking_id" -Method GET

Write-Host "✓ Tracking chain cameras: $($vizData.data.tracking_chain.Count)" -ForegroundColor Green
Write-Host "✓ Predicted cameras: $($vizData.data.predicted_cameras.Count)" -ForegroundColor Green
Write-Host "✓ Road connections: $($vizData.data.connections.Count)" -ForegroundColor Green
Write-Host ""

Write-Host "=== TEST COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "   - Vehicle tracked through $($updateTracking.data.tracking_chain.Count) cameras"
Write-Host "   - $($updateTracking.data.next_predictions.Count) new predictions generated"
Write-Host "   - System ready for continuous tracking loop"
Write-Host ""
Write-Host "Next step: Check frontend at http://localhost:3000" -ForegroundColor Yellow
