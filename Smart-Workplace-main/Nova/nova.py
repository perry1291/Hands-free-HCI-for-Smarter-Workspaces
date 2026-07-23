"""
Nova AI Assistant - Main Application
This file combines the web interface and assistant functionality in one place
"""
import eel
import os
import socket
import random
import sys
import threading
import traceback
import time
import subprocess
from queue import Queue

# Assistant functionality imports
import pyttsx3
import speech_recognition as sr
from datetime import date
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
from os import listdir
from os.path import isfile, join
import wikipedia

# Import integrations module for PowerPoint and Whiteboard functionality
from integrations import launch_powerpoint, launch_whiteboard, stop_powerpoint, stop_whiteboard

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Adjust speech recognition settings globally
r.dynamic_energy_threshold = True
r.energy_threshold = 300  # Lower threshold to detect speech more easily
r.pause_threshold = 0.5  # More responsive detection of the end of speech

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status
use_voice_input = True  # Voice input enabled by default

# Thread management
voice_thread = None
voice_data_queue = []
voice_thread_running = False
is_listening = False

class ChatBot:
    """Main chatbot class that handles the web interface and communication"""
    started = False
    userinputQueue = Queue()
    port_range_start = 45000
    port_range_end = 55000

    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    def popUserInput():
        return ChatBot.userinputQueue.get()

    def close_callback(route, websockets):
        """Called when the window is closed by clicking the X button"""
        print("Window closed by user - shutting down...")
        ChatBot.close()
        sys.exit(0)

    @eel.expose
    def getUserInput(msg):
        """Receives user input from the web interface"""
        ChatBot.userinputQueue.put(msg)
        print(msg)
    
    def close():
        """Handles graceful shutdown"""
        global voice_thread_running
        voice_thread_running = False
        ChatBot.started = False
        print("Nova AI Assistant is shutting down...")
    
    def addUserMsg(msg):
        """Adds a user message to the chat UI"""
        eel.addUserMsg(msg)
    
    def addAppMsg(msg):
        """Adds an assistant message to the chat UI"""
        eel.addAppMsg(msg)

    def get_random_available_port():
        """Generate a random port in a safe range and verify it's available"""
        for _ in range(50):  # Try up to 50 different ports
            port = random.randint(ChatBot.port_range_start, ChatBot.port_range_end)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except OSError:
                    continue
        
        # If we get here, we couldn't find an available port
        raise RuntimeError("Could not find an available port after 50 attempts")

    def start_web_interface():
        """Starts the web interface using eel"""
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(path + r'/web', allowed_extensions=['.js', '.html'])
        
        try:
            # Get a random available port
            port = ChatBot.get_random_available_port()
            print(f"Using port: {port}")
            
            # Launch eel with special exception handling
            try:
                eel.start('index.html', 
                        mode='chrome',
                        host='localhost',
                        port=port,
                        block=False,
                        size=(350, 480),
                        position=(10,100),
                        disable_cache=True,
                        close_callback=ChatBot.close_callback)
                
                ChatBot.started = True
                
                # Main loop
                while ChatBot.started:
                    try:
                        eel.sleep(10.0)
                    except Exception as sleep_exception:
                        print(f"Sleep exception (likely main thread exit): {sleep_exception}")
                        break
                    
            except Exception as start_exception:
                print(f"Error in eel.start: {start_exception}")
                traceback.print_exc()
        
        except Exception as e:
            print(f"Error starting application: {e}")
            traceback.print_exc()

# ------------------Assistant Functions----------------------
def reply(audio):
    """Speak and display a response"""
    ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    """Greet the user based on time of day"""
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Nova, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500 
    r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    """Convert spoken audio to text"""
    voice_data = ''
    try:
        # Initialize microphone source
        microphone = sr.Microphone()
        with microphone as source:
            # Don't re-adjust these settings each time as they're now set globally
            print("Listening...")
            
            # Adjust for ambient noise briefly
            r.adjust_for_ambient_noise(source, duration=0.3)
            
            try:
                # Wait for audio with a reasonable timeout
                audio = r.listen(source, phrase_time_limit=5, timeout=7)
                print("Recognizing...")
                
                try:
                    # Use the more reliable service
                    voice_data = r.recognize_google(audio)
                    print(f"Recognized: {voice_data}")
                    # Immediately return successful recognition
                    return voice_data.lower()
                except sr.RequestError as e:
                    print(f"Google Speech Recognition service error: {e}")
                    reply('Speech recognition service is unavailable. Please check your internet connection.')
                except sr.UnknownValueError:
                    print('Could not recognize speech')
            except sr.WaitTimeoutError:
                print("Listening timed out - no speech detected")
            except Exception as e:
                print(f"Error during listening: {str(e)}")
    except Exception as e:
        print(f"Microphone error: {str(e)}")
    
    # Only reached if there was an error
    return ""

