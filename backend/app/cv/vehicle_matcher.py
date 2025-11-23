"""
Vehicle matching using feature extraction and comparison
Compares uploaded reference vehicle with camera feed detections
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json


class VehicleMatcher:
    """
    Match vehicles using color histograms, ORB features, and template matching
    """
    
    def __init__(self):
        self.reference_vehicle = None
        self.reference_features = None
        self.reference_histogram = None
        self.orb = cv2.ORB_create(nfeatures=500)
        self.bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
    def set_reference_vehicle(self, image_path: str) -> bool:
        """
        Load and extract features from reference vehicle image
        
        Args:
            image_path: Path to reference vehicle image
            
        Returns:
            True if successful
        """
        try:
            # Load reference image
            img = cv2.imread(str(image_path))
            if img is None:
                print(f"Failed to load reference image: {image_path}")
                return False
            
            self.reference_vehicle = img
            
            # Extract ORB features
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.reference_features = self.orb.detectAndCompute(gray, None)
            
            # Extract color histogram
            self.reference_histogram = self._extract_color_histogram(img)
            
            print(f"Reference vehicle loaded: {Path(image_path).name}")
            print(f"  Features detected: {len(self.reference_features[0]) if self.reference_features[0] else 0}")
            
            return True
            
        except Exception as e:
            print(f"Error loading reference vehicle: {e}")
            return False
    
    def _extract_color_histogram(self, img: np.ndarray, bins: int = 32) -> np.ndarray:
        """
        Extract color histogram from image
        
        Args:
            img: Input image (BGR)
            bins: Number of histogram bins per channel
            
        Returns:
            Normalized histogram
        """
        # Convert to HSV for better color representation
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Calculate histogram for each channel
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [bins, bins, bins], 
                           [0, 180, 0, 256, 0, 256])
        
        # Normalize
        hist = cv2.normalize(hist, hist).flatten()
        
        return hist
    
    def _extract_features(self, img: np.ndarray) -> Tuple[Optional[tuple], np.ndarray]:
        """
        Extract ORB features and color histogram from image
        
        Args:
            img: Input image (BGR)
            
        Returns:
            (ORB features, color histogram)
        """
        # ORB features
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        orb_features = self.orb.detectAndCompute(gray, None)
        
        # Color histogram
        histogram = self._extract_color_histogram(img)
        
        return orb_features, histogram
    
    def match_vehicle(self, candidate_image: np.ndarray, threshold: float = 0.25) -> Dict:
        """
        Match candidate vehicle against reference
        
        Args:
            candidate_image: Candidate vehicle image (BGR)
            threshold: Matching threshold (0.0 to 1.0) - VERY LOW for demo (0.25 = 25% match)
            
        Returns:
            Matching result with score and match status
        """
        if self.reference_vehicle is None:
            return {
                "matched": False,
                "score": 0.0,
                "reason": "No reference vehicle set"
            }
        
        try:
            # Extract features from candidate
            candidate_features, candidate_hist = self._extract_features(candidate_image)
            
            # 1. Color histogram comparison (fast check)
            hist_score = cv2.compareHist(
                self.reference_histogram, 
                candidate_hist, 
                cv2.HISTCMP_CORREL
            )
            
            # Boost low scores for better detection
            # If histogram shows any correlation (>0), give it a boost
            if hist_score > 0:
                hist_score = hist_score * 1.2  # 20% boost
                if hist_score > 1.0:
                    hist_score = 1.0
            
            # 2. ORB feature matching
            feature_score = 0.0
            if (self.reference_features[1] is not None and 
                candidate_features[1] is not None and
                len(self.reference_features[1]) > 0 and 
                len(candidate_features[1]) > 0):
                
                try:
                    # Match features
                    matches = self.bf_matcher.match(
                        self.reference_features[1], 
                        candidate_features[1]
                    )
                    
                    # More lenient matching - accept more matches
                    good_matches = [m for m in matches if m.distance < 80]  # Increased from 50
                    
                    # Calculate feature score
                    if len(matches) > 0:
                        feature_score = len(good_matches) / len(matches)
                except:
                    feature_score = 0.0
            
            # Combined score (weighted average)
            # Color histogram: 80% weight (most reliable)
            # Features: 20% weight
            combined_score = (hist_score * 0.8) + (feature_score * 0.2)
            
            # Determine match - using VERY LOW threshold for demo
            matched = combined_score >= threshold
            
            return {
                "matched": matched,
                "score": float(combined_score),
                "histogram_score": float(hist_score),
                "feature_score": float(feature_score),
                "threshold": threshold,
                "reason": "Match found" if matched else f"No match - score {combined_score:.2f} below threshold {threshold}"
            }
            
        except Exception as e:
            return {
                "matched": False,
                "score": 0.0,
                "reason": f"Error during matching: {str(e)}"
            }
    
    def match_video_frames(self, video_path: str, max_frames: int = 100) -> Dict:
        """
        Process video and find matching vehicles
        
        Args:
            video_path: Path to video file
            max_frames: Maximum frames to process
            
        Returns:
            Detection results with match statistics
        """
        if self.reference_vehicle is None:
            return {
                "matched": False,
                "total_frames": 0,
                "matched_frames": 0,
                "match_rate": 0.0,
                "reason": "No reference vehicle set"
            }
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            total_frames = 0
            matched_frames = 0
            best_score = 0.0
            
            while cap.isOpened() and total_frames < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                total_frames += 1
                
                # Process every 3rd frame for better detection
                if total_frames % 3 != 0:
                    continue
                
                # Try to match the whole frame first (simpler approach)
                match_result = self.match_vehicle(frame, threshold=0.25)
                
                if match_result["matched"]:
                    matched_frames += 1
                    best_score = max(best_score, match_result["score"])
                    continue
                
                # Detect vehicles using HSV - detect multiple colors
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Red color detection
                lower_red1 = np.array([0, 50, 50])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([160, 50, 50])
                upper_red2 = np.array([180, 255, 255])
                
                mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                mask_red = cv2.bitwise_or(mask_red1, mask_red2)
                
                # Blue color detection
                lower_blue = np.array([100, 50, 50])
                upper_blue = np.array([130, 255, 255])
                mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
                
                # White color detection
                lower_white = np.array([0, 0, 150])
                upper_white = np.array([180, 50, 255])
                mask_white = cv2.inRange(hsv, lower_white, upper_white)
                
                # Black color detection
                lower_black = np.array([0, 0, 0])
                upper_black = np.array([180, 255, 50])
                mask_black = cv2.inRange(hsv, lower_black, upper_black)
                
                # Combine all masks
                mask = cv2.bitwise_or(mask_red, mask_blue)
                mask = cv2.bitwise_or(mask, mask_white)
                mask = cv2.bitwise_or(mask, mask_black)
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Process each detected vehicle
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area < 500:  # Lowered threshold for smaller detections
                        continue
                    
                    # Get bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Skip if too small
                    if w < 20 or h < 20:
                        continue
                    
                    # Extract vehicle region
                    vehicle_roi = frame[y:y+h, x:x+w]
                    
                    # Match against reference with VERY LOW threshold for demo
                    match_result = self.match_vehicle(vehicle_roi, threshold=0.25)
                    
                    if match_result["matched"]:
                        matched_frames += 1
                        best_score = max(best_score, match_result["score"])
                        break  # Found a match in this frame
            
            cap.release()
            
            match_rate = (matched_frames / total_frames * 100) if total_frames > 0 else 0
            
            return {
                "matched": matched_frames > 0,
                "total_frames": total_frames,
                "matched_frames": matched_frames,
                "match_rate": round(match_rate, 2),
                "best_score": round(best_score, 2),
                "reason": f"Vehicle matched in {matched_frames} frames" if matched_frames > 0 
                         else "Reference vehicle not found in video"
            }
            
        except Exception as e:
            return {
                "matched": False,
                "total_frames": 0,
                "matched_frames": 0,
                "match_rate": 0.0,
                "reason": f"Error processing video: {str(e)}"
            }


# Global vehicle matcher instance
vehicle_matcher = VehicleMatcher()
