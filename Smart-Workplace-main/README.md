# Hands-free HCI for Smarter Workspaces

Smart Workplace is an AI-powered productivity suite that combines voice-controlled application management with PowerPoint and Whiteboard integration.

## Features

### Nova AI Assistant
- Voice command support for launching and controlling applications
- Seamless integration with PowerPoint and Whiteboard
- Natural language processing for application control
- Process management and monitoring
- Voice-activated commands for presentations and whiteboard sessions

### PowerPoint Integration
- Launch PowerPoint presentations using voice commands
- Navigate through slides using voice control
- Close presentations with voice commands
- Process monitoring and management

### Whiteboard Integration
- Launch Microsoft Whiteboard using voice commands
- Control whiteboard sessions through voice
- Efficient process management for whiteboard sessions


## Installation

1. Clone the repository:
```bash
git clone https://github.com/Janavikachi/Smart-Workplace.git
cd Smart-Workplace
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
.\venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## OCR Setup Instructions

To use the Optical Character Recognition (OCR) feature in the whiteboard, you need to install Tesseract OCR:

### Windows Installation:

1. Download Tesseract OCR:
   - Go to https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest installer (e.g., `tesseract-ocr-w64-setup-5.3.1.20230401.exe` for 64-bit Windows)

2. Install Tesseract:
   - Run the downloaded installer
   - Choose the installation directory (default is usually `C:\Program Files\Tesseract-OCR`)
   - **Important**: Remember the installation path

3. Add Tesseract to System PATH:
   - Open Windows Search and type "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables" button
   - Under "System Variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add the Tesseract installation path (e.g., `C:\Program Files\Tesseract-OCR`)
   - Click "OK" on all windows

4. Verify Installation:
   - Open a new Command Prompt
   - Type `tesseract --version`
   - If you see version information, the installation was successful

### Troubleshooting OCR:

1. If `tesseract` command is not recognized:
   - Double-check that you added the correct path to System PATH
   - Try restarting your computer
   - Verify the installation by checking if the Tesseract folder exists in Program Files

2. If OCR is not working in the application:
   - Make sure Tesseract is properly installed and in PATH
   - Check if the Python package `pytesseract` is installed
   - Ensure you have proper permissions to access the Tesseract installation

3. For better OCR results:
   - Ensure good lighting when using the whiteboard
   - Write clearly and legibly
   - Use contrasting colors (dark text on light background)
   - Keep the text size reasonable

## Directory Structure

```
smart-workplace/
├── Nova/
│   ├── nova.py                 # Main AI assistant script
│   └── run_nova.bat           # Windows batch file to run Nova
├── PowerPoint/                 # PowerPoint integration module
├── whiteboard/                # Whiteboard integration module
├── requirements.txt
└── README.md
```

## Module Usage Instructions

### 1. Nova AI Assistant (Nova/nova.py)
- Start Nova using `run_nova.bat` or `python nova.py`
- Available voice commands:
  - "Launch PowerPoint" - Opens PowerPoint
  - "Close PowerPoint" - Closes PowerPoint
  - "Launch Whiteboard" - Opens Whiteboard
  - "Close Whiteboard" - Closes Whiteboard
  - "Stop Nova" - Terminates the AI assistant

### 2. PowerPoint Integration (PowerPoint/)
- Ensures proper communication between Nova and PowerPoint
- Handles process management for PowerPoint applications
- Manages presentation states and commands

### 3. Whiteboard Integration (whiteboard/)
- Manages communication between Nova and Microsoft Whiteboard
- Handles process management for Whiteboard sessions
- Controls whiteboard states and commands

## Voice Commands Reference

1. PowerPoint Commands:
   - "Launch PowerPoint" - Starts PowerPoint application
   - "Close PowerPoint" - Closes active PowerPoint instance
   - "Next slide" - Moves to next slide
   - "Previous slide" - Moves to previous slide

2. Whiteboard Commands:
   - "Launch Whiteboard" - Opens Microsoft Whiteboard
   - "Close Whiteboard" - Closes active Whiteboard session

3. System Commands:
   - "Stop Nova" - Terminates the AI assistant
   - "Status" - Reports current application states

## Troubleshooting

1. Voice Recognition Issues:
   - Ensure you're in a quiet environment
   - Speak clearly and at a moderate pace
   - Check microphone settings in Windows

2. Application Launch Issues:
   - Verify PowerPoint and Whiteboard are properly installed
   - Check process management permissions
   - Ensure no conflicting applications are running
 
