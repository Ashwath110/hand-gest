# Hand Gesture Tracking Project

Real-time hand tracking and finger detection system using computer vision and pre-trained machine learning models.

## Features

- **Real-time Hand Detection**: Detects hands using MediaPipe's pre-trained models
- **Finger Tip Tracking**: Identifies and tracks all 5 fingertips
- **Movement Tracking**: Visualizes hand movement with a colorful trail
- **Lock-on Tracking**: Automatically locks onto detected hands for continuous tracking
- **Multi-hand Support**: Can track up to 2 hands simultaneously
- **Live Camera Feed**: Uses your webcam for real-time tracking

## Technology Stack

- **OpenCV**: Computer vision and camera handling
- **MediaPipe**: Pre-trained hand detection and tracking models (Google's ML solution)
- **NumPy**: Numerical computations
- **Python 3.7+**: Programming language

## Installation

### Prerequisites
- Python 3.7 or higher
- Webcam/Camera

### Setup Steps

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application**:
```bash
python main.py
```

## Usage

### Controls
- **Q**: Quit the application
- **T**: Toggle tracking lock on/off
- **C**: Clear movement trail
- **R**: Reset tracking

### Features Explained

#### Hand Detection
The application automatically detects hands in the camera frame using MediaPipe's pre-trained models. No additional training required!

#### Finger Tracking
- Identifies all 5 fingertips (Thumb, Index, Middle, Ring, Pinky)
- Shows which fingers are extended
- Draws purple circles on fingertips

#### Movement Trail
- Visualizes hand movement with a colorful fading trail
- Trail follows the center of your hand
- Helps visualize gesture patterns

#### Lock-on Tracking
- Automatically locks onto detected hands
- Keeps tracking even with fast movements
- Shows bounding box around tracked hand

## Project Structure

```
Hand gestures/
│
├── main.py              # Main application entry point
├── hand_tracker.py      # Hand detection and tracking module
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## How It Works

### MediaPipe Hand Tracking
This project uses **MediaPipe Hands**, a pre-trained machine learning model that:
- Detects 21 hand landmarks (knuckles, fingertips, wrist, etc.)
- Works in real-time on standard hardware
- Trained on diverse datasets for robust detection
- Handles various lighting conditions and hand orientations

### Detection Pipeline
1. **Camera Input**: Captures frames from webcam
2. **Hand Detection**: MediaPipe identifies hands in the frame
3. **Landmark Extraction**: Extracts 21 3D landmarks per hand
4. **Finger State**: Determines which fingers are extended
5. **Visualization**: Draws landmarks, connections, and tracking info

## Technical Details

### Hand Landmarks
MediaPipe detects 21 landmarks per hand:
- Wrist (0)
- Thumb: 1, 2, 3, 4 (tip)
- Index: 5, 6, 7, 8 (tip)
- Middle: 9, 10, 11, 12 (tip)
- Ring: 13, 14, 15, 16 (tip)
- Pinky: 17, 18, 19, 20 (tip)

### Tracking Algorithm
- **Detection Confidence**: 0.7 (70% threshold)
- **Tracking Confidence**: 0.7 (maintains tracking across frames)
- **Max Hands**: 2 simultaneous hands
- **FPS**: Typically 30-60 FPS on modern hardware

## Customization

### Adjust Detection Sensitivity
In `main.py`, modify the HandDetector initialization:
```python
self.detector = HandDetector(
    max_hands=2,                    # Number of hands to track
    detection_confidence=0.7,       # Detection threshold (0.0-1.0)
    tracking_confidence=0.7         # Tracking threshold (0.0-1.0)
)
```

### Change Trail Length
In `main.py`, modify:
```python
self.max_trail_length = 30  # Number of points in trail
```

### Camera Resolution
In `main.py`, adjust:
```python
self.cap.set(3, 1280)  # Width
self.cap.set(4, 720)   # Height
```

## Troubleshooting

### Camera Not Opening
- Check if camera is already in use by another application
- Try different camera IDs: `app.start_camera(camera_id=1)`
- Verify camera permissions

### Low FPS
- Lower camera resolution
- Reduce max_hands to 1
- Close other applications using camera

### Hand Not Detected
- Ensure good lighting
- Keep hand within camera frame
- Distance: 0.5m - 2m from camera works best
- Lower detection_confidence threshold

## Future Enhancements

Potential features to add:
- Gesture recognition (specific hand poses)
- Recording and playback of gestures
- Multi-gesture sequence detection
- Virtual drawing/painting mode
- Mouse control via hand gestures
- Sign language recognition

## Credits

- **MediaPipe**: Google's open-source ML framework
- **OpenCV**: Open-source computer vision library

## License

This project is open source and available for educational purposes.

## Requirements

See `requirements.txt` for detailed dependencies.
