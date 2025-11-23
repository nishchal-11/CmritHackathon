"""
Route calculation and ETA prediction endpoints
Uses OSRM for routing with simulated traffic
"""
from fastapi import APIRouter, HTTPException
import httpx
from typing import Dict, Any, List
import asyncio

router = APIRouter()

# OSRM base URL (public demo server)
OSRM_BASE_URL = "http://router.project-osrm.org"

# Traffic simulation multipliers
TRAFFIC_MULTIPLIERS = {
    "city_center": 1.8,  # Heavy traffic (MG Road, Koramangala)
    "urban": 1.4,        # Medium traffic (Indiranagar)
    "highway": 1.1       # Light traffic (Silk Board exit)
}


async def get_osrm_route(start_lat: float, start_lng: float, 
                         end_lat: float, end_lng: float) -> Dict[str, Any]:
    """
    Get route from OSRM API
    
    Returns:
        Route with geometry, distance, and duration
    """
    url = f"{OSRM_BASE_URL}/route/v1/driving/{start_lng},{start_lat};{end_lng},{end_lat}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != "Ok":
                raise HTTPException(status_code=400, detail="OSRM routing failed")
            
            route = data["routes"][0]
            return {
                "distance": route["distance"],  # meters
                "duration": route["duration"],  # seconds
                "geometry": route["geometry"]["coordinates"],  # [[lng, lat], ...]
                "steps": len(route.get("legs", [{}])[0].get("steps", []))
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"OSRM service unavailable: {str(e)}")


def apply_traffic_simulation(base_duration: float, route_type: str) -> float:
    """
    Apply traffic multiplier to base duration
    
    Args:
        base_duration: Base travel time in seconds
        route_type: Type of route ('city_center', 'urban', 'highway')
    
    Returns:
        Adjusted duration in seconds
    """
    multiplier = TRAFFIC_MULTIPLIERS.get(route_type, 1.3)
    return base_duration * multiplier


@router.post("/calculate")
async def calculate_route(
    start_lat: float,
    start_lng: float,
    end_lat: float,
    end_lng: float,
    route_type: str = "urban"
) -> Dict[str, Any]:
    """
    Calculate route with traffic simulation
    
    Body params:
        start_lat, start_lng: Starting coordinates
        end_lat, end_lng: Destination coordinates
        route_type: 'city_center', 'urban', or 'highway'
    
    Returns:
        Route with geometry, ETA, and traffic-adjusted duration
    """
    # Get base route from OSRM
    route = await get_osrm_route(start_lat, start_lng, end_lat, end_lng)
    
    # Apply traffic simulation
    base_duration = route["duration"]
    adjusted_duration = apply_traffic_simulation(base_duration, route_type)
    
    # Convert geometry to Leaflet format [[lat, lng], ...]
    leaflet_geometry = [[coord[1], coord[0]] for coord in route["geometry"]]
    
    return {
        "distance_meters": route["distance"],
        "distance_km": round(route["distance"] / 1000, 2),
        "base_duration_seconds": int(base_duration),
        "adjusted_duration_seconds": int(adjusted_duration),
        "eta_minutes": round(adjusted_duration / 60, 1),
        "route_type": route_type,
        "traffic_multiplier": TRAFFIC_MULTIPLIERS.get(route_type, 1.3),
        "geometry": leaflet_geometry,
        "steps": route["steps"]
    }


@router.get("/eta/{start_node}/{end_node}")
async def get_eta(start_node: str, end_node: str) -> Dict[str, Any]:
    """
    Get ETA between two predefined nodes
    
    Args:
        start_node: Starting node name (e.g., 'node1', 'hub')
        end_node: Destination node name
    
    Returns:
        ETA and route information
    """
    # Predefined node coordinates
    NODES = {
        "hub": {"lat": 12.9756, "lng": 77.6066, "name": "MG Road Metro"},
        "node1": {"lat": 12.9719, "lng": 77.6412, "name": "Indiranagar"},
        "node2": {"lat": 12.9352, "lng": 77.6245, "name": "Koramangala"},
        "node3": {"lat": 12.9177, "lng": 77.6233, "name": "Silk Board"}
    }
    
    start = NODES.get(start_node.lower())
    end = NODES.get(end_node.lower())
    
    if not start or not end:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Determine route type based on nodes
    if start_node in ["hub", "node2"]:
        route_type = "city_center"
    elif end_node == "node3":
        route_type = "highway"
    else:
        route_type = "urban"
    
    result = await calculate_route(
        start["lat"], start["lng"],
        end["lat"], end["lng"],
        route_type
    )
    
    result["start_node"] = start["name"]
    result["end_node"] = end["name"]
    
    return result


@router.post("/predict-escape")
async def predict_escape_route(
    detected_node: str,
    possible_exits: List[str]
) -> Dict[str, Any]:
    """
    Predict most likely escape route based on ETAs
    
    Body params:
        detected_node: Node where target was detected
        possible_exits: List of possible exit nodes
    
    Returns:
        Ranked escape routes with ETAs
    """
    routes = []
    
    for exit_node in possible_exits:
        try:
            eta_result = await get_eta(detected_node, exit_node)
            routes.append({
                "exit_node": exit_node,
                "eta_minutes": eta_result["eta_minutes"],
                "distance_km": eta_result["distance_km"],
                "route_type": eta_result["route_type"],
                "geometry": eta_result["geometry"]
            })
        except Exception as e:
            continue
    
    # Sort by ETA (fastest route = most likely)
    routes.sort(key=lambda x: x["eta_minutes"])
    
    return {
        "detected_at": detected_node,
        "analyzed_exits": len(routes),
        "predicted_route": routes[0] if routes else None,
        "all_routes": routes
    }
