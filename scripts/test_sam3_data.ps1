# ==============================================================================
# Test SAM 3 Detection Data Integration
# ==============================================================================

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PrecomputedPath = Join-Path $ProjectRoot "models\precomputed"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Testing SAM 3 Detection Data" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if precomputed directory exists
if (-not (Test-Path $PrecomputedPath)) {
    Write-Host "ERROR: Precomputed directory not found!" -ForegroundColor Red
    Write-Host "Path: $PrecomputedPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Run extract_sam3_data.ps1 first!" -ForegroundColor Yellow
    exit 1
}

Write-Host "Checking precomputed directory..." -ForegroundColor Yellow
Write-Host "Path: $PrecomputedPath" -ForegroundColor White
Write-Host ""

# List all node directories
$NodeDirs = Get-ChildItem -Path $PrecomputedPath -Directory

if ($NodeDirs.Count -eq 0) {
    Write-Host "WARNING: No node directories found!" -ForegroundColor Red
    Write-Host "Extract the SAM 3 data first using extract_sam3_data.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found $($NodeDirs.Count) node(s):" -ForegroundColor Green
Write-Host ""

foreach ($NodeDir in $NodeDirs) {
    Write-Host "Node: $($NodeDir.Name)" -ForegroundColor Cyan
    Write-Host "  Path: $($NodeDir.FullName)" -ForegroundColor White
    
    # Check metadata
    $MetadataPath = Join-Path $NodeDir.FullName "metadata.json"
    if (Test-Path $MetadataPath) {
        Write-Host "  ✅ metadata.json found" -ForegroundColor Green
        
        try {
            $Metadata = Get-Content $MetadataPath | ConvertFrom-Json
            Write-Host "  - Total frames: $($Metadata.total_frames)" -ForegroundColor White
            Write-Host "  - Detected frames: $($Metadata.detected_frames)" -ForegroundColor White
            Write-Host "  - Detection rate: $([math]::Round($Metadata.detection_rate * 100, 2))%" -ForegroundColor White
            
            if ($Metadata.frames.Count -gt 0) {
                $Sample = $Metadata.frames[0]
                Write-Host "  - Sample frame: $($Sample.frame_idx)" -ForegroundColor White
                Write-Host "  - Sample confidence: $([math]::Round($Sample.confidence * 100, 2))%" -ForegroundColor White
                
                # Check if mask file exists
                $SampleMaskPath = Join-Path $NodeDir.FullName $Sample.mask_path
                if (Test-Path $SampleMaskPath) {
                    Write-Host "  ✅ Sample mask file exists" -ForegroundColor Green
                } else {
                    Write-Host "  ⚠️ Sample mask file missing!" -ForegroundColor Yellow
                }
            }
        } catch {
            Write-Host "  ⚠️ Could not parse metadata: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ❌ metadata.json missing!" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Test backend API if running
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Testing Backend API" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$BackendUrl = "http://127.0.0.1:8000"

try {
    Write-Host "Checking backend status..." -ForegroundColor Yellow
    $StatusResponse = Invoke-WebRequest -Uri "$BackendUrl/api/status" -UseBasicParsing -TimeoutSec 5
    $Status = $StatusResponse.Content | ConvertFrom-Json
    
    Write-Host "✅ Backend is online!" -ForegroundColor Green
    Write-Host "  Models path exists: $($Status.models_path)" -ForegroundColor White
    Write-Host ""
    
    # Test camera endpoints
    Write-Host "Testing camera endpoints..." -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($NodeDir in $NodeDirs) {
        $NodeName = $NodeDir.Name
        
        try {
            $CheckUrl = "$BackendUrl/api/camera/check/$NodeName"
            $CheckResponse = Invoke-WebRequest -Uri $CheckUrl -UseBasicParsing -TimeoutSec 5
            $CheckData = $CheckResponse.Content | ConvertFrom-Json
            
            if ($CheckData.found) {
                Write-Host "  ✅ $NodeName - DETECTED" -ForegroundColor Green
                Write-Host "     Confidence: $([math]::Round($CheckData.confidence * 100, 2))%" -ForegroundColor White
            } else {
                Write-Host "  ⚠️ $NodeName - No detection" -ForegroundColor Yellow
                Write-Host "     Message: $($CheckData.message)" -ForegroundColor White
            }
        } catch {
            Write-Host "  ❌ $NodeName - API call failed" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host "⚠️ Backend not running or not accessible" -ForegroundColor Yellow
    Write-Host "Start the backend with:" -ForegroundColor White
    Write-Host "  cd backend; ..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Test Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
