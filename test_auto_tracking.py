"""
Test script for automatic vehicle tracking system
Demonstrates the complete loop: Detection → Prediction → Check → Handover
"""

import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_auto_tracking():
    """Test the automatic tracking loop"""
    
    print_section("🚨 AUTOMATIC VEHICLE TRACKING TEST")
    
    # Vehicle details (theft scenario)
    vehicle = {
        "color": "white",
        "model": "SUV",
        "license_plate": "KA01AB1234",
        "distinctive_features": ["dent on left door", "roof rack"]
    }
    
    # Start point (theft location)
    start_camera = "hub_mgroad"
    
    print(f"\n🎯 Starting Point: {start_camera}")
    print(f"🚗 Vehicle: {vehicle['color']} {vehicle['model']}")
    print(f"🔍 Features: {', '.join(vehicle['distinctive_features'])}")
    
    # Call auto-tracking API
    print("\n⏳ Starting automatic tracking loop...")
    
    try:
        response = requests.post(
            f"{API_BASE}/track/auto",
            json={
                "camera_id": start_camera,
                "vehicle": vehicle
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result["success"]:
                data = result["data"]
                
                print_section("✅ TRACKING COMPLETED")
                
                print(f"\n📊 Summary:")
                print(f"   Tracking ID: {data['tracking_id']}")
                print(f"   Status: {data['status']}")
                print(f"   Total Hops: {data['total_hops']}")
                print(f"   Distance Covered: {data['total_distance_km']} km")
                print(f"   Duration: {data['duration_minutes']:.2f} minutes")
                print(f"   Cameras Checked: {data['final_status']['total_cameras_checked']}")
                
                print_section("🗺️  TRACKING CHAIN (Where Vehicle Was Found)")
                
                for i, detection in enumerate(data['tracking_chain']):
                    status_icon = "✅" if detection['status'] == "detected" else "❌"
                    print(f"\n{status_icon} Hop {i + 1}: {detection['camera_name']}")
                    print(f"   Camera ID: {detection['camera_id']}")
                    print(f"   Location: ({detection['lat']}, {detection['lng']})")
                    print(f"   Time: {detection['detection_time']}")
                    print(f"   Status: {detection['status']}")
                
                print_section("🔍 ALL PREDICTIONS (Cameras That Were Checked)")
                
                for hop in data['all_predictions']:
                    print(f"\n📍 From: {hop['from_camera_name']}")
                    print(f"   Checking {len(hop['cameras_to_check'])} possible cameras:")
                    
                    for cam in hop['cameras_to_check']:
                        prob_bar = "█" * int(cam['probability'] * 20)
                        print(f"   • {cam['camera_name']}")
                        print(f"     ETA: {cam['eta_minutes']} min | Probability: {cam['probability']*100:.0f}% {prob_bar}")
                
                print_section("🏁 FINAL STATUS")
                
                final = data['final_status']
                print(f"\n   Last Seen: {final['last_seen_name']}")
                print(f"   Camera ID: {final['last_seen_camera']}")
                print(f"   Reason: {final['reason']}")
                
                # Get visualization data
                print_section("🎨 GETTING VISUALIZATION DATA")
                
                viz_response = requests.get(
                    f"{API_BASE}/track/visualize/{data['tracking_id']}"
                )
                
                if viz_response.status_code == 200:
                    viz_data = viz_response.json()['data']
                    
                    print(f"\n   Animation Steps: {len(viz_data.get('animation_sequence', []))}")
                    print(f"   Prediction Paths: {len(viz_data.get('prediction_paths', []))}")
                    print(f"   Camera Checks: {len(viz_data.get('all_camera_checks', []))}")
                    
                    print("\n   ✅ Visualization data ready for frontend!")
                
                print_section("✅ TEST COMPLETED SUCCESSFULLY")
                return True
                
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        return False

def test_manual_tracking():
    """Test manual tracking (step by step)"""
    
    print_section("🎯 MANUAL TRACKING TEST (Step by Step)")
    
    vehicle = {
        "color": "white",
        "model": "SUV",
        "distinctive_features": ["dent on left door"]
    }
    
    try:
        # Start tracking
        response = requests.post(
            f"{API_BASE}/track/start",
            json={
                "camera_id": "hub_mgroad",
                "vehicle": vehicle
            }
        )
        
        if response.status_code == 200:
            data = response.json()['data']
            tracking_id = data['tracking_id']
            
            print(f"\n✅ Tracking started: {tracking_id}")
            print(f"   Initial detection: {data['initial_detection']['camera_name']}")
            print(f"   Predictions: {len(data['predictions'])}")
            
            for pred in data['predictions']:
                print(f"   • {pred['camera_name']} - ETA: {pred['eta_minutes']} min ({pred['probability']*100:.0f}%)")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_network_info():
    """Test network information endpoints"""
    
    print_section("🌐 NETWORK INFORMATION")
    
    try:
        # Get all cameras
        response = requests.get(f"{API_BASE}/network/cameras")
        
        if response.status_code == 200:
            cameras = response.json()['data']
            
            print(f"\n📹 Total Cameras: {len(cameras)}")
            
            for cam in cameras:
                print(f"\n   {cam['name']}")
                print(f"   ID: {cam['id']}")
                print(f"   Type: {cam['type']}")
                print(f"   Location: ({cam['lat']}, {cam['lng']})")
                print(f"   Connections: {cam['connections_count']}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                 OPERATION GRIDLOCK - AUTO TRACKING TEST            ║
║              Geospatial Vehicle Tracking System - FOSS             ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Run tests
    print("\n🔧 Testing backend connectivity...")
    
    try:
        response = requests.get(f"{API_BASE}/../status")
        if response.status_code == 200:
            print("✅ Backend is online!")
        else:
            print("❌ Backend not responding properly")
            exit(1)
    except:
        print("❌ Cannot connect to backend. Is it running on http://127.0.0.1:8000?")
        exit(1)
    
    # Run tests
    test_network_info()
    test_manual_tracking()
    test_auto_tracking()
    
    print("\n" + "="*70)
    print("  🎉 ALL TESTS COMPLETED")
    print("="*70)
    print("\nNext steps:")
    print("1. Open frontend: http://localhost:3000")
    print("2. Click 'Start Demo' to see automatic tracking in action")
    print("3. Watch the map animate camera checks and detections")
    print("\n")
