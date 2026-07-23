# Gesture-Controlled PowerPoint Presentation

This application allows you to control PowerPoint presentations using hand gestures captured by your webcam. You can navigate between slides, draw annotations, and control the webcam preview using both hand gestures and keyboard shortcuts.

## Features

- **Slide Navigation**: Navigate between slides using hand gestures
- **Drawing Tool**: Draw annotations directly on slides with your finger
- **Pointer Mode**: Point to specific content without drawing
- **Annotation Eraser**: Remove annotations with a simple gesture
- **Fullscreen Presentation**: Display your presentation in fullscreen mode
- **Webcam Controls**: Toggle, move, and manage webcam preview

## System Requirements

- **Operating System**: Windows 10 or later
- **Python**: Version 3.6 or later
- **Webcam**: Built-in or external webcam
- **RAM**: At least 4GB recommended
- **Display**: Resolution of 1280x720 or higher recommended

## Installation

1. Install Python 3.x if not already installed
2. Install required dependencies using one of these methods:

   **Option 1**: Using requirements.txt (recommended)
   ```bash
   pip install -r requirements.txt
   ```

   **Option 2**: Install packages individually
   ```bash
   pip install opencv-python cvzone mediapipe numpy tensorflow
   ```

3. Clone or download this repository
4. Place your presentation slides in the "Presentation" folder (JPG format) or place your .pptx file in the "PowerPoint" folder

## Quick Start Guide

1. Run the program:
```bash
python main.py
```

2. Two windows will appear:
   - **Presentation window**: Full-screen display of your slides
   - **Webcam window**: Half-size display of your webcam with control information

3. Use hand gestures or keyboard shortcuts to control the presentation

## Detailed Controls

### Keyboard Controls

- **q**: Quit application (closes all windows properly)
- **h**: Hide/Show webcam preview on presentation
- **w**: Move webcam preview up
- **a**: Move webcam preview left
- **s**: Move webcam preview down
- **d**: Move webcam preview right
- **Esc**: Toggle fullscreen mode

### Hand Gestures

- **Thumb Only (👍)**: Previous slide
- **Pinky Only (🤙)**: Next slide
- **Index + Middle Fingers (✌️)**: Show pointer (temporary mark)
- **Index Finger Only (☝️)**: Draw annotations (persistent)
- **Index + Middle + Ring Fingers**: Erase last annotation
- **All Fingers Up (✋)**: Toggle webcam visibility

## Using the Drawing Feature

The drawing feature allows you to annotate slides in real-time:

1. Raise your hand so it's visible in the webcam
2. Hold up only your index finger (all other fingers down)
3. Move your finger to draw - the annotation will appear on the full presentation screen
4. Drawing works across the entire presentation, regardless of where your hand is in the webcam window
5. To stop drawing, change your hand gesture

## Green Threshold Line

The green horizontal line visible in the webcam window is the "gesture threshold":

- Hand gestures performed **above** this line trigger slide navigation actions
- Hand gestures performed **below** this line are for drawing and pointing

## Troubleshooting

- **Hand Detection Issues**: Ensure good lighting and keep your hand clearly visible
- **Slide Navigation Problems**: Make hand gestures clear and distinct above the green line
- **Drawing Not Working**: Ensure only your index finger is raised and other fingers are clearly down
- **Application Crashes**: Check you have all dependencies installed correctly
- **Folder Path Error**: Ensure your slides are in the correct folder and format

## Customization

You can modify these settings in the code:

- **Webcam Size**: Adjust the `current_ws` and `current_hs` variables
- **Gesture Threshold**: Change the `gestureThreshold` variable
- **Drawing Color/Thickness**: Modify parameters in the `draw_smooth_line` function

## File Structure

- **main.py**: Main application code
- **Presentation/**: Folder containing presentation slides (JPG format)
- **Powerpoint/**: Original PowerPoint file (optional)

## Credits

This application uses:
- OpenCV for image processing
- cvzone and MediaPipe for hand tracking
- NumPy for numerical operations
- TensorFlow for machine learning support 