"""
API endpoints for vehicle tracking system
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
from app.vehicle_tracking import vehicle_tracker

router = APIRouter()

class VehicleFingerprint(BaseModel):
    color: str
    model: str
    license_plate: Optional[str] = None
    distinctive_features: List[str] = []  # e.g., ["dent on left door", "roof rack"]

class StartTrackingRequest(BaseModel):
    camera_id: str
    vehicle: VehicleFingerprint
    detection_time: Optional[str] = None  # ISO format

class DetectionResultRequest(BaseModel):
    tracking_id: str
    found_at_camera: Optional[str] = None  # None if not found
    detection_time: Optional[str] = None

@router.post("/track/start")
async def start_tracking(request: StartTrackingRequest):
    """
    Start tracking a vehicle from initial detection point
    
    Example:
    {
        "camera_id": "hub_mgroad",
        "vehicle": {
            "color": "white",
            "model": "SUV",
            "distinctive_features": ["dent on left door"]
        }
    }
    """
    try:
        detection_time = None
        if request.detection_time:
            detection_time = datetime.fromisoformat(request.detection_time)
        
        session = vehicle_tracker.track_vehicle(
            start_camera_id=request.camera_id,
            vehicle_fingerprint=request.vehicle.dict(),
            detection_time=detection_time
        )
        
        return {
            "success": True,
            "data": session
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/track/auto")
async def start_auto_tracking(request: StartTrackingRequest):
    """
    Start AUTOMATIC tracking with complete camera checking loop
    
    This implements the full system:
    1. Detect vehicle at initial camera (theft location)
    2. Predict ALL possible next cameras
    3. Check ALL predicted cameras for vehicle
    4. When found, repeat from new camera
    5. Continue until vehicle lost or max hops reached
    
    Example:
    {
        "camera_id": "hub_mgroad",
        "vehicle": {
            "color": "white",
            "model": "SUV",
            "license_plate": "KA01AB1234",
            "distinctive_features": ["dent on left door", "roof rack"]
        }
    }
    
    Returns complete tracking history with all camera checks
    """
    try:
        detection_time = None
        if request.detection_time:
            detection_time = datetime.fromisoformat(request.detection_time)
        
        # Run automatic tracking loop
        session = vehicle_tracker.auto_track_vehicle(
            start_camera_id=request.camera_id,
            vehicle_fingerprint=request.vehicle.dict(),
            max_hops=10,  # Maximum 10 camera jumps
            detection_time=detection_time
        )
        
        return {
            "success": True,
            "data": session,
            "message": f"Auto-tracking completed: {session['total_hops']} hops, {session['final_status']['total_cameras_checked']} cameras checked"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/track/update")
async def update_tracking(request: DetectionResultRequest):
    """
    Update tracking with detection result from predicted cameras
    
    Example (Found):
    {
        "tracking_id": "track_1732167890",
        "found_at_camera": "node_1_indiranagar"
    }
    
    Example (Lost):
    {
        "tracking_id": "track_1732167890",
        "found_at_camera": null
    }
    """
    try:
        detection_time = None
        if request.detection_time:
            detection_time = datetime.fromisoformat(request.detection_time)
        
        result = vehicle_tracker.handle_detection_result(
            tracking_id=request.tracking_id,
            found_at_camera=request.found_at_camera,
            detection_time=detection_time
        )
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/track/status/{tracking_id}")
async def get_tracking_status(tracking_id: str):
    """Get current status of a tracking session"""
    session = vehicle_tracker.get_tracking_status(tracking_id)
    if not session:
        raise HTTPException(status_code=404, detail="Tracking session not found")
    
    return {
        "success": True,
        "data": session
    }

@router.get("/track/visualize/{tracking_id}")
async def get_visualization_data(tracking_id: str):
    """
    Get tracking data formatted for map visualization
    Returns camera locations, connections, and search windows
    """
    viz_data = vehicle_tracker.get_tracking_visualization_data(tracking_id)
    
    if "error" in viz_data:
        raise HTTPException(status_code=404, detail=viz_data["error"])
    
    return {
        "success": True,
        "data": viz_data
    }

@router.get("/network/cameras")
async def get_all_cameras():
    """Get list of all cameras in the network"""
    from app.road_network import ROAD_NETWORK
    
    cameras = []
    for cam_id, cam_data in ROAD_NETWORK.items():
        cameras.append({
            "id": cam_id,
            "name": cam_data["name"],
            "lat": cam_data["lat"],
            "lng": cam_data["lng"],
            "type": cam_data["type"],
            "connections_count": len(cam_data["connections"])
        })
    
    return {
        "success": True,
        "data": cameras,
        "total": len(cameras)
    }

@router.get("/network/connections/{camera_id}")
async def get_camera_connections(camera_id: str):
    """Get all roads/connections from a specific camera"""
    from app.road_network import get_connected_cameras, get_camera_info
    
    camera_info = get_camera_info(camera_id)
    if not camera_info:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    connections = get_connected_cameras(camera_id)
    
    return {
        "success": True,
        "data": {
            "camera": {
                "id": camera_id,
                "name": camera_info["name"],
                "lat": camera_info["lat"],
                "lng": camera_info["lng"]
            },
            "connections": connections
        }
    }
