# # pip install  cvzone and pip install mediapipe
# import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# import tensorflow as tf
# import cv2
# # import os
# from cvzone.HandTrackingModule import HandDetector
# import numpy as np

# # Function to display webcam controls information
# def draw_control_info(img):
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     font_scale = 0.5
#     color = (255, 255, 255)
#     thickness = 1
    
#     controls = [
#         "Webcam Controls:",
#         "h: Hide/Show webcam",
#         "w/a/s/d: Move webcam",
#         "q: Quit application",
#         "Esc: Toggle fullscreen mode",
#         "Gesture: All fingers up to toggle webcam"
#     ]
    
#     y_pos = 30
#     for text in controls:
#         cv2.putText(img, text, (10, y_pos), font, font_scale, color, thickness)
#         y_pos += 20
    
#     return img

# # Function to map coordinates from webcam to presentation
# def map_coordinates(x, y, webcam_width, webcam_height, presentation_width, presentation_height):
#     # Map the coordinates from webcam space to presentation space
#     # Ensure full coverage of the presentation area from the webcam input
#     mapped_x = int(np.interp(x, [0, webcam_width], [0, presentation_width]))
#     mapped_y = int(np.interp(y, [0, webcam_height], [0, presentation_height]))
#     return mapped_x, mapped_y

# # Function to draw a smooth line between points
# def draw_smooth_line(img, points, color, thickness):
#     if len(points) < 2:
#         return
    
#     for i in range(1, len(points)):
#         # Draw line segment
#         cv2.line(img, points[i-1], points[i], color, thickness)
        
#         # Draw circle at junction for continuity
#         cv2.circle(img, points[i], thickness//2, color, cv2.FILLED)
    
#     # Draw circle at the last point
#     cv2.circle(img, points[-1], thickness//2, color, cv2.FILLED)

# #variables
# width, height = 1280, 720
# folderPath = "C:/Major Project/Smart-Workplace-main/Smart-Workplace-main/PowerPoint Presentation/Slides"

# #folderPath ="Presentation"

# #camera setup
# cap = cv2.VideoCapture(0)   
# cap.set(3, width)   # 3 is the id no.
# cap.set(4, height)

# #GET THE LIST OF PRESENTATION IMAGES
# pathImages = sorted(os.listdir(folderPath), key=len) #sorted the slides
# # print(pathImages) print the img no.

# #variables
# imgNumber = 0 #show the image of that number
# hs, ws = int(120*1), int(213*1)  # Default webcam size
# gestureThreshold =600
# buttonPressed = False
# buttonCounter = 0
# buttonDelay = 15
# annotations = [[]]
# annotationNumber = -1
# annotationStart = False
# lastDrawTime = 0  # For rate limiting drawing
# drawInterval = 10  # Milliseconds between draw points

# # Webcam preview control variables
# webcamVisible = True  # Toggle visibility
# webcamX = 0  # X position (top-left corner)
# webcamY = 0  # Y position (top-left corner)
# webcamScaleFactor = 1.0  # Scale factor fixed at 1.0

# # Variables to track window state
# isFullScreen = True

# #handdetector
# detector = HandDetector(detectionCon=0.8, maxHands=1)   #detectionCon means you 80% sure that hand

# while True:
#     #import Images
#     success, img = cap.read()   #check the img
#     img = cv2.flip(img, 1) # 1 means horizontal and 0 means vertical
#     pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
#     imgCurrent = cv2.imread(pathFullImage)
#     hands, img = detector.findHands(img)  #flipType=False
#     cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

#     # Get original image dimensions before any processing
#     h_orig, w_orig, _ = imgCurrent.shape

#     if hands and buttonPressed is False:
#         hand = hands[0]#first one hand
#         fingers = detector.fingersUp(hand)
#         cx, cy = hand['center']
#         lmList = hand['lmList']

#         #CONSTRAIN VALUE FOR EASIER DRAWING
#         # indexFinger = lmList[8][0], lmList[8][1]  #8indes number
#         # xVal = int(np.interp(lmList[8][0],[width//2,w],[0,width]))
#         # yVal = int(np.interp(lmList[8][1],[150, height-150], [0,height]))
#         # indexFinger = xVal, yVal
        
#         # Map coordinates from webcam view to presentation view
#         # This ensures drawing works across the entire presentation
        
#         # Map finger position to presentation coordinates
#         # Use full image dimensions for proper mapping across the entire slide
#         xVal = int(np.interp(lmList[8][0], [0, width], [0, w_orig]))
#         yVal = int(np.interp(lmList[8][1], [0, height], [0, h_orig]))
#         indexFinger = xVal, yVal

#         # Regular gesture handling 
#         if cy <= gestureThreshold:    #if hand is at the height of the face
#             #gesture 1
#             if fingers == [1,0,0,0,0]:
#                 print("left")          
#                 if imgNumber>0: #limitation to it
#                     buttonPressed = True
#                     imgNumber -=1
#                     annotations = [[]]
#                     annotationNumber = -1
#                     annotationStart = False
                
#             #gesture 2
#             if fingers == [0,0,0,0,1]:
                
#                 print("Right")              
#                 if imgNumber < len(pathImages)-1:
#                     buttonPressed = True
#                     imgNumber +=1
#                     annotations = [[]]
#                     annotationNumber = -1
#                     annotationStart = False
                    
#         #gesture 3 show pointer
#         if fingers == [0,1,1,0,0]:
#             cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)
#             # annotationStart = False

#         #gesture 4 Draw pointer
#         if fingers == [0,1,0,0,0]:
            
#             if annotationStart is False:
#                 annotationStart = True
#                 annotationNumber +=1
#                 annotations.append([])
            
#             # Draw circle indicator on current position
#             cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)
            
#             # Rate limit drawing to improve continuity
#             currentTime = cv2.getTickCount() / cv2.getTickFrequency() * 1000  # Convert to ms
#             if currentTime - lastDrawTime > drawInterval:
#                 # Store coordinates in annotations list for persistent drawing
#                 annotations[annotationNumber].append(indexFinger)
#                 lastDrawTime = currentTime
                
#                 # Draw the latest portion of the line
#                 if len(annotations[annotationNumber]) >= 2:
#                     # Get last few points for smoother immediate drawing
#                     recent_points = annotations[annotationNumber][-min(5, len(annotations[annotationNumber])):]
#                     draw_smooth_line(imgCurrent, recent_points, (0,0,200), 8)
#         else:
#             annotationStart = False

#         #gesture 5 Easer pointer
#         if fingers == [0,1,1,1,0]:
#             if annotations:
#                 annotations.pop(-1)
#                 annotationNumber -=1
#                 buttonPressed = True
        
#         #gesture 6 Toggle webcam visibility
#         if fingers == [1,1,1,1,1]:
#             webcamVisible = not webcamVisible
#             buttonPressed = True
                
#     #buttonPressed Iterations
#     if buttonPressed:
#         buttonCounter +=1
#         if buttonCounter > buttonDelay:
#             buttonCounter = 0
#             buttonPressed = False

#     # Draw all annotations with improved line thickness
#     # Get current dimensions for scaling
#     h_curr, w_curr, _ = imgCurrent.shape
    
#     # Scale factors to adjust annotation coordinates
#     scale_x = w_curr / w_orig
#     scale_y = h_curr / h_orig
    
#     for i in range(len(annotations)):
#         if len(annotations[i]) > 0:
#             # Scale annotation points to current image size
#             scaled_points = []
#             for point in annotations[i]:
#                 x, y = point
#                 scaled_x = int(x * scale_x)
#                 scaled_y = int(y * scale_y)
#                 scaled_points.append((scaled_x, scaled_y))
            
