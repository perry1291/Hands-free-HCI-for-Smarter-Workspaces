import cv2  
import numpy as np
import time
import os # to access header jpg
import HandTrackingModule as htm
import pytesseract
from PIL import Image
import tkinter as tk
from threading import Thread
import math

# Set the path to the Tesseract executable if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'tesseract'  # Should work as it's in the system PATH

# Class for OCR Window using tkinter
class OCRWindow:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Recognized Text")
            self.root.geometry("400x300")
            
            # Create frame for controls
            self.control_frame = tk.Frame(self.root)
            self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
            
            # Create button to trigger OCR
            self.ocr_button = tk.Button(self.control_frame, text="Recognize Text", command=self.trigger_ocr)
            self.ocr_button.pack(side=tk.LEFT, padx=5)
            
            # Create button to clear text
            self.clear_button = tk.Button(self.control_frame, text="Clear Text", command=self.clear_text)
            self.clear_button.pack(side=tk.LEFT, padx=5)
            
            # Create text display with scrollbar
            self.text_frame = tk.Frame(self.root)
            self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            self.scrollbar = tk.Scrollbar(self.text_frame)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.text_display = tk.Text(self.text_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set)
            self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.config(command=self.text_display.yview)
            
            # OCR request flag
            self.ocr_requested = False
            self.canvas_image = None
            
            # Function to update canvas image from main program
            self.last_recognized_text = ""
            self.tkinter_available = True
        except:
            print("Tkinter window could not be created, OCR disabled")
            self.tkinter_available = False
        
    def trigger_ocr(self):
        if self.tkinter_available:
            self.ocr_requested = True
        
    def clear_text(self):
        if self.tkinter_available:
            self.text_display.delete(1.0, tk.END)
            self.last_recognized_text = ""
        
    def update_canvas(self, img):
        if self.tkinter_available:
            self.canvas_image = img.copy()
        
    def process_ocr(self):
        if self.tkinter_available and self.ocr_requested and self.canvas_image is not None:
            try:
                # Preprocess image for better OCR recognition
                gray = cv2.cvtColor(self.canvas_image, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)
                
                # Apply morphological operations to clean the image
                kernel = np.ones((2, 2), np.uint8)
                thresh = cv2.dilate(thresh, kernel, iterations=1)
                thresh = cv2.erode(thresh, kernel, iterations=1)
                
                # Perform OCR with improved configuration
                text = pytesseract.image_to_string(thresh, config='--psm 6 --oem 3')
                text = text.strip()
                
                # Only update if text is different and not empty
                if text and text != self.last_recognized_text:
                    self.text_display.insert(tk.END, text + "\n")
                    self.text_display.see(tk.END)
                    self.last_recognized_text = text
            except Exception as e:
                print(f"OCR error: {e}")
                
            self.ocr_requested = False
            
    def update(self):
        if self.tkinter_available:
            try:
                self.process_ocr()
                self.root.update()
                return True
            except Exception as e:
                # Only print the close message once
                print("OCR window closed")
                self.tkinter_available = False
                return False
        return False
        
    def close(self):
        if self.tkinter_available:
            try:
                self.root.destroy()
            except:
                pass

