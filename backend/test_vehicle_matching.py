"""
Test vehicle matching functionality
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.cv.vehicle_matcher import vehicle_matcher

def test_vehicle_matcher():
    """Test basic vehicle matching functionality"""
    
    print("=" * 60)
    print("VEHICLE MATCHING TEST")
    print("=" * 60)
    
    # Test 1: Check matcher initialization
    print("\n1. Testing matcher initialization...")
    print(f"   Reference vehicle set: {vehicle_matcher.reference_vehicle is not None}")
    print(f"   ORB detector created: {vehicle_matcher.orb is not None}")
    
    # Test 2: Check if sample vehicle images exist
    print("\n2. Checking for sample vehicle images...")
    uploads_path = Path(__file__).parent / "assets" / "vehicle_uploads"
    
    if uploads_path.exists():
        image_files = list(uploads_path.glob("*.jpg")) + list(uploads_path.glob("*.png"))
        print(f"   Found {len(image_files)} vehicle images")
        
        if image_files:
            # Try loading first image as reference
            print(f"\n3. Testing reference vehicle loading...")
            test_image = image_files[0]
            print(f"   Loading: {test_image.name}")
            
            success = vehicle_matcher.set_reference_vehicle(str(test_image))
            print(f"   Success: {success}")
            
            if success:
                print(f"   Features detected: {len(vehicle_matcher.reference_features[0]) if vehicle_matcher.reference_features[0] else 0}")
                print(f"   Histogram shape: {vehicle_matcher.reference_histogram.shape}")
    else:
        print(f"   Upload directory not found: {uploads_path}")
    
    # Test 3: Check video directory
    print("\n4. Checking for video files...")
    videos_path = Path(__file__).parent / "assets" / "videos"
    
    if videos_path.exists():
        video_files = list(videos_path.glob("*.mp4")) + list(videos_path.glob("*.avi"))
        print(f"   Found {len(video_files)} video files")
        
        if video_files and vehicle_matcher.reference_vehicle is not None:
            print(f"\n5. Testing video matching...")
            test_video = video_files[0]
            print(f"   Processing: {test_video.name}")
            
            result = vehicle_matcher.match_video_frames(str(test_video), max_frames=20)
            print(f"\n   Results:")
            print(f"   - Matched: {result['matched']}")
            print(f"   - Total frames: {result['total_frames']}")
            print(f"   - Matched frames: {result['matched_frames']}")
            print(f"   - Match rate: {result['match_rate']}%")
            print(f"   - Reason: {result['reason']}")
    else:
        print(f"   Video directory not found: {videos_path}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_vehicle_matcher()
