# Nova AI Assistant

Nova is a desktop AI assistant with voice recognition capabilities and a sleek dark blue user interface. 

## Features

- Voice recognition for hands-free operation
- Text-based chat interface with modern UI
- Web search functionality
- Location search
- Date and time queries
- File navigation
- Screenshot capture
- Clipboard operations (copy/paste)
- PowerPoint presentation with gesture control
- Whiteboard application with drawing and shape recognition

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/nova-assistant.git
cd nova-assistant
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

## Usage

There are two ways to run Nova:

### Option 1: Using the Batch File (Windows)
Simply double-click `run_nova.bat` to start Nova in a new window. The batch file will automatically handle any lingering processes.

### Option 2: Using Python Directly
Run the application from the command line:
```
python nova.py
```

If you're experiencing issues with port conflicts, use the clean flag:
```
python nova.py --clean
```

## Voice Commands

Nova responds to various voice commands, including:
- "Hello" - Greets you
- "What is your name" - Tells you its name
- "Date" - Shows the current date
- "Time" - Shows the current time
- "Search [query]" - Searches Google for your query
- "Location" - Asks for a place to locate on Google Maps
- "Screenshot" - Takes a screenshot of your screen
- "Copy" - Copies selected text
- "Paste" - Pastes text from clipboard
- "List" - Lists files in the root directory
- "PowerPoint" or "Presentation" - Launches the PowerPoint presentation app
- "Stop PowerPoint" or "Quit PowerPoint" - Stops the running PowerPoint app
- "Whiteboard" or "Drawing" - Launches the Whiteboard drawing application
- "Stop Whiteboard" or "Quit Whiteboard" - Stops the running Whiteboard app
- "Stop apps" or "Quit all apps" - Stops both PowerPoint and Whiteboard applications
- "Voice on/off" - Enables or disables voice recognition
- "Bye" - Puts the assistant to sleep
- "Exit", "Quit" or "Terminate" - Shuts down the assistant

## Troubleshooting

If you encounter issues:

1. **Port in use errors**: Try running with the clean flag: `python nova.py --clean`
2. **Voice recognition issues**: Make sure your microphone is properly connected and you have a stable internet connection
3. **UI not loading**: Check that you have Chrome installed, as it's used to render the UI

## Customization

You can customize Nova's appearance by modifying the CSS files in the `web/css` directory.

## Project Structure

The codebase has the following structure:
- `nova.py` - Main application file with all functionality
- `integrations.py` - Module for external application integrations
- `run_nova.bat` - Windows batch file for easy launching
- `web/` - Directory containing the UI files (HTML, CSS, JS)
- `screenshots/` - Directory where screenshots are saved

## Integrated Applications

Nova integrates with the following applications:

### PowerPoint Presentation
- Launch with voice commands: "PowerPoint", "Presentation", etc.
- Stop with voice commands: "Stop PowerPoint", "Quit PowerPoint", etc.
- Control slides with hand gestures:
  - Thumb up: Previous slide
  - Pinky up: Next slide
  - Index+Middle finger up: Show pointer
  - Index finger up: Draw on slides
  - Index+Middle+Ring finger up: Erase drawing

### Whiteboard
- Launch with voice commands: "Whiteboard", "Drawing", etc.
- Stop with voice commands: "Stop Whiteboard", "Quit Whiteboard", etc.
- Features:
  - Gesture-based drawing with multiple colors
  - Shape recognition (circles, triangles, rectangles)
  - OCR (Optical Character Recognition) for text extraction
  - Clear canvas and eraser functionality