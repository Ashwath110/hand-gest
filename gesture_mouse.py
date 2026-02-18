"""
Hand Gesture Mouse Control
Uses hand tracking to control mouse cursor and perform clicks
"""
import cv2
import numpy as np
import pyautogui
import time
from hand_tracker import HandDetector
from collections import deque

# Configure PyAutoGUI with SAFETY FEATURES
pyautogui.FAILSAFE = True  # Move mouse to top-left corner for EMERGENCY STOP
pyautogui.PAUSE = 0  # Remove pause between commands for smooth movement


class GestureMouse:
    """
    Hand gesture mouse controller
    """
    
    def __init__(self):
        """Initialize gesture mouse controller"""
        self.detector = HandDetector(max_hands=1, detection_confidence=0.7, tracking_confidence=0.7)
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Camera frame dimensions (will be set when video starts)
        self.frame_width = 640
        self.frame_height = 480
        
        # Smoothing parameters
        self.smoothing = 5  # Reduced from 7 for more responsive movement
        self.prev_x, self.prev_y = 0, 0
        
        # Click detection
        self.pinch_threshold = 40  # Distance threshold for pinch detection
        self.is_pinching = False
        self.pinch_count = 0
        self.last_pinch_time = 0
        self.double_click_time = 0.5  # Time window for double click
        self.click_cooldown = 0.3  # Cooldown between clicks
        
        # Drag detection
        self.is_dragging = False
        self.pinch_start_time = 0
        self.drag_threshold_time = 3.0  # Time to hold pinch before drag starts (3 seconds)
        
        # Movement zone (ignore edges for stability) - OPTIMIZED FOR SENSITIVITY
        self.margin = 150  # Increased for higher sensitivity (smaller zone = more cursor movement)
        
        # Visual feedback
        self.pinch_history = deque(maxlen=10)
        
    def get_distance(self, p1, p2):
        """
        Calculate Euclidean distance between two points
        
        Args:
            p1, p2: Points as (x, y) tuples
            
        Returns:
            Distance between points
        """
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def smooth_coordinates(self, x, y):
        """
        Smooth cursor movement using weighted average
        
        Args:
            x, y: Current coordinates
            
        Returns:
            Smoothed (x, y) coordinates
        """
        smooth_x = self.prev_x + (x - self.prev_x) / self.smoothing
        smooth_y = self.prev_y + (y - self.prev_y) / self.smoothing
        
        self.prev_x, self.prev_y = smooth_x, smooth_y
        
        return int(smooth_x), int(smooth_y)
    
    def map_to_screen(self, x, y):
        """
        Map camera coordinates to screen coordinates
        
        Args:
            x, y: Camera frame coordinates
            
        Returns:
            Screen coordinates (x, y)
        """
        # Define movement zone (excluding margins)
        zone_x1, zone_y1 = self.margin, self.margin
        zone_x2 = self.frame_width - self.margin
        zone_y2 = self.frame_height - self.margin
        
        # Map to screen with inverted Y axis for natural movement
        screen_x = np.interp(x, [zone_x1, zone_x2], [0, self.screen_width])
        screen_y = np.interp(y, [zone_y1, zone_y2], [0, self.screen_height])
        
        return int(screen_x), int(screen_y)
    
    def detect_pinch(self, landmarks):
        """
        Detect pinch gesture (index finger + thumb touching)
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Tuple (is_pinching, distance)
        """
        if len(landmarks) == 0:
            return False, 0
        
        # Get index fingertip (8) and thumb tip (4)
        index_tip = (landmarks[8][1], landmarks[8][2])
        thumb_tip = (landmarks[4][1], landmarks[4][2])
        
        # Calculate distance
        distance = self.get_distance(index_tip, thumb_tip)
        
        # Check if pinching
        is_pinching = distance < self.pinch_threshold
        
        return is_pinching, distance
    
    def handle_click(self):
        """
        Handle click detection and double-click
        """
        current_time = time.time()
        
        # Check if enough time has passed since last click
        if current_time - self.last_pinch_time < self.click_cooldown:
            return
        
        # Check for double click
        if current_time - self.last_pinch_time < self.double_click_time:
            # Double click detected
            pyautogui.doubleClick()
            self.pinch_count = 0
            print("Double Click!")
        else:
            # Single click
            pyautogui.click()
            self.pinch_count = 1
            print("Click!")
        
        self.last_pinch_time = current_time
    
    def start_drag(self):
        """
        Start dragging operation
        """
        if not self.is_dragging:
            pyautogui.mouseDown()
            self.is_dragging = True
            print("Drag Started!")
    
    def stop_drag(self):
        """
        Stop dragging operation
        """
        if self.is_dragging:
            pyautogui.mouseUp()
            self.is_dragging = False
            print("Drag Ended!")
    
    def run(self):
        """
        Main loop for gesture mouse control
        """
        cap = cv2.VideoCapture(0)
        cap.set(3, self.frame_width)
        cap.set(4, self.frame_height)
        
        if not cap.isOpened():
            print("ERROR: Could not open camera!")
            return
        
        print("\n" + "="*60)
        print("  HAND GESTURE MOUSE CONTROL - STARTED")
        print("="*60)
        print("\nGesture Controls:")
        print("  - Move INDEX FINGER to control cursor")
        print("  - PINCH once (Index + Thumb) for LEFT CLICK")
        print("  - DOUBLE PINCH quickly for DOUBLE CLICK") 
        print("  - HOLD PINCH for 3 SECONDS to DRAG files/objects")
        print("\nSafety Features:")
        print("  - Press 'Q' to quit safely")
        print("  - Move mouse to TOP-LEFT corner for EMERGENCY STOP")
        print("  - Your regular mouse works normally alongside gestures")
        print("="*60 + "\n")
        
        prev_time = 0
        
        try:
            while True:
                success, img = cap.read()
                if not success:
                    print("Warning: Failed to read frame from camera")
                    break
                
                # Flip image for mirror effect
                img = cv2.flip(img, 1)
                
                # Update frame dimensions
                self.frame_height, self.frame_width = img.shape[:2]
                
                # Find hands
                img = self.detector.find_hands(img, draw=True)
                landmarks = self.detector.find_position(img, draw=False)
                
                # Get hand info
                hand_info = self.detector.get_hand_info()
                
                if hand_info['detected'] and len(landmarks) > 0:
                    # Get index fingertip position (landmark 8)
                    index_tip = landmarks[8]
                    index_x, index_y = index_tip[1], index_tip[2]
                    
                    # Draw circle on index fingertip
                    cv2.circle(img, (index_x, index_y), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "INDEX", (index_x + 20, index_y), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Check for pinch gesture
                    is_pinching, pinch_distance = self.detect_pinch(landmarks)
                    
                    # Store pinch state
                    self.pinch_history.append(is_pinching)
                    
                    # Get current time for drag detection
                    current_time = time.time()
                    
                    # Handle pinch detection with drag support
                    if is_pinching and not self.is_pinching:
                        # Pinch just started
                        self.is_pinching = True
                        self.pinch_start_time = current_time
                    elif is_pinching and self.is_pinching:
                        # Pinch is being held
                        pinch_duration = current_time - self.pinch_start_time
                        
                        if pinch_duration >= self.drag_threshold_time and not self.is_dragging:
                            # Start dragging after threshold time
                            self.start_drag()
                    elif not is_pinching and self.is_pinching:
                        # Pinch ended
                        pinch_duration = current_time - self.pinch_start_time
                        
                        if self.is_dragging:
                            # End drag if we were dragging
                            self.stop_drag()
                        else:
                            # Any pinch release (not during drag) = click
                            self.handle_click()
                        
                        self.is_pinching = False
                    
                    # Move mouse cursor
                    # Map coordinates to screen
                    screen_x, screen_y = self.map_to_screen(index_x, index_y)
                    
                    # Smooth movement
                    smooth_x, smooth_y = self.smooth_coordinates(screen_x, screen_y)
                    
                    # Move cursor (works for both normal movement and dragging)
                    try:
                        pyautogui.moveTo(smooth_x, smooth_y)
                    except pyautogui.FailSafeException:
                        print("\n[EMERGENCY STOP] Mouse moved to corner - Exiting safely...")
                        if self.is_dragging:
                            self.stop_drag()
                        break
                    
                    # Visual feedback
                    # Draw thumb tip
                    thumb_tip = landmarks[4]
                    cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 15, (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, "THUMB", (thumb_tip[1] + 20, thumb_tip[2]), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
                    # Draw line between thumb and index
                    line_color = (0, 255, 255) if is_pinching else (255, 0, 0)
                    cv2.line(img, (index_x, index_y), (thumb_tip[1], thumb_tip[2]), 
                            line_color, 3)
                    
                    # Display pinch distance
                    mid_x = (index_x + thumb_tip[1]) // 2
                    mid_y = (index_y + thumb_tip[2]) // 2
                    cv2.putText(img, f"{int(pinch_distance)}px", (mid_x, mid_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    # Pinch indicator with timer
                    if self.is_dragging:
                        cv2.putText(img, "DRAGGING!", (50, 100),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)
                        cv2.circle(img, (50, 150), 20, (255, 0, 255), cv2.FILLED)
                    elif is_pinching:
                        pinch_duration = current_time - self.pinch_start_time
                        remaining = max(0, self.drag_threshold_time - pinch_duration)
                        cv2.putText(img, f"PINCH: {remaining:.1f}s", (50, 100),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 165, 255), 3)
                        cv2.circle(img, (50, 150), 20, (0, 165, 255), cv2.FILLED)
                        # Progress bar for drag threshold
                        progress = min(1.0, pinch_duration / self.drag_threshold_time)
                        bar_width = int(300 * progress)
                        cv2.rectangle(img, (50, 170), (350, 190), (100, 100, 100), -1)
                        cv2.rectangle(img, (50, 170), (50 + bar_width, 190), (0, 255, 0), -1)
                
                # Draw movement zone with instructions
                cv2.rectangle(img, (self.margin, self.margin), 
                             (self.frame_width - self.margin, self.frame_height - self.margin),
                             (255, 255, 0), 2)
                cv2.putText(img, "Active Zone", (self.margin + 10, self.margin + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                
                # Calculate FPS
                current_time = time.time()
                fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
                prev_time = current_time
                
                # Display info panel
                cv2.putText(img, f"FPS: {int(fps)}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(img, f"Tracking: {'ON' if hand_info['detected'] else 'OFF'}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                           (0, 255, 0) if hand_info['detected'] else (0, 0, 255), 2)
                cv2.putText(img, f"Screen: {self.screen_width}x{self.screen_height}", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Instructions at bottom
                cv2.putText(img, "Green = Index | Blue = Thumb | Yellow = High Sensitivity Zone", 
                           (10, self.frame_height - 70), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 255, 255), 1)
                cv2.putText(img, "Quick Pinch = Click | Double Pinch = Double Click", 
                           (10, self.frame_height - 45), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 255, 255), 1)
                cv2.putText(img, "Pinch = Click | Hold 3 sec = DRAG | Q to Quit", 
                           (10, self.frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 255, 255), 1)
                
                # Show image
                cv2.imshow("Hand Gesture Mouse Control", img)
                
                # Exit on 'Q' key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("\n[SAFE EXIT] Quitting gesture control...")
                    break
        
        except KeyboardInterrupt:
            print("\n[KEYBOARD INTERRUPT] Exiting safely...")
        except Exception as e:
            print(f"\n[ERROR] {str(e)}")
            print("Exiting safely...")
        finally:
            # Ensure drag is stopped if active
            if self.is_dragging:
                self.stop_drag()
            cap.release()
            cv2.destroyAllWindows()
            print("\n" + "="*60)
            print("  Hand Gesture Mouse Control STOPPED")
            print("  Your regular mouse is now the only active input")
            print("="*60 + "\n")


def main():
    """Main function"""
    try:
        controller = GestureMouse()
        controller.run()
    except Exception as e:
        print(f"Failed to start: {e}")
        print("Make sure your camera is available and not in use by another application.")


if __name__ == "__main__":
    main()
