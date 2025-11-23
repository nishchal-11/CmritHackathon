# ==============================================================================
# Extract SAM 3 Detection Data
# ==============================================================================
# Run this after downloading gridlock_precomputed_masks.zip from Google Colab
# ==============================================================================

param(
    [string]$ZipPath = "$env:USERPROFILE\Downloads\gridlock_precomputed_masks.zip"
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$TargetDir = Join-Path $ProjectRoot "models\precomputed"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SAM 3 Detection Data Extraction" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if ZIP exists
if (-not (Test-Path $ZipPath)) {
    Write-Host "ERROR: ZIP file not found at: $ZipPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please specify the correct path:" -ForegroundColor Yellow
    Write-Host "  .\scripts\extract_sam3_data.ps1 -ZipPath 'C:\path\to\gridlock_precomputed_masks.zip'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found ZIP file: $ZipPath" -ForegroundColor Green

# Create target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    Write-Host "Created directory: $TargetDir" -ForegroundColor Green
}

# Extract ZIP
Write-Host ""
Write-Host "Extracting SAM 3 detection data..." -ForegroundColor Yellow

try {
    # Use PowerShell's Expand-Archive
    $TempExtract = Join-Path $env:TEMP "gridlock_temp_extract"
    if (Test-Path $TempExtract) {
        Remove-Item -Recurse -Force $TempExtract
    }
    
    Expand-Archive -Path $ZipPath -DestinationPath $TempExtract -Force
    
    # Find the gridlock_outputs folder
    $OutputsPath = Get-ChildItem -Path $TempExtract -Recurse -Directory | Where-Object { $_.Name -eq "gridlock_outputs" } | Select-Object -First 1
    
    if ($null -eq $OutputsPath) {
        Write-Host "ERROR: Could not find 'gridlock_outputs' folder in ZIP" -ForegroundColor Red
        exit 1
    }
    
    # Copy node directories to target
    $NodeDirs = Get-ChildItem -Path $OutputsPath.FullName -Directory
    
    foreach ($NodeDir in $NodeDirs) {
        $TargetNodeDir = Join-Path $TargetDir $NodeDir.Name
        
        if (Test-Path $TargetNodeDir) {
            Write-Host "  Overwriting: $($NodeDir.Name)" -ForegroundColor Yellow
            Remove-Item -Recurse -Force $TargetNodeDir
        } else {
            Write-Host "  Extracting: $($NodeDir.Name)" -ForegroundColor Green
        }
        
        Copy-Item -Path $NodeDir.FullName -Destination $TargetNodeDir -Recurse -Force
    }
    
    # Clean up temp
    Remove-Item -Recurse -Force $TempExtract
    
    Write-Host ""
    Write-Host "Extraction complete!" -ForegroundColor Green
    
} catch {
    Write-Host "ERROR: Extraction failed: $_" -ForegroundColor Red
    exit 1
}

# Verify extracted data
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Verification Results" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$NodeDirs = Get-ChildItem -Path $TargetDir -Directory

if ($NodeDirs.Count -eq 0) {
    Write-Host "WARNING: No node directories found!" -ForegroundColor Red
    exit 1
}

foreach ($NodeDir in $NodeDirs) {
    Write-Host "Node: $($NodeDir.Name)" -ForegroundColor Cyan
    
    # Check metadata.json
    $MetadataPath = Join-Path $NodeDir.FullName "metadata.json"
    if (Test-Path $MetadataPath) {
        $Metadata = Get-Content $MetadataPath | ConvertFrom-Json
        Write-Host "  Total Frames: $($Metadata.total_frames)" -ForegroundColor White
        Write-Host "  Detected Frames: $($Metadata.detected_frames)" -ForegroundColor Green
        Write-Host "  Detection Rate: $([math]::Round($Metadata.detection_rate * 100, 2))%" -ForegroundColor Yellow
        
        # Count mask files
        $MaskCount = (Get-ChildItem -Path $NodeDir.FullName -Filter "*_mask.png").Count
        $OverlayCount = (Get-ChildItem -Path $NodeDir.FullName -Filter "*_overlay.png").Count
        Write-Host "  Mask Files: $MaskCount" -ForegroundColor White
        Write-Host "  Overlay Files: $OverlayCount" -ForegroundColor White
    } else {
        Write-Host "  ERROR: metadata.json not found!" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "1. Restart your backend server (if running)" -ForegroundColor Yellow
Write-Host "2. Test detection endpoint:" -ForegroundColor Yellow
Write-Host "   Invoke-WebRequest 'http://127.0.0.1:8000/api/camera/check/hub_mgroad'" -ForegroundColor White
Write-Host "3. Open frontend and click 'Start Demo'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Data location: $TargetDir" -ForegroundColor Green
Write-Host ""