#             # Use the smooth line drawing function with scaled points
#             draw_smooth_line(imgCurrent, scaled_points, (0,0,200), 8)

#     #adding webcan image on slides
#     if webcamVisible:
#         # Fixed webcam size - using original larger size
#         current_ws = int(213*2)  # Original values doubled for larger webcam
#         current_hs = int(120*2)  # Original values doubled for larger webcam
        
#         # Resize webcam image
#         imgSmall = cv2.resize(img, (current_ws, current_hs))
        
#         # Get dimensions of current slide
#         h, w, _ = imgCurrent.shape
        
#         # Calculate positions ensuring webcam stays within slide boundaries
#         x_pos = min(max(webcamX, 0), w - current_ws)
#         y_pos = min(max(webcamY, 0), h - current_hs)
        
#         # Place webcam image on the slide at specified position
#         try:
#             imgCurrent[y_pos:y_pos+current_hs, x_pos:x_pos+current_ws] = imgSmall
#         except:
#             # Handle edge cases where dimensions might not match
#             pass
    
#     # Resize imgCurrent to the desired width and height
#     imgCurrent = cv2.resize(imgCurrent, (width, height))
    
#     # Remove drawing control information on slides
#     # imgCurrent = draw_control_info(imgCurrent)
    
#     # Display instructions on the webcam feed instead
#     img = draw_control_info(img)

#     # Resize webcam display to half screen
#     webcam_display = cv2.resize(img, (width//2, height//2))
    
#     # Create named window for presentation with current screen mode property
#     cv2.namedWindow("Presentation", cv2.WND_PROP_FULLSCREEN)
#     if isFullScreen:
#         cv2.setWindowProperty("Presentation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     else:
#         cv2.setWindowProperty("Presentation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    
#     # Display the windows
#     cv2.imshow("Webcam", webcam_display)
#     cv2.imshow("Presentation", imgCurrent)
    
#     key = cv2.waitKey(1)   #open time window  & 1 is delay pf milisecond
#     if key ==ord('q'):     #exit the window when we press the key q 
#         # Properly close all windows
#         cv2.destroyWindow("Webcam")
#         cv2.destroyWindow("Presentation")
#         cv2.destroyAllWindows()
#         cap.release()
#         break
#     elif key == 27:  # Escape key to toggle fullscreen mode
#         isFullScreen = not isFullScreen
#     # Webcam control keybindings
#     elif key == ord('h'):  # Toggle webcam visibility (h for hide/show)
#         webcamVisible = not webcamVisible
#     elif key == ord('w'):  # Move webcam up
#         webcamY = max(webcamY - 10, 0)
#     elif key == ord('s'):  # Move webcam down
#         webcamY += 10
#     elif key == ord('a'):  # Move webcam left
#         webcamX = max(webcamX - 10, 0)
#     elif key == ord('d'):  # Move webcam right
#         webcamX += 10


