"""
Camera surveillance endpoints
Handles checking camera feeds for vehicle detection
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
import json
from typing import Dict, Any
import shutil
from datetime import datetime

router = APIRouter()

# Path to precomputed masks
MODELS_PATH = Path(__file__).parent.parent.parent.parent / "models" / "precomputed"
# Path to store uploaded videos
UPLOADS_PATH = Path(__file__).parent.parent.parent.parent / "assets" / "videos"
UPLOADS_PATH.mkdir(parents=True, exist_ok=True)


@router.get("/check/{node_name}")
async def check_camera(node_name: str) -> Dict[str, Any]:
    """
    Check if target vehicle is detected at a specific node
    
    Args:
        node_name: Name of the node (e.g., 'node_1_indiranagar')
    
    Returns:
        Detection result with confidence, frame info, and mask paths
    """
    # Map friendly names to directory names
    node_mapping = {
        "node1": "node_1_indiranagar",
        "node_1": "node_1_indiranagar",
        "indiranagar": "node_1_indiranagar",
        "node2": "node_2_koramangala",
        "node_2": "node_2_koramangala",
        "koramangala": "node_2_koramangala",
        "node3": "node_3_silkboard",
        "node_3": "node_3_silkboard",
        "silkboard": "node_3_silkboard",
        "hub": "hub_mgroad",
        "mgroad": "hub_mgroad"
    }
    
    # Normalize node name
    normalized_name = node_mapping.get(node_name.lower(), node_name)
    node_dir = MODELS_PATH / normalized_name
    metadata_file = node_dir / "metadata.json"
    
    # Check if precomputed data exists
    if not metadata_file.exists():
        return {
            "found": False,
            "node": normalized_name,
            "message": "No precomputed data available. Run SAM 3 processing in Colab first.",
            "confidence": 0.0
        }
    
    # Load metadata
    try:
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        if not metadata.get("frames") or len(metadata["frames"]) == 0:
            return {
                "found": False,
                "node": normalized_name,
                "message": "No vehicle detected in this camera feed",
                "confidence": 0.0,
                "total_frames": metadata.get("total_frames", 0)
            }
        
        # Get the frame with highest confidence
        best_detection = max(metadata["frames"], key=lambda x: x["confidence"])
        
        return {
            "found": True,
            "node": normalized_name,
            "node_display": metadata.get("node_name", normalized_name),
            "confidence": best_detection["confidence"],
            "frame_idx": best_detection["frame_idx"],
            "bbox": best_detection.get("bbox"),
            "mask_path": f"/static/models/{normalized_name}/{best_detection['mask_path']}",
            "overlay_path": f"/static/models/{normalized_name}/{best_detection['overlay_path']}",
            "detection_rate": metadata.get("detection_rate", 0),
            "total_frames": metadata.get("total_frames", 0),
            "detected_frames": metadata.get("detected_frames", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading metadata: {str(e)}")


@router.get("/status")
async def camera_status() -> Dict[str, Any]:
    """
    Get status of all camera nodes
    
    Returns:
        Status of each camera node with detection counts
    """
    nodes = ["node_1_indiranagar", "node_2_koramangala", "node_3_silkboard", "hub_mgroad"]
    status = {}
    
    for node in nodes:
        node_dir = MODELS_PATH / node
        metadata_file = node_dir / "metadata.json"
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                status[node] = {
                    "available": True,
                    "total_frames": metadata.get("total_frames", 0),
                    "detected_frames": metadata.get("detected_frames", 0),
                    "detection_rate": metadata.get("detection_rate", 0)
                }
            except:
                status[node] = {"available": False, "error": "Failed to read metadata"}
        else:
            status[node] = {"available": False, "message": "No data"}
    
    return {
        "status": "operational",
        "nodes": status,
        "precomputed_path": str(MODELS_PATH.exists())
    }


@router.post("/scan-all")
async def scan_all_cameras() -> Dict[str, Any]:
    """
    Simulate scanning all camera nodes for target
    
    Returns:
        Results from all nodes
    """
    nodes = ["node_1_indiranagar", "node_2_koramangala", "node_3_silkboard", "hub_mgroad"]
    results = {}
    
    for node in nodes:
        try:
            result = await check_camera(node)
            results[node] = result
        except Exception as e:
            results[node] = {"found": False, "error": str(e)}
    
    # Find best detection
    detections = [r for r in results.values() if r.get("found", False)]
    
    return {
        "scanned_nodes": len(nodes),
        "detections_found": len(detections),
        "results": results,
        "best_detection": max(detections, key=lambda x: x["confidence"]) if detections else None
    }


@router.post("/upload-video")
async def upload_video(
    video: UploadFile = File(...),
    camera_name: str = Form(...),
    camera_index: str = Form(...)
) -> Dict[str, Any]:
    """
    Upload a video file for a specific camera
    
    Args:
        video: The video file to upload
        camera_name: Name of the camera
        camera_index: Index of the camera
    
    Returns:
        Upload status and file information
    """
    try:
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(video.filename).suffix
        safe_camera_name = camera_name.replace(" ", "_").replace(",", "")
        new_filename = f"camera_{camera_index}_{safe_camera_name}_{timestamp}{file_extension}"
        
        file_path = UPLOADS_PATH / new_filename
        
        # Save the uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        return {
            "status": "success",
            "message": "Video uploaded successfully",
            "camera_name": camera_name,
            "camera_index": camera_index,
            "filename": new_filename,
            "file_size_mb": round(file_size_mb, 2),
            "upload_time": timestamp,
            "file_path": str(file_path)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {str(e)}")
