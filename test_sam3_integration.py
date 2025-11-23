"""
Test SAM3 Integration
Quick test to verify SAM3 setup is working
"""
import requests
import sys
from pathlib import Path

API_BASE = "http://localhost:8000/api/sam3"

def test_sam3_status():
    """Test SAM3 status endpoint"""
    print("🔍 Checking SAM3 status...")
    response = requests.get(f"{API_BASE}/status")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SAM3 Status:")
        print(f"   - Available: {data['sam3_available']}")
        print(f"   - Initialized: {data['initialized']}")
        print(f"   - Model: {data['model_name']}")
        print(f"   - Device: {data['device']}")
        print(f"   - HF Token Set: {data['hf_token_set']}")
        return data
    else:
        print(f"❌ Status check failed: {response.status_code}")
        return None

def test_sam3_initialize():
    """Test SAM3 initialization"""
    print("\n🚀 Initializing SAM3 model...")
    response = requests.post(f"{API_BASE}/initialize")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data['status']}")
        print(f"   Model: {data['model']}")
        print(f"   Device: {data['device']}")
        return True
    else:
        print(f"❌ Initialization failed: {response.status_code}")
        print(f"   {response.json()}")
        return False

def test_video_upload(video_path: str = None):
    """Test video upload and processing"""
    if not video_path:
        print("\n⏭️  Skipping video upload test (no video provided)")
        return
    
    video_file = Path(video_path)
    if not video_file.exists():
        print(f"❌ Video file not found: {video_path}")
        return
    
    print(f"\n📹 Uploading and processing video: {video_file.name}")
    
    with open(video_file, "rb") as f:
        files = {"video": (video_file.name, f, "video/mp4")}
        data = {
            "node_name": "test_node",
            "max_frames": "50",
            "use_hsv": "true"  # Start with HSV for testing
        }
        
        response = requests.post(
            f"{API_BASE}/process-video",
            files=files,
            data=data,
            timeout=300  # 5 minute timeout
        )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Video processed successfully!")
        print(f"   Node: {result['node_name']}")
        print(f"   Method: {result['method']}")
        print(f"   Frames processed: {result['processed_frames']}")
        print(f"   Detections: {result['detected_frames']}")
        print(f"   Detection rate: {result['detection_rate']:.1%}")
        print(f"   Output: {result['output_path']}")
    else:
        print(f"❌ Processing failed: {response.status_code}")
        print(f"   {response.json()}")

if __name__ == "__main__":
    print("🧪 SAM3 Integration Test Suite\n")
    print("=" * 50)
    
    # Test 1: Check status
    status = test_sam3_status()
    
    if not status:
        print("\n❌ Backend not running or SAM3 endpoint not available")
        print("   Start backend: cd backend && ../.venv/Scripts/python.exe -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Test 2: Initialize (if available)
    if status['sam3_available'] and not status['initialized']:
        test_sam3_initialize()
    
    # Test 3: Process video (if path provided)
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        test_video_upload(video_path)
    else:
        print("\n💡 To test video processing:")
        print(f"   python {__file__} path/to/video.mp4")
    
    print("\n" + "=" * 50)
    print("✅ Tests complete!")
