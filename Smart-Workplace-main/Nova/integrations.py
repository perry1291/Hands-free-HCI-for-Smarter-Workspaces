"""
Nova App Integrations Module
This module provides integration functions for launching external applications from Nova
"""
import os
import subprocess
import sys
import threading
import signal
import psutil
import time

# Running processes tracking
powerpoint_process = None
whiteboard_process = None

def launch_powerpoint():
    """
    Launch the PowerPoint presentation application in a separate process
    """
    global powerpoint_process
    try:
        # Get the base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        powerpoint_dir = os.path.join(base_dir, "PowerPoint Presentation")
        
        # Ensure the path exists
        if not os.path.exists(powerpoint_dir):
            return False, "PowerPoint application directory not found"
            
        # Run the PowerPoint app in a separate process
        powerpoint_process = subprocess.Popen([sys.executable, os.path.join(powerpoint_dir, "main.py")], 
                        cwd=powerpoint_dir,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        
        return True, "PowerPoint presentation launched successfully"
    except Exception as e:
        return False, f"Error launching PowerPoint presentation: {str(e)}"


def launch_whiteboard():
    """
    Launch the whiteboard application in a separate process
    """
    global whiteboard_process
    try:
        # Get the base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        whiteboard_dir = os.path.join(base_dir, "whiteboard")
        
        # Ensure the path exists
        if not os.path.exists(whiteboard_dir):
            return False, "Whiteboard application directory not found"
            
        # Run the whiteboard app in a separate process
        whiteboard_process = subprocess.Popen([sys.executable, os.path.join(whiteboard_dir, "VirtualPainter.py")], 
                        cwd=whiteboard_dir,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        
        return True, "Whiteboard application launched successfully"
    except Exception as e:
        return False, f"Error launching whiteboard application: {str(e)}"


def stop_powerpoint():
    """
    Stop the PowerPoint presentation application
    """
    global powerpoint_process
    
    try:
        # First try to stop by stored process
        if powerpoint_process and powerpoint_process.poll() is None:
            try:
                # More aggressive termination
                if sys.platform == 'win32':
                    # On Windows, use taskkill to forcefully terminate the process
                    subprocess.run(f"taskkill /F /PID {powerpoint_process.pid} /T", shell=True)
                else:
                    # On Unix, kill with SIGKILL
                    powerpoint_process.kill()
                
                # Check if the process has terminated
                try:
                    powerpoint_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass  # Process may already be terminated
                    
                powerpoint_process = None
                return True, "PowerPoint presentation stopped successfully"
            except:
                # Continue to other methods if this fails
                pass
        
        # Second approach: find and kill processes containing "main.py" in PowerPoint directory
        killed = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline']:
                    cmd_line = ' '.join(proc.info['cmdline'])
                    if "PowerPoint Presentation" in cmd_line and "main.py" in cmd_line:
                        if sys.platform == 'win32':
                            # On Windows, use taskkill to forcefully terminate the process
                            subprocess.run(f"taskkill /F /PID {proc.info['pid']} /T", shell=True)
                        else:
                            # On Unix, kill with SIGKILL
                            proc.kill()
                        killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        if killed:
            return True, "PowerPoint presentation stopped by process search"
        
        # Third approach: target window title
        if sys.platform == 'win32':
            try:
                # Kill any Python process running the PowerPoint presentation by window title
                result = subprocess.run(
                    'taskkill /F /FI "WINDOWTITLE eq Presentation*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Also try process name
                result2 = subprocess.run(
                    'taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Presentation*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True, "PowerPoint presentation stopped using taskkill"
            except:
                pass
                
        # Fourth approach: brute force search for potential PowerPoint windows
        if sys.platform == 'win32':
            try:
                subprocess.run(
                    'taskkill /F /FI "WINDOWTITLE eq *Presentation*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True, "PowerPoint windows closed"
            except:
                pass
                
        return False, "PowerPoint presentation could not be found or is not running"
        
    except Exception as e:
        return False, f"Error stopping PowerPoint presentation: {str(e)}"


def stop_whiteboard():
    """
    Stop the whiteboard application
    """
    global whiteboard_process
    
    try:
        # First try to stop by stored process
        if whiteboard_process and whiteboard_process.poll() is None:
            try:
                # More aggressive termination
                if sys.platform == 'win32':
                    # On Windows, use taskkill to forcefully terminate the process
                    subprocess.run(f"taskkill /F /PID {whiteboard_process.pid} /T", shell=True)
                else:
                    # On Unix, kill with SIGKILL
                    whiteboard_process.kill()
                
                # Check if the process has terminated
                try:
                    whiteboard_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass  # Process may already be terminated
                    
                whiteboard_process = None
                return True, "Whiteboard application stopped successfully"
            except:
                # Continue to other methods if this fails
                pass
        
        # Second approach: find and kill processes containing "VirtualPainter.py"
        killed = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline']:
                    cmd_line = ' '.join(proc.info['cmdline'])
                    if ("whiteboard" in cmd_line and "VirtualPainter.py" in cmd_line) or "Virtual Painter" in cmd_line:
                        if sys.platform == 'win32':
                            # On Windows, use taskkill to forcefully terminate the process
                            subprocess.run(f"taskkill /F /PID {proc.info['pid']} /T", shell=True)
                        else:
                            # On Unix, kill with SIGKILL
                            proc.kill()
                        killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        if killed:
            return True, "Whiteboard application stopped by process search"
        
        # Third approach: target window title
        if sys.platform == 'win32':
            try:
                # Kill any Python process with whiteboard windows
                result = subprocess.run(
                    'taskkill /F /FI "WINDOWTITLE eq Virtual Painter*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Also try with more specific process name
                result2 = subprocess.run(
                    'taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Virtual Painter*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Also try canvas window
                result3 = subprocess.run(
                    'taskkill /F /FI "WINDOWTITLE eq Canvas*" /T', 
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True, "Whiteboard application stopped using taskkill"
            except:
                pass
                
        # Fourth approach: brute force search for potential Whiteboard windows
        if sys.platform == 'win32':
            try:
                subprocess.run(
                    'taskkill /F /FI "WINDOWTITLE eq *Whiteboard*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True, "Whiteboard windows closed"
            except:
                pass
                
        return False, "Whiteboard application could not be found or is not running"
        
    except Exception as e:
        return False, f"Error stopping whiteboard application: {str(e)}"


def shutdown_all_apps():
    """
    Forcefully stop all applications including the Nova UI when shutting down
    """
    try:
        # Stop PowerPoint
        stop_powerpoint()
        
        # Stop Whiteboard
        stop_whiteboard()
        
        # Kill any remaining Python processes (but not the current one)
        if sys.platform == 'win32':
            try:
                current_pid = os.getpid()
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        # Only kill other python processes
                        if proc.info['name'] == 'python.exe' and proc.info['pid'] != current_pid:
                            subprocess.run(f"taskkill /F /PID {proc.info['pid']} /T", shell=True)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
            except:
                pass
                
        # Kill any Chrome processes related to the Nova UI
        if sys.platform == 'win32':
            try:
                subprocess.run(
                    'taskkill /F /IM chrome.exe /FI "WINDOWTITLE eq Nova*" /T', 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except:
                pass
    except Exception as e:
        print(f"Error during shutdown: {str(e)}")
    finally:
        return True 