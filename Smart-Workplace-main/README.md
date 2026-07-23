# Hands-free Human–Computer Interaction for Smarter Workspaces

An AI-powered Human–Computer Interaction (HCI) system that enables users to interact with computers using **voice commands**, **hand gestures**, and **computer vision**, eliminating the need for traditional input devices such as keyboards and mice.

The project integrates a virtual AI assistant, gesture-controlled presentation system, and intelligent virtual whiteboard into a unified desktop application for touch-free productivity.

---

## Features

### 🎙️ Nova AI Assistant
- Voice-controlled desktop assistant
- Launch and terminate applications
- Open websites and perform Google searches
- Location search using Google Maps
- File and folder navigation
- Take screenshots
- Clipboard operations
- Voice and text-based interaction
- System command execution

### 🖐️ Gesture-Controlled Presentation
- Hands-free PowerPoint slide navigation
- Virtual laser pointer
- Slide annotation
- Annotation erase functionality
- Webcam overlay support
- Fullscreen presentation mode

### 🎨 Smart Virtual Whiteboard
- Air drawing using hand gestures
- Multiple drawing colors
- Eraser tool
- Shape recognition
- OCR-based handwriting recognition
- Real-time drawing smoothing
- Interactive canvas interface

---

## Project Architecture

```
                     Nova AI Assistant
          (Speech Recognition + Desktop Automation)
                          │
          ┌───────────────┴───────────────┐
          │                               │
 Gesture-Controlled Presentation    Smart Virtual Whiteboard
     (Computer Vision)           (Drawing + OCR + Shape Detection)
```

---

## Technology Stack

### Programming Language
- Python

### Computer Vision
- OpenCV
- MediaPipe
- cvzone

### Artificial Intelligence
- TensorFlow
- SpeechRecognition
- Tesseract OCR

### Desktop Automation
- PyAutoGUI
- pynput
- psutil
- subprocess

### GUI
- Eel
- Tkinter

### Supporting Libraries
- NumPy
- pyttsx3
- Wikipedia API

### Development Tools
- VS Code
- Git
- GitHub

---

## Project Modules

### 1. Nova AI Assistant

Nova serves as the central controller of the system.

It continuously listens for voice commands and performs desktop automation tasks such as:

- Opening applications
- Launching the presentation module
- Launching the virtual whiteboard
- Web searches
- File management
- Location search
- Voice responses
- Application shutdown

The assistant provides both voice and text-based interaction through an Eel-powered graphical interface.

---

### 2. Gesture-Controlled Presentation

This module allows users to control PowerPoint presentations entirely through hand gestures.

Supported interactions include:

- Next slide
- Previous slide
- Laser pointer
- Slide annotation
- Erasing annotations
- Webcam controls

Hand tracking is performed using MediaPipe landmarks while OpenCV processes the camera feed in real time.

---

### 3. Smart Virtual Whiteboard

The whiteboard enables users to draw in the air using hand gestures.

Features include:

- Real-time drawing
- Smooth handwriting
- Shape recognition
- OCR-based handwriting extraction
- Multiple drawing colors
- Eraser
- Canvas management

Recognized geometric shapes include:

- Circle
- Rectangle
- Square
- Triangle
- Straight Line

---

## OCR Pipeline

The project extracts handwritten text from the virtual whiteboard using Tesseract OCR.

Image preprocessing includes:

- Grayscale conversion
- Binary thresholding
- Dilation
- Erosion

These preprocessing steps improve OCR accuracy before text extraction.

---

## Workflow

1. User issues a voice command or performs a hand gesture.
2. Nova processes speech commands using SpeechRecognition.
3. MediaPipe detects hand landmarks from webcam frames.
4. OpenCV interprets gestures and maps them to system actions.
5. OCR extracts handwritten text from the whiteboard.
6. Desktop automation modules execute the requested task.

---

## Challenges Addressed

- Real-time hand tracking
- Gesture stability and smoothing
- Voice recognition responsiveness
- Multi-process application management
- OCR preprocessing for improved recognition
- Shape detection using contour analysis
- Coordinate mapping between webcam and presentation canvas
- Desktop automation through voice commands

---

## Applications

- Smart Classrooms
- Online Teaching
- Business Presentations
- Accessibility Solutions
- Touch-free Workstations
- Collaborative Workspaces
- Interactive Learning Environments

---

## Future Improvements

- Offline speech recognition
- Deep learning-based gesture classification
- Multi-user gesture recognition
- Custom gesture training
- Cloud synchronization
- Multilingual voice assistant
- Gesture personalization
- Cross-platform compatibility

---

## Repository Structure

```
SMART-WORKPLACE-MAIN/
│
├── Nova/
│   ├── nova.py
│   ├── integrations.py
│   ├── web/
│   └── README.md
│
├── PowerPoint Presentation/
│   ├── main.py
│   └── Slides/
│
├── whiteboard/
│   ├── VirtualPainter.py
│   ├── HandTrackingModule.py
│   └── README.md
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/Hands-Free-HCI.git
cd Hands-Free-HCI
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Tesseract OCR

Download and install Tesseract OCR:

https://github.com/tesseract-ocr/tesseract

Ensure the executable is added to your system PATH.

---

## Run

```bash
python main.py
```

---

## Research Publication

This project was presented as a research paper:

**Hands-Free Human–Computer Interaction for Smarter Workspaces**

The work explores multimodal human–computer interaction by integrating computer vision, speech recognition, OCR, and desktop automation into a unified hands-free workspace system.


---

## License

This project is intended for educational and research purposes.
