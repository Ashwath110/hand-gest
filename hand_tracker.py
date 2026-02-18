"""
Hand Tracking Module
Uses MediaPipe's pre-trained models for hand detection and tracking
"""
import cv2
import mediapipe as mp
import time


class HandDetector:
    """
    Hand detector class that uses MediaPipe for real-time hand tracking
    """
    
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        """
        Initialize hand detector with MediaPipe
        
        Args:
            mode: Static image mode (False for video)
            max_hands: Maximum number of hands to detect
            detection_confidence: Minimum detection confidence threshold
            tracking_confidence: Minimum tracking confidence threshold
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initialize MediaPipe hands module (pre-trained model)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Hand landmark indices
        self.finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        self.finger_pips = [2, 6, 10, 14, 18]  # PIP joints for finger detection
        
    def find_hands(self, img, draw=True):
        """
        Find hands in the image
        
        Args:
            img: Input image (BGR format)
            draw: Whether to draw hand landmarks on image
            
        Returns:
            Image with drawings (if draw=True)
        """
        # Convert BGR to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        # Draw hand landmarks if hands detected
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    # Draw landmarks with connections
                    self.mp_draw.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
        
        return img
    
    def find_position(self, img, hand_no=0, draw=True):
        """
        Find positions of hand landmarks
        
        Args:
            img: Input image
            hand_no: Which hand to track (0 for first hand detected)
            draw: Whether to draw circles on fingertips
            
        Returns:
            List of landmark positions [id, x, y]
        """
        self.landmark_list = []
        
        if self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[hand_no]
                
                # Get image dimensions
                h, w, c = img.shape
                
                # Extract each landmark position
                for id, landmark in enumerate(hand.landmark):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    self.landmark_list.append([id, cx, cy])
                    
                    # Draw circles on fingertips
                    if draw and id in self.finger_tips:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        
        return self.landmark_list
    
    def fingers_up(self):
        """
        Check which fingers are up
        
        Returns:
            List of 5 values (0 or 1) for each finger [Thumb, Index, Middle, Ring, Pinky]
        """
        fingers = []
        
        if len(self.landmark_list) != 0:
            # Thumb (special case - check horizontal position)
            if self.landmark_list[self.finger_tips[0]][1] > self.landmark_list[self.finger_tips[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other 4 fingers (check vertical position)
            for id in range(1, 5):
                if self.landmark_list[self.finger_tips[id]][2] < self.landmark_list[self.finger_pips[id]][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        return fingers
    
    def get_hand_center(self):
        """
        Get the center point of the hand (wrist + middle finger MCP average)
        
        Returns:
            Tuple (x, y) of hand center or None if no hand detected
        """
        if len(self.landmark_list) != 0:
            wrist = self.landmark_list[0]
            middle_mcp = self.landmark_list[9]
            center_x = (wrist[1] + middle_mcp[1]) // 2
            center_y = (wrist[2] + middle_mcp[2]) // 2
            return (center_x, center_y)
        return None
    
    def get_hand_info(self):
        """
        Get comprehensive hand information
        
        Returns:
            Dictionary with hand tracking data
        """
        info = {
            'detected': len(self.landmark_list) > 0,
            'landmarks': self.landmark_list,
            'fingers_up': self.fingers_up() if len(self.landmark_list) > 0 else [],
            'center': self.get_hand_center(),
            'fingertips': []
        }
        
        # Extract fingertip positions
        if len(self.landmark_list) > 0:
            for tip_id in self.finger_tips:
                info['fingertips'].append({
                    'id': tip_id,
                    'position': (self.landmark_list[tip_id][1], self.landmark_list[tip_id][2])
                })
        
        return info
