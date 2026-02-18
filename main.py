"""
Hand Gesture Tracking Application
Real-time hand tracking with finger detection using camera feed
Uses pre-trained MediaPipe models for robust tracking
"""
import cv2
import time
import numpy as np
from hand_tracker import HandDetector


class HandTrackingApp:
    """
    Main application for hand gesture tracking
    """
    
    def __init__(self):
        """Initialize the application"""
        self.cap = None
        self.detector = HandDetector(max_hands=2, detection_confidence=0.7, tracking_confidence=0.7)
        self.trail_points = []  # Store trail points for movement visualization
        self.max_trail_length = 30
        self.tracking_active = False
        self.locked_hand_id = None
        
    def start_camera(self, camera_id=0):
        """
        Start the camera feed
        
        Args:
            camera_id: Camera device ID (0 for default camera)
        """
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(3, 1280)  # Width
        self.cap.set(4, 720)   # Height
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {camera_id}")
            return False
        
        print(f"Camera {camera_id} opened successfully")
        return True
    
    def draw_trail(self, img, center):
        """
        Draw movement trail
        
        Args:
            img: Image to draw on
            center: Current hand center position
        """
        if center:
            self.trail_points.append(center)
            
            # Limit trail length
            if len(self.trail_points) > self.max_trail_length:
                self.trail_points.pop(0)
            
            # Draw trail with fading effect
            for i in range(1, len(self.trail_points)):
                if self.trail_points[i - 1] is None or self.trail_points[i] is None:
                    continue
                
                # Calculate thickness and color based on position in trail
                thickness = int(np.sqrt(self.max_trail_length / float(i + 1)) * 3)
                alpha = i / len(self.trail_points)
                color = (int(255 * alpha), int(100 * alpha), int(255 * (1 - alpha)))
                
                cv2.line(img, self.trail_points[i - 1], self.trail_points[i], color, thickness)
    
    def draw_info(self, img, fps, hand_info):
        """
        Draw information overlay on the image
        
        Args:
            img: Image to draw on
            fps: Current FPS
            hand_info: Hand detection information
        """
        # Draw FPS
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw hand detection status
        status = "Hand Detected" if hand_info['detected'] else "No Hand Detected"
        color = (0, 255, 0) if hand_info['detected'] else (0, 0, 255)
        cv2.putText(img, status, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Draw finger count
        if hand_info['detected']:
            fingers = hand_info['fingers_up']
            finger_count = fingers.count(1)
            cv2.putText(img, f'Fingers Up: {finger_count}', (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Draw tracking status
            tracking_text = "Tracking: LOCKED" if self.tracking_active else "Tracking: SEARCHING"
            tracking_color = (0, 255, 255) if self.tracking_active else (255, 165, 0)
            cv2.putText(img, tracking_text, (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, tracking_color, 2)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "Q - Quit",
            "T - Toggle Tracking Lock",
            "C - Clear Trail",
            "R - Reset"
        ]
        
        y_offset = img.shape[0] - 150
        for i, instruction in enumerate(instructions):
            cv2.putText(img, instruction, (10, y_offset + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_hand_bbox(self, img, landmarks):
        """
        Draw bounding box around detected hand
        
        Args:
            img: Image to draw on
            landmarks: List of hand landmarks
        """
        if len(landmarks) > 0:
            x_coords = [lm[1] for lm in landmarks]
            y_coords = [lm[2] for lm in landmarks]
            
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            # Add padding
            padding = 20
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(img.shape[1], x_max + padding)
            y_max = min(img.shape[0], y_max + padding)
            
            # Draw bounding box
            color = (0, 255, 255) if self.tracking_active else (255, 0, 0)
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
            
            # Draw "LOCKED" text if tracking
            if self.tracking_active:
                cv2.putText(img, "LOCKED", (x_min, y_min - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    def run(self):
        """
        Main application loop
        """
        if not self.start_camera():
            return
        
        print("\n=== Hand Gesture Tracking Started ===")
        print("Controls:")
        print("  Q - Quit application")
        print("  T - Toggle tracking lock on/off")
        print("  C - Clear movement trail")
        print("  R - Reset tracking")
        print("=====================================\n")
        
        prev_time = 0
        
        try:
            while True:
                success, img = self.cap.read()
                
                if not success:
                    print("Error: Failed to read frame from camera")
                    break
                
                # Flip image for mirror effect
                img = cv2.flip(img, 1)
                
                # Find hands in the frame
                img = self.detector.find_hands(img, draw=True)
                landmarks = self.detector.find_position(img, draw=True)
                hand_info = self.detector.get_hand_info()
                
                # Auto-lock tracking when hand is detected
                if hand_info['detected'] and not self.tracking_active:
                    self.tracking_active = True
                    print("Hand detected - Tracking locked!")
                
                # Draw bounding box around hand
                if hand_info['detected']:
                    self.draw_hand_bbox(img, landmarks)
                
                # Draw movement trail from hand center
                center = hand_info['center']
                if center and self.tracking_active:
                    self.draw_trail(img, center)
                    # Draw center point
                    cv2.circle(img, center, 10, (0, 255, 255), cv2.FILLED)
                
                # Calculate FPS
                current_time = time.time()
                fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
                prev_time = current_time
                
                # Draw information overlay
                self.draw_info(img, fps, hand_info)
                
                # Display the image
                cv2.imshow("Hand Gesture Tracking", img)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("Quitting application...")
                    break
                elif key == ord('t') or key == ord('T'):
                    self.tracking_active = not self.tracking_active
                    status = "enabled" if self.tracking_active else "disabled"
                    print(f"Tracking lock {status}")
                    if not self.tracking_active:
                        self.trail_points.clear()
                elif key == ord('c') or key == ord('C'):
                    self.trail_points.clear()
                    print("Trail cleared")
                elif key == ord('r') or key == ord('R'):
                    self.trail_points.clear()
                    self.tracking_active = False
                    print("Tracking reset")
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed successfully")


def main():
    """Entry point"""
    app = HandTrackingApp()
    app.run()


if __name__ == "__main__":
    main()
