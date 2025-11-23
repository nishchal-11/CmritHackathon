"""
Simple test to verify vehicle matching is working
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.cv.vehicle_matcher import vehicle_matcher
import cv2
import numpy as np

def test_simple_matching():
    """Test basic matching functionality"""
    
    print("=" * 60)
    print("SIMPLE VEHICLE MATCHING TEST")
    print("=" * 60)
    
    # Check for uploaded vehicles
    uploads_path = Path(__file__).parent / "assets" / "vehicle_uploads"
    
    if not uploads_path.exists():
        print(f"❌ Upload directory not found: {uploads_path}")
        return
    
    # Find image files
    image_files = list(uploads_path.glob("*.jpg")) + list(uploads_path.glob("*.png")) + list(uploads_path.glob("*.jpeg"))
    
    if not image_files:
        print("❌ No vehicle images found in uploads")
        print(f"   Please upload a vehicle image first")
        return
    
    # Use the most recent image
    reference_image = sorted(image_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
    print(f"\n✅ Found reference image: {reference_image.name}")
    
    # Load reference vehicle
    print(f"\n🔄 Loading reference vehicle...")
    success = vehicle_matcher.set_reference_vehicle(str(reference_image))
    
    if not success:
        print("❌ Failed to load reference vehicle")
        return
    
    print(f"✅ Reference vehicle loaded successfully")
    
    # Test matching against itself (should score high)
    print(f"\n🔍 Testing self-match (should score high)...")
    img = cv2.imread(str(reference_image))
    result = vehicle_matcher.match_vehicle(img, threshold=0.4)
    
    print(f"\n   Match Result:")
    print(f"   - Matched: {result['matched']}")
    print(f"   - Score: {result['score']:.3f}")
    print(f"   - Histogram Score: {result['histogram_score']:.3f}")
    print(f"   - Feature Score: {result['feature_score']:.3f}")
    print(f"   - Threshold: {result['threshold']}")
    
    # Check for video files
    videos_path = Path(__file__).parent / "assets" / "videos"
    
    if videos_path.exists():
        video_files = list(videos_path.glob("*.mp4")) + list(videos_path.glob("*.avi"))
        
        if video_files:
            test_video = sorted(video_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
            print(f"\n✅ Found video: {test_video.name}")
            
            print(f"\n🎬 Testing video matching (processing 30 frames)...")
            video_result = vehicle_matcher.match_video_frames(str(test_video), max_frames=30)
            
            print(f"\n   Video Results:")
            print(f"   - Matched: {video_result['matched']}")
            print(f"   - Total Frames: {video_result['total_frames']}")
            print(f"   - Matched Frames: {video_result['matched_frames']}")
            print(f"   - Match Rate: {video_result['match_rate']}%")
            print(f"   - Best Score: {video_result.get('best_score', 0)}")
            print(f"   - Message: {video_result['reason']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    # Recommendations
    print("\n📋 RECOMMENDATIONS:")
    if result['score'] >= 0.7:
        print("   ✅ Matching is working well! Score > 0.7")
    elif result['score'] >= 0.4:
        print("   ⚠️  Matching is working but with lower confidence")
        print("      Consider adjusting threshold to 0.4 for better detection")
    else:
        print("   ❌ Matching needs improvement")
        print("      Possible issues:")
        print("      - Image quality too low")
        print("      - Feature detection failed")
        print("      - OpenCV not configured correctly")

if __name__ == "__main__":
    test_simple_matching()
