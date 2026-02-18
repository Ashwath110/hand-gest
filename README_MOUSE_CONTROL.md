# Hand Gesture Mouse Control

Control your computer's mouse cursor using hand gestures captured by your webcam.

## Safety Features ✅

### 1. **Program-Only Control**
   - Gesture control ONLY works while the program is running
   - Your physical mouse works normally at all times
   - No system modifications or permanent changes

### 2. **Emergency Stop**
   - Press 'Q' key to quit immediately
   - Move mouse to TOP-LEFT corner of screen for emergency stop
   - Close camera window to stop

### 3. **Non-Invasive**
   - Does not disable or interfere with your regular mouse
   - Both gesture and physical mouse work simultaneously
   - No background processes after closing

## How to Use

### Installation
```bash
# Install required package
pip install pyautogui

# Or install all requirements
pip install -r requirements.txt
```

### Run the Program
```bash
python gesture_mouse.py
```

## Gesture Controls

| Gesture | Action |
|---------|--------|
| Point with INDEX finger | Move cursor |
| Quick Pinch (Index + Thumb touch) | Left Click |
| Double Pinch (2x quickly) | Double Click / Open Application |
| Hold Pinch (0.2+ seconds) | **DRAG files/objects** |
| Press 'Q' | Quit Program |
| Mouse to top-left corner | Emergency Stop |

## Visual Indicators

- **Green Circle** = Index fingertip (cursor control)
- **Blue Circle** = Thumb tip
- **Yellow Box** = Active tracking zone (LARGER - increased from 100px to 50px margin)
- **Line between fingers** = Distance indicator
  - Blue line = Not pinching
  - Yellow line = Pinching (clicking)
- **Orange "PINCHING!"** = Quick pinch detected (will click)
- **Purple "DRAGGING!"** = Drag mode active (holding and moving)

## Settings You Can Adjust

In `gesture_mouse.py`:

```python
# Smoothing (higher = smoother but slower)
self.smoothing = 7

# Pinch sensitivity (lower = easier to trigger)
self.pinch_threshold = 40

# Double-click timing (seconds)
self.double_click_time = 0.5

# Click cooldown to prevent accidental multiple clicks
self.click_cooldown = 0.3

# Drag threshold - how long to hold pinch before drag starts
self.drag_threshold_time = 0.2

# Active zone margin (lower = larger active zone)
self.margin = 50  # Changed from 100 for BIGGER zone
```

## Troubleshooting

**Camera not opening?**
- Close other applications using the camera (Skype, Zoom, etc.)
- Check camera permissions in Windows settings

**Cursor movement too sensitive?**
- Increase `self.smoothing` value (try 10-15)

**Clicks not registering?**
- Increase `self.pinch_threshold` value (try 50-60)

**Hand not detected?**
- Ensure good lighting
- Keep hand within yellow tracking zone
- Distance: 0.5m - 2m from camera

## Safety Guarantee

✅ **This program:**
- Only runs when you execute it
- Stops completely when closed
- Does not modify system settings
- Does not disable your physical mouse
- Creates no background processes

❌ **This program does NOT:**
- Run at startup
- Continue after closing
- Modify Windows mouse settings
- Disable your physical mouse
- Create any permanent changes

## Uninstalling

Simply delete the files - no cleanup needed! Your system remains completely unchanged.