# Shape recognition helper functions
def detect_shape(points):
    """Detect if points form a recognizable shape"""
    if len(points) < 5:
        return None, None
        
    # Convert points to numpy array
    points = np.array(points, dtype=np.int32)
    
    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(points)
    
    # Get shape metrics
    area = cv2.contourArea(points)
    perimeter = cv2.arcLength(points, True)
    
    # Avoid division by zero
    if perimeter == 0:
        return None, None
        
    # Calculate circularity / roundness (1.0 for perfect circle)
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    
    # Calculate rectangularity (1.0 for perfect rectangle)
    rect_area = w * h
    rectangularity = area / rect_area if rect_area > 0 else 0
    
    # Calculate aspect ratio
    aspect_ratio = w / h if h > 0 else 0
    
    # Convex hull analysis
    hull = cv2.convexHull(points)
    hull_area = cv2.contourArea(hull)
    solidity = area / hull_area if hull_area > 0 else 0
    
    # Approximate the shape
    epsilon = 0.03 * perimeter  # Increased epsilon for better approximation
    approx = cv2.approxPolyDP(points, epsilon, True)
    num_vertices = len(approx)
    
    # Debug info
    print(f"Shape metrics: circularity={circularity:.2f}, rectangularity={rectangularity:.2f}, vertices={num_vertices}")
    
    # Shape detection logic with improved thresholds
    shape_type = None
    shape_points = None
    
    # Circle detection
    if circularity > 0.7:  # Lower threshold for more lenient circle detection
        # Find center and radius
        center, radius = cv2.minEnclosingCircle(points)
        center = (int(center[0]), int(center[1]))
        radius = int(radius)
        shape_type = "circle"
        shape_points = (center, radius)
        
    # Rectangle/Square detection - make more flexible
    elif (rectangularity > 0.7 and (num_vertices == 4 or num_vertices == 5)):
        # Check if it's a square
        if 0.85 < aspect_ratio < 1.15:
            shape_type = "square"
        else:
            shape_type = "rectangle"
            
        # Use minimum area rectangle for better alignment
        rect = cv2.minAreaRect(points)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        shape_points = box
        
    # Triangle detection - make more flexible
    elif (num_vertices == 3 or num_vertices == 4) and solidity > 0.7:
        shape_type = "triangle"
        # Use the approximated points
        shape_points = approx.reshape(-1, 2)
        
    # Line detection - improved logic
    elif (w > 3*h or h > 3*w) and ((w > 100) or (h > 100)):
        shape_type = "line"
        # Use PCA to get the main axis
        pts = np.float32(points)
        mean, eigenvectors = cv2.PCACompute(pts, mean=None)
        
        # Get direction vector
        direction = eigenvectors[0]
        direction = direction / np.linalg.norm(direction)
        
        # Get center
        center = np.float32([x + w/2, y + h/2])
        
        # Compute line endpoints
        endpoint1 = center - direction * max(w, h) * 0.6
        endpoint2 = center + direction * max(w, h) * 0.6
        
        # Convert to integers
        endpoint1 = tuple(map(int, endpoint1))
        endpoint2 = tuple(map(int, endpoint2))
        
        shape_points = np.array([endpoint1, endpoint2], dtype=np.int32)
    
    return shape_type, shape_points