import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def draw_control_info(img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (255, 255, 255)
    thickness = 1
    
    controls = [
        "Webcam Controls:",
        "h: Hide/Show webcam",
        "w/a/s/d: Move webcam",
        "q: Quit application",
        "Esc: Toggle fullscreen mode",
        "Gesture: All fingers up to toggle webcam"
    ]
    
    y_pos = 30
    for text in controls:
        cv2.putText(img, text, (10, y_pos), font, font_scale, color, thickness)
        y_pos += 20
    
    return img

def draw_smooth_line(img, points, color, thickness):
    if len(points) < 2:
        return
    for i in range(1, len(points)):
        cv2.line(img, points[i-1], points[i], color, thickness)
        cv2.circle(img, points[i], thickness//2, color, cv2.FILLED)
    cv2.circle(img, points[-1], thickness//2, color, cv2.FILLED)

# --- Configuration ---
width, height = 1280, 720
folderPath = "C:/Major Project/Smart-Workplace-main/Smart-Workplace-main/PowerPoint Presentation/Slides"
valid_extensions = ['.jpg', '.jpeg', '.png']

# Get sorted list of image files
pathImages = sorted(
    [f for f in os.listdir(folderPath) if os.path.splitext(f)[1].lower() in valid_extensions],
    key=len
)

# 🔐 Prevent error if no slides
if not pathImages:
    print(f"❌ No slide images found in: {folderPath}")
    exit()

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Variables
imgNumber = 0
hs, ws = int(120*1), int(213*1)
gestureThreshold = 600
buttonPressed = False
buttonCounter = 0
buttonDelay = 15
annotations = [[]]
annotationNumber = -1
annotationStart = False
lastDrawTime = 0
drawInterval = 10
webcamVisible = True
webcamX, webcamY = 0, 0
webcamScaleFactor = 1.0
isFullScreen = True
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # ✅ Safe check here for index error
    if imgNumber >= len(pathImages):
        imgNumber = len(pathImages) - 1

    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    h_orig, w_orig, _ = imgCurrent.shape

    if hands and not buttonPressed:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        xVal = int(np.interp(lmList[8][0], [0, width], [0, w_orig]))
        yVal = int(np.interp(lmList[8][1], [0, height], [0, h_orig]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:
            if fingers == [1, 0, 0, 0, 0] and imgNumber > 0:
                print("⬅ Left Slide")
                buttonPressed = True
                imgNumber -= 1
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False

            if fingers == [0, 0, 0, 0, 1] and imgNumber < len(pathImages) - 1:
                print("➡ Right Slide")
                buttonPressed = True
                imgNumber += 1
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            currentTime = cv2.getTickCount() / cv2.getTickFrequency() * 1000
            if currentTime - lastDrawTime > drawInterval:
                annotations[annotationNumber].append(indexFinger)
                lastDrawTime = currentTime
                if len(annotations[annotationNumber]) >= 2:
                    recent_points = annotations[annotationNumber][-min(5, len(annotations[annotationNumber])):]
                    draw_smooth_line(imgCurrent, recent_points, (0, 0, 200), 8)
        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

        if fingers == [1, 1, 1, 1, 1]:
            webcamVisible = not webcamVisible
            buttonPressed = True

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    h_curr, w_curr, _ = imgCurrent.shape
    scale_x = w_curr / w_orig
    scale_y = h_curr / h_orig

    for i in range(len(annotations)):
        if annotations[i]:
            scaled_points = [(int(x * scale_x), int(y * scale_y)) for x, y in annotations[i]]
            draw_smooth_line(imgCurrent, scaled_points, (0, 0, 200), 8)

    if webcamVisible:
        current_ws, current_hs = int(213 * 2), int(120 * 2)
        imgSmall = cv2.resize(img, (current_ws, current_hs))
        h, w, _ = imgCurrent.shape
        x_pos = min(max(webcamX, 0), w - current_ws)
        y_pos = min(max(webcamY, 0), h - current_hs)
        try:
            imgCurrent[y_pos:y_pos + current_hs, x_pos:x_pos + current_ws] = imgSmall
        except:
            pass

    imgCurrent = cv2.resize(imgCurrent, (width, height))
    img = draw_control_info(img)
    webcam_display = cv2.resize(img, (width // 2, height // 2))

    cv2.namedWindow("Presentation", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Presentation", cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN if isFullScreen else cv2.WINDOW_NORMAL)

    cv2.imshow("Webcam", webcam_display)
    cv2.imshow("Presentation", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
    elif key == 27:
        isFullScreen = not isFullScreen
    elif key == ord('h'):
        webcamVisible = not webcamVisible
    elif key == ord('w'):
        webcamY = max(webcamY - 10, 0)
    elif key == ord('s'):
        webcamY += 10
    elif key == ord('a'):
        webcamX = max(webcamX - 10, 0)
    elif key == ord('d'):
        webcamX += 10
        