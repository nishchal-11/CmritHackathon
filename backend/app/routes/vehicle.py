"""
Vehicle upload and management endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
import json
from typing import Dict, Any, Optional
import shutil
from datetime import datetime

router = APIRouter()

# Path to store uploaded vehicle files
UPLOADS_PATH = Path(__file__).parent.parent.parent.parent / "assets" / "vehicle_uploads"
UPLOADS_PATH.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_vehicle(
    file: UploadFile = File(...),
    license_plate: str = Form(default=""),
    color: str = Form(default=""),
    model: str = Form(default=""),
    description: str = Form(default="")
) -> Dict[str, Any]:
    """
    Upload vehicle image or video for investigation
    
    Args:
        file: Image or video file
        license_plate: Vehicle license plate number
        color: Vehicle color
        model: Vehicle model/type
        description: Additional description or distinctive features
    
    Returns:
        Upload status and vehicle information
    """
    try:
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(file.filename).suffix
        new_filename = f"vehicle_{timestamp}{file_extension}"
        
        file_path = UPLOADS_PATH / new_filename
        
        # Save the uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        # Create vehicle record
        vehicle_record = {
            "id": timestamp,
            "filename": new_filename,
            "file_path": str(file_path),
            "file_size_mb": round(file_size_mb, 2),
            "upload_time": timestamp,
            "license_plate": license_plate or "Unknown",
            "color": color or "Unknown",
            "model": model or "Unknown",
            "description": description or "",
            "status": "uploaded"
        }
        
        # Save vehicle metadata
        metadata_file = UPLOADS_PATH / f"vehicle_{timestamp}_metadata.json"
        with metadata_file.open("w") as f:
            json.dump(vehicle_record, f, indent=2)
        
        return {
            "status": "success",
            "message": "Vehicle uploaded successfully",
            "data": vehicle_record
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading vehicle: {str(e)}")


@router.get("/list")
async def list_vehicles() -> Dict[str, Any]:
    """
    List all uploaded vehicles
    
    Returns:
        List of vehicle records
    """
    try:
        vehicles = []
        
        for metadata_file in UPLOADS_PATH.glob("*_metadata.json"):
            try:
                with metadata_file.open("r") as f:
                    vehicle_data = json.load(f)
                    vehicles.append(vehicle_data)
            except:
                continue
        
        # Sort by upload time (newest first)
        vehicles.sort(key=lambda x: x.get("upload_time", ""), reverse=True)
        
        return {
            "status": "success",
            "count": len(vehicles),
            "vehicles": vehicles
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing vehicles: {str(e)}")


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: str) -> Dict[str, Any]:
    """
    Get specific vehicle information
    
    Args:
        vehicle_id: Vehicle ID (timestamp)
    
    Returns:
        Vehicle record
    """
    try:
        metadata_file = UPLOADS_PATH / f"vehicle_{vehicle_id}_metadata.json"
        
        if not metadata_file.exists():
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        with metadata_file.open("r") as f:
            vehicle_data = json.load(f)
        
        return {
            "status": "success",
            "data": vehicle_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving vehicle: {str(e)}")