def main():
    # Adjusted parameters for better drawing
    brushThickness = 8  # Slightly thinner for better precision
    eraserThickness = 80  # Smaller eraser for more control
    
    # Drawing smoothing parameters
    smoothening = 0.4  # Higher value = smoother lines but more lag (0-1)
    pointHistory = []  # Store recent drawing points for smoothing
    maxHistoryPoints = 5  # Number of points to average
    
    # Shape recognition parameters
    shape_mode = False  # Shape recognition mode
    drawing_points = []  # Points collected during drawing
    shape_points_min = 10  # Minimum points needed for shape recognition
    
    # Tutorial mode flag and state
    tutorialMode = True
    tutorialStep = 0
    tutorialMessages = [
        "Welcome! Raise your index and middle finger to select colors",
        "Put your hand in frame and try raising index & middle fingers",
        "Great! Now point at a color at the top to select it",
        "Now raise only index finger to draw",
        "Move your finger to draw. Two fingers up to select colors again",
        "Use black color as eraser. Press 'h' for help, 's' for shape mode"
    ]
    
    # Color palette - 8 colors
    colorList = [
        (0, 0, 255),    # red
        (0, 255, 255),  # yellow
        (255, 0, 0),    # blue
        (0, 0, 0),      # black (eraser)
        (0, 255, 0),    # green
        (255, 0, 255),  # magenta
        (0, 165, 255),  # orange
        (128, 0, 128)   # purple
    ]
    
    # Creating custom header with colors and function buttons
    headerImg = np.zeros((125, 1280, 3), np.uint8)
    
    # Draw color buttons
    numColors = len(colorList)
    btnWidth = 1000 // numColors
    for i in range(numColors):
        cv2.rectangle(headerImg, (i*btnWidth+50, 25), ((i+1)*btnWidth+50, 100), colorList[i], cv2.FILLED)
        # Add border to buttons
        cv2.rectangle(headerImg, (i*btnWidth+50, 25), ((i+1)*btnWidth+50, 100), (255, 255, 255), 2)
        # Add color label
        colorName = ["Red", "Yellow", "Blue", "Eraser", "Green", "Magenta", "Orange", "Purple"][i]
        textSize = cv2.getTextSize(colorName, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        textX = (i*btnWidth+50) + (btnWidth - textSize[0])//2
        cv2.putText(headerImg, colorName, (textX, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    header = headerImg
    
    # Create OCR button in header
    cv2.rectangle(header, (1200, 25), (1260, 100), (200, 200, 200), cv2.FILLED)
    cv2.rectangle(header, (1200, 25), (1260, 100), (255, 255, 255), 2)
    cv2.putText(header, "OCR", (1207, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Create shape mode button
    cv2.rectangle(header, (1130, 25), (1190, 100), (150, 150, 250), cv2.FILLED)
    cv2.rectangle(header, (1130, 25), (1190, 100), (255, 255, 255), 2)
    cv2.putText(header, "Shape", (1135, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    # Create clear button
    cv2.rectangle(header, (1060, 25), (1120, 100), (50, 50, 50), cv2.FILLED)
    cv2.rectangle(header, (1060, 25), (1120, 100), (255, 255, 255), 2)
    cv2.putText(header, "Clear", (1065, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Create a custom close button in the header - positioned in the top right of the interface
    cv2.rectangle(header, (1280-50, 0), (1280, 40), (50, 50, 50), cv2.FILLED)
    cv2.putText(header, "X", (1280-30, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Set up named windows with normal properties to enable close button
    cv2.namedWindow('Virtual Painter', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Canvas', cv2.WINDOW_NORMAL)

    # Initialize OCR window
    ocr_window = OCRWindow()
    
    # Camera setup
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera. Exiting.")
        return
        
    cap.set(3, 1280)
    cap.set(4, 720)

    # Initialize hand detector
    detector = htm.handDetector(detectionCon=0.7, maxHands=1)
    
    # Initialize drawing variables
    xp, yp = 0, 0
    smooth_x, smooth_y = 0, 0
    drawColor = (0, 0, 255)  # red
    
    # Initialize canvas
    imgCanvas = np.zeros((720,1280,3), np.uint8)
    
    # Timer for automatic OCR check
    ocr_timer = time.time()
    ocr_interval = 3  # Check every 3 seconds
    
    # Frame counter for stability
    frame_count = 0
    last_gesture = None
    gesture_stability_count = 0
    
    # Flag to track gesture transitions and drawing state
    actively_drawing = False
    current_drawing_id = 0
    last_selection_time = time.time()
    
    # Last detected shape and its render state
    last_shape_type = None
    last_shape_points = None
    last_shape_color = None

    # Function to apply smoothing to finger position
    def smooth_position(x, y, prev_x, prev_y, smoothening_factor):
        return int(prev_x + (x - prev_x) * smoothening_factor), int(prev_y + (y - prev_y) * smoothening_factor)
    
    # Function to clear canvas
    def clear_canvas():
        return np.zeros((720,1280,3), np.uint8)
    
    # Function to check if windows are still open
    def check_windows():
        try:
            prop1 = cv2.getWindowProperty('Virtual Painter', cv2.WND_PROP_VISIBLE)
            prop2 = cv2.getWindowProperty('Canvas', cv2.WND_PROP_VISIBLE)
            # Window closed if property becomes -1
            if prop1 < 0 or prop2 < 0:
                return False
            return True
        except:
            return False
    
    while True:
        # Frame counter
        frame_count += 1

        # Import image
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera")
            break

        img = cv2.flip(img, 1)

        # Find hand landmarks
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            try:
                # Get index and middle fingertips positions
                x1, y1 = lmList[8][1:]  # Index finger tip
                x2, y2 = lmList[12][1:]  # Middle finger tip
                
                # Check which fingers are up
                fingers = detector.fingersUp()
                
                # If both index and middle finger are up, it's selection mode
                if fingers[1] and fingers[2]:
                    # Apply shape recognition if we were drawing before
                    if actively_drawing and shape_mode and len(drawing_points) > shape_points_min:
                        shape_type, shape_pts = detect_shape(drawing_points)
                        if shape_type is not None:
                            # Store the shape data for persistent display
                            last_shape_type = shape_type
                            last_shape_points = shape_pts
                            last_shape_color = drawColor
                            
                            # Create a copy of the canvas before drawing the shape
                            temp_canvas = imgCanvas.copy()
                            
                            # Erase the original drawn shape
                            for pt in drawing_points:
                                cv2.circle(imgCanvas, pt, eraserThickness//2, (0,0,0), -1)
                            
                            # Draw refined shape on canvas
                            if shape_type == "circle":
                                center, radius = shape_pts
                                cv2.circle(imgCanvas, center, radius, drawColor, brushThickness)
                            elif shape_type in ["rectangle", "square"]:
                                cv2.drawContours(imgCanvas, [shape_pts], 0, drawColor, brushThickness)
                            elif shape_type == "triangle":
                                if len(shape_pts) >= 3:  # Make sure we have enough points
                                    cv2.drawContours(imgCanvas, [shape_pts.reshape((-1, 1, 2))], 0, drawColor, brushThickness)
                            elif shape_type == "line":
                                pt1, pt2 = shape_pts
                                cv2.line(imgCanvas, tuple(pt1), tuple(pt2), drawColor, brushThickness)
                    
                    # Reset drawing state
                    actively_drawing = False
                    drawing_points = []
                    
                    # Don't spam logs
                    if frame_count % 30 == 0:
                        print('selection mode')
                        
                    # checking for the click
                    if y1 < 125:
                        # Color selection
                        for i in range(numColors):
                            if i*btnWidth+50 < x1 < (i+1)*btnWidth+50:
                                drawColor = colorList[i]
                                # Update tutorial step if in tutorial mode
                                if tutorialMode and tutorialStep == 2:
                                    tutorialStep = 3
                        
                        # Close button press - top right X button
                        if 1280-50 < x1 < 1280 and 0 < y1 < 40:
                            print("Close button pressed!")
                            break
                            
                        # OCR button press
                        if 1200 < x1 < 1260:
                            ocr_window.trigger_ocr()
                            
                        # Shape button press
                        if 1130 < x1 < 1190:
                            shape_mode = not shape_mode
                            
                        # Clear button press
                        if 1060 < x1 < 1120:
                            imgCanvas = clear_canvas()
                            last_shape_type = None
                            print("Canvas cleared!")
                                
                    cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

                # Drawing mode - only index finger is up
                if fingers[1] and not fingers[2]:
                    # Don't spam logs
                    if frame_count % 30 == 0:
                        print('drawing mode')
                        
                    # Update tutorial step if in tutorial mode
                    if tutorialMode and tutorialStep == 3:
                        tutorialStep = 4
                        
                    # Draw circle at finger tip
                    cv2.circle(img, (x1,y1), 15, drawColor, cv2.FILLED)
                    
                    # Check if we just started a new drawing
                    if not actively_drawing:
                        # Reset drawing points completely when starting a new drawing
                        actively_drawing = True
                        current_drawing_id += 1
                        # Reset all drawing state
                        xp, yp = x1, y1
                        smooth_x, smooth_y = x1, y1
                        drawing_points = [(x1, y1)]
                    else:
                        # We're already drawing, continue the current stroke
                        
                        # Apply smoothing - weighted average of current and previous position
                        smooth_x, smooth_y = smooth_position(x1, y1, smooth_x, smooth_y, smoothening)
                        
                        # Add point to drawing points list for shape recognition
                        drawing_points.append((smooth_x, smooth_y))
                        
                        # Draw line between smooth points
                        if drawColor == (0,0,0):
                            cv2.line(img, (xp,yp), (smooth_x, smooth_y), drawColor, eraserThickness)
                            cv2.line(imgCanvas, (xp,yp), (smooth_x, smooth_y), drawColor, eraserThickness)
                        else:
                            cv2.line(img, (xp,yp), (smooth_x, smooth_y), drawColor, brushThickness)
                            cv2.line(imgCanvas, (xp,yp), (smooth_x, smooth_y), drawColor, brushThickness)

                        xp, yp = smooth_x, smooth_y
            except Exception as e:
                print(f"Error processing hand gestures: {e}")
        else:
            # No hand detected
            if actively_drawing:
                # If we lose hand detection while drawing, preserve the drawing state
                # but don't add new points
                pass
            
            # Update tutorial step if needed and in tutorial mode
            if tutorialMode and tutorialStep == 0:
                tutorialStep = 1

        # Process the canvas for display
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)
        
        # Setting header image
        img[0:125, 0:1280] = header
        
        # Display shape recognition status
        if shape_mode:
            cv2.putText(img, "Shape Recognition ON", (1050, 150), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(img, "Shape Recognition OFF", (1050, 150), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                  
        # Display last detected shape
        if last_shape_type is not None:
            cv2.putText(img, f"Last Shape: {last_shape_type.capitalize()}", (50, 150), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Display tutorial message if in tutorial mode
        if tutorialMode:
            # Add semi-transparent overlay for tutorial message
            overlay = img.copy()
            cv2.rectangle(overlay, (0, 600), (1280, 660), (0, 0, 0), -1)
            img = cv2.addWeighted(overlay, 0.5, img, 0.5, 0)
            
            # Add tutorial message
            cv2.putText(img, tutorialMessages[tutorialStep], (20, 640), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Blend with canvas for artistic effect
        img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
        
        # Update OCR canvas image
        ocr_window.update_canvas(imgCanvas)
        
        # Check for automatic OCR at regular intervals
        current_time = time.time()
        if current_time - ocr_timer > ocr_interval:
            if ocr_window.tkinter_available:
                ocr_window.trigger_ocr()
                ocr_timer = current_time
        
        # Update OCR window - only try if it's available
        if ocr_window.tkinter_available:
            try:
                if not ocr_window.update():
                    # Don't try again if it failed
                    ocr_window.tkinter_available = False
            except:
                # In case update throws an exception
                ocr_window.tkinter_available = False
        
        # Show the windows
        cv2.imshow('Virtual Painter', img)
        cv2.imshow('Canvas', imgCanvas)
        
        # Check if windows are closed
        if not check_windows():
            print("Window closed by user")
            break
        
        # Check for key press
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            print("Exiting program...")
            break
        elif key == ord('q') or key == ord('Q'):
            print("Exiting program...")
            break
        elif key == ord('o') or key == ord('O'):
            ocr_window.trigger_ocr()
        elif key == ord('c') or key == ord('C'):
            # Clear canvas
            imgCanvas = clear_canvas()
            last_shape_type = None
            print("Canvas cleared with 'c' key!")
        elif key == ord('h') or key == ord('H'):
            # Toggle tutorial mode
            tutorialMode = not tutorialMode
        elif key == ord('s') or key == ord('S'):
            # Toggle shape recognition mode
            shape_mode = not shape_mode
    
    # Clean up
    ocr_window.close()
    cap.release()
    cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    main()