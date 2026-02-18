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
| Pinch once (Index + Thumb touch) | Left Click |
| Double Pinch (2x quickly) | Double Click / Open Application |
| Hold Pinch (3 seconds) | **DRAG files/objects** |
| Press 'Q' | Quit Program |
| Mouse to top-left corner | Emergency Stop |

## Visual Indicators

- **Green Circle** = Index fingertip (cursor control)
- **Blue Circle** = Thumb tip
- **Yellow Box** = High sensitivity zone (optimized for minimal hand movement)
- **Line between fingers** = Distance indicator
  - Blue line = Not pinching
  - Yellow line = Pinching (clicking)
- **Orange "PINCH: X.Xs"** = Pinch detected with countdown timer to drag
- **Green Progress Bar** = Visual indicator showing time until drag activates
- **Purple "DRAGGING!"** = Drag mode active (holding and moving)

## How to Use Drag Feature

**To drag files or objects:**

1. **Point** your index finger at the file/object you want to drag
2. **Pinch** your index finger and thumb together
3. **Hold the pinch for 3 full seconds** (watch the countdown timer and progress bar)
4. After 3 seconds, **"DRAGGING!"** will appear in purple
5. **Keep holding the pinch** and move your hand to drag the object
6. **Release the pinch** to drop the file at the new location

**For normal clicks:**
- Just pinch and release quickly (under 3 seconds)
- Every pinch release that isn't during a drag = click
- More reliable clicking - no minimum hold time needed!

**Why 3 seconds?**
- Prevents accidental dragging during normal clicks
- Gives you time to position correctly before drag starts
- Visual feedback (timer + progress bar) shows when drag will activate
- Clear distinction between click and drag operations

## Settings You Can Adjust

In `gesture_mouse.py`:

```python
# Smoothing (higher = smoother but slower, lower = more responsive)
self.smoothing = 5  # Optimized for responsiveness

# Pinch sensitivity (lower = easier to trigger)
self.pinch_threshold = 40

# Double-click timing (seconds)
self.double_click_time = 0.5

# Click cooldown to prevent accidental multiple clicks
self.click_cooldown = 0.3

# Drag threshold - how long to hold pinch before drag starts
self.drag_threshold_time = 3.0  # 3 seconds with visual progress bar

# Active zone margin (HIGHER = more sensitivity, less hand movement needed)
self.margin = 150  # Optimized for high sensitivity
```

## Sensitivity Tips

**Current setting is optimized for balanced sensitivity:**
- Small hand movements = large cursor movements
- Yellow zone is smaller = higher sensitivity
- Smoothing reduced for more responsive feel

**To adjust sensitivity:**
- **More sensitive**: Increase `self.margin` to 200
- **Less sensitive**: Decrease `self.margin` to 100
- **Smoother but slower**: Increase `self.smoothing` to 8-10
- **Faster but jittery**: Decrease `self.smoothing` to 3-4

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