def take_screenshot():
    """Take a screenshot and save it with timestamp"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/screenshot_{timestamp}.png'
        
        # Ensure screenshots directory exists
        os.makedirs('screenshots', exist_ok=True)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        reply(f"Screenshot saved as {screenshot_path}")
        return screenshot_path
    except Exception as e:
        reply(f"Failed to take screenshot: {str(e)}")
        return None

def respond(voice_data):
    """Process and respond to user commands"""
    global file_exp_status, files, is_awake, path
    print(voice_data)
    ChatBot.addUserMsg(voice_data)

    if is_awake == False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Nova!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    # PowerPoint Integration - Launch
    elif any(phrase in voice_data.lower() for phrase in ['powerpoint', 'presentation', 'open powerpoint', 'start powerpoint', 'launch powerpoint']):
        reply('Starting PowerPoint presentation app...')
        success, message = launch_powerpoint()
        if success:
            reply('PowerPoint presentation launched. Use hand gestures to control it.')
        else:
            reply(f'Sorry, I could not launch PowerPoint. {message}')

    # PowerPoint Integration - Stop
    elif any(phrase in voice_data.lower() for phrase in ['stop powerpoint', 'quit powerpoint', 'close powerpoint', 'exit powerpoint', 'end powerpoint']):
        reply('Stopping PowerPoint presentation...')
        success, message = stop_powerpoint()
        if success:
            reply('PowerPoint presentation has been stopped.')
        else:
            reply(f'Could not stop PowerPoint. {message}')

    # Whiteboard Integration - Launch
    elif any(phrase in voice_data.lower() for phrase in ['whiteboard', 'drawing', 'open whiteboard', 'start whiteboard', 'launch whiteboard']):
        reply('Starting Whiteboard application...')
        success, message = launch_whiteboard()
        if success:
            reply('Whiteboard launched. Use hand gestures to draw.')
        else:
            reply(f'Sorry, I could not launch Whiteboard. {message}')

    # Whiteboard Integration - Stop
    elif any(phrase in voice_data.lower() for phrase in ['stop whiteboard', 'quit whiteboard', 'close whiteboard', 'exit whiteboard', 'end whiteboard']):
        reply('Stopping Whiteboard application...')
        success, message = stop_whiteboard()
        if success:
            reply('Whiteboard application has been stopped.')
        else:
            reply(f'Could not stop Whiteboard. {message}')
            
    # Stop all applications
    elif any(phrase in voice_data.lower() for phrase in ['stop all apps', 'quit all apps', 'close all apps', 'stop apps', 'quit apps', 'close apps']):
        reply('Stopping all applications...')
        
        # Stop PowerPoint
        pp_success, pp_message = stop_powerpoint()
        
        # Stop Whiteboard
        wb_success, wb_message = stop_whiteboard()
        
        if pp_success and wb_success:
            reply('All applications have been stopped successfully.')
        elif pp_success:
            reply('PowerPoint stopped successfully, but could not stop Whiteboard.')
        elif wb_success:
            reply('Whiteboard stopped successfully, but could not stop PowerPoint.')
        else:
            reply('Could not stop any applications. They may not be running.')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        ChatBot.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'screenshot' in voice_data or 'screen shot' in voice_data or 'capture screen' in voice_data:
        reply('Taking a screenshot...')
        take_screenshot()

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif 'exit' in voice_data or 'terminate' in voice_data or 'quit' in voice_data:
        reply("Shutting down Nova. Goodbye!")
        ChatBot.close()
        sys.exit()
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest' in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

def update_voice_status(status):
    """Update voice status indicator in the UI"""
    try:
        eel.updateVoiceStatusFromPython(status)
        print(f"Voice status updated to: {status}")
    except Exception as e:
        print(f"Error updating voice status: {e}")

def voice_recognition_thread():
    """Background thread for voice recognition"""
    global voice_thread_running, is_listening
    while voice_thread_running:
        try:
            if use_voice_input:
                # Update UI to show we're listening
                if not is_listening:
                    is_listening = True
                    update_voice_status('listening')
                
                # Call record_audio to get voice input
                data = record_audio()
                
                if data:
                    print(f"Voice input detected: {data}")
                    voice_data_queue.append(data)
                    
                    # Briefly show we heard something before returning to listening
                    update_voice_status('active')
                    time.sleep(0.5)
                    update_voice_status('listening')
                else:
                    # Short sleep if no data to avoid tight looping
                    time.sleep(0.1)
            else:
                # Not listening anymore
                if is_listening:
                    is_listening = False
                    update_voice_status('inactive')
                    
                # Longer sleep when voice input is disabled
                time.sleep(0.5)
        except Exception as e:
            print(f"Voice thread error: {str(e)}")
            is_listening = False
            update_voice_status('inactive')
            time.sleep(0.5)  # Prevent rapid error cycling

def kill_python_processes():
    """Kill any lingering Python processes that might be using the ports"""
    try:
        print("Checking for lingering Python processes...")
        if sys.platform == 'win32':
            subprocess.run("taskkill /F /IM python.exe /T", shell=True, capture_output=True)
        else:
            # For Unix-like systems, we'd use a different approach
            pass
    except Exception as e:
        print(f"Warning: Failed to kill processes: {e}")

def start_assistant():
    """Main processing loop for the assistant"""
    global voice_thread_running, voice_thread, voice_data_queue, use_voice_input
    
    # Start voice recognition in a separate thread
    voice_thread_running = True
    voice_thread = threading.Thread(target=voice_recognition_thread)
    voice_thread.daemon = True  # Make this a daemon thread so it exits when main thread exits
    voice_thread.start()
    
    wish()
    voice_data = None
    
    # Main program loop with improved reliability
    while True:
        try:
            # Check for user text input first
            if ChatBot.isUserInput():
                # Take input from GUI
                voice_data = ChatBot.popUserInput()
                
                # Handle voice control commands
                if voice_data.lower() == "voice on":
                    use_voice_input = True
                    update_voice_status('active')
                    reply("Voice input enabled. You can now speak commands.")
                    voice_data = ""
                elif voice_data.lower() == "voice off":
                    use_voice_input = False
                    update_voice_status('inactive')
                    reply("Voice input disabled. Using text input only.")
                    voice_data = ""
            
            # Check if we have voice data from the thread
            elif voice_data_queue:
                voice_data = voice_data_queue.pop(0)
            else:
                # Small delay to prevent CPU overuse
                time.sleep(0.1)
                continue
    
            # Process voice_data only if it's not empty
            if voice_data:
                try:
                    respond(voice_data)
                except SystemExit:
                    print("Exiting Nova AI Assistant...")
                    break
                except Exception as e:
                    # More detailed exception handling
                    print(f"EXCEPTION: {str(e)}")
                    reply("Sorry, I encountered an error processing that request.")
                finally:
                    voice_data = None  # Clear voice data after processing
                    
        except KeyboardInterrupt:
            print("\nUser interrupted - shutting down...")
            break
        except Exception as e:
            print(f"Main loop error: {str(e)}")
            time.sleep(1)  # Prevent CPU overload in case of repeated errors

    # Clean up before exit
    ChatBot.close()
    voice_thread_running = False
    if voice_thread and voice_thread.is_alive():
        voice_thread.join(timeout=1.0)  # Wait for voice thread to terminate
    sys.exit(0)

def main():
    """Main function to start the Nova AI Assistant"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Nova AI Assistant")
    parser.add_argument('--clean', action='store_true', help='Kill lingering Python processes before starting')
    args = parser.parse_args()
    
    if args.clean:
        kill_python_processes()
    
    print("Starting Nova AI Assistant...")
    
    # Start the web interface in a separate thread
    web_thread = threading.Thread(target=ChatBot.start_web_interface)
    web_thread.daemon = True
    web_thread.start()
    
    # Wait for web interface to initialize
    while not ChatBot.started:
        time.sleep(0.1)
    
    # Start the assistant in the main thread
    try:
        start_assistant()
    except KeyboardInterrupt:
        print("\nShutting down Nova AI Assistant...")
        ChatBot.close()
        sys.exit(0)

if __name__ == "__main__":
    main() 