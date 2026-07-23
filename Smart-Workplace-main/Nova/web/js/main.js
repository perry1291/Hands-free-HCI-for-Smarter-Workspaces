'use strict';

// Voice recognition status management
let voiceEnabled = true; // Start with voice enabled

// Function to update the voice status indicator
function updateVoiceStatus(status) {
    const voiceStatus = document.getElementById('voice-status');
    if (!voiceStatus) return;
    
    if (status === 'active') {
        voiceStatus.className = 'voice-status active';
        voiceStatus.innerHTML = '<i class="fas fa-microphone"></i>';
        document.getElementById('userInput').placeholder = 'Type a command or speak (voice is enabled)...';
    } else if (status === 'inactive') {
        voiceStatus.className = 'voice-status';
        voiceStatus.innerHTML = '<i class="fas fa-microphone-slash"></i>';
        document.getElementById('userInput').placeholder = 'Type a command (voice is disabled)...';
    } else if (status === 'listening') {
        voiceStatus.className = 'voice-status active listening';
    }
}

// Initialize Clock Display
function updateTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    document.getElementById('time-display').textContent = `${hours}:${minutes}`;
}

// Update time every minute
updateTime();
setInterval(updateTime, 60000);

// Ensure input field is always visible and accessible
function ensureInputFieldVisible() {
    const inputField = document.getElementById("userInput");
    const inputContainer = document.getElementById("convForm");
    
    if (!inputField || !inputContainer) {
        console.error("Input elements not found!");
        return;
    }
    
    // Make sure the input container is visible
    inputContainer.style.display = 'flex';
    
    // Focus on the input field
    setTimeout(() => {
        inputField.focus();
    }, 100);
}

// Call this function periodically to ensure input remains visible
setInterval(ensureInputFieldVisible, 2000);

// Voice status toggle
document.addEventListener('DOMContentLoaded', function() {
    const voiceStatus = document.getElementById('voice-status');
    
    if (voiceStatus) {
        voiceStatus.addEventListener('click', function() {
            if (this.classList.contains('active')) {
                // Turn off voice
                voiceEnabled = false;
                updateVoiceStatus('inactive');
                
                // Send command to Python backend
                getUserInputWithValue('voice off');
            } else {
                // Turn on voice
                voiceEnabled = true;
                updateVoiceStatus('active');
                
                // Send command to Python backend
                getUserInputWithValue('voice on');
            }
        });
    }
});

// Helper function to send commands programmatically
function getUserInputWithValue(value) {
    try {
        eel.getUserInput(value);
    } catch (error) {
        console.error("Error sending command:", error);
    }
}

// Input handling with improved error handling
document.getElementById("userInputButton").addEventListener("click", getUserInput, false);
document.getElementById("userInput").addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        getUserInput();
    }
});

// Expose a method for Python to update the voice status
eel.expose(updateVoiceStatusFromPython);
function updateVoiceStatusFromPython(status) {
    updateVoiceStatus(status);
    voiceEnabled = (status === 'active' || status === 'listening');
}

// Improved DOMContentLoaded handler
document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById("userInput");
    
    // Add welcome message
    const messages = document.getElementById("messages");
    messages.innerHTML = '<div class="welcome-message">Welcome to Nova AI Assistant<br><span class="hint">Voice recognition is enabled. You can speak commands or type them directly.</span></div>';
    
    // Focus on input and add a visual hint
    setTimeout(() => {
        inputField.focus();
        inputField.style.animation = "highlightInput 1.5s ease infinite";
        
        // Remove the animation after user interacts with the input
        inputField.addEventListener('input', function() {
            this.style.animation = 'none';
        }, { once: true });
    }, 1000);
    
    // Ensure the input container is visible
    ensureInputFieldVisible();
    
    // Initialize voice status
    updateVoiceStatus('active');
});

// Add a typing indicator effect
function showTypingIndicator() {
    const element = document.getElementById("messages");
    element.innerHTML += '<div class="message to typing-indicator"><span></span><span></span><span></span></div>';
    element.scrollTop = element.scrollHeight;
    return element.childElementCount - 1;
}

function removeTypingIndicator(index) {
    const element = document.getElementById("messages");
    if (element.children[index] && element.children[index].classList.contains('typing-indicator')) {
        element.removeChild(element.children[index]);
    }
}

// Add sound effects for messages
const messageSentSound = new Audio('data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//tQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAADWgD///////////////////////////////////////////8AAAA8TEFNRTMuMTAwAQAAAAAAAAAAABSAJAJAQgAAgAAAA1rYzFgLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//sQZAAP8AAAaQAAAAgAAA0gAAABAAABpAAAACAAADSAAAAETEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVU=');
const messageReceivedSound = new Audio('data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//tQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAADWgD///////////////////////////////////////////8AAAA8TEFNRTMuMTAwAQAAAAAAAAAAABSAJAJAQgAAgAAAA1rGTjQLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//sQZAAP8AAAaQAAAAgAAA0gAAABAAABpAAAACAAADSAAAAETEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVU=');

// Expose EEL functions
eel.expose(addUserMsg);
eel.expose(addAppMsg);

// Add user message with animation and sound
function addUserMsg(msg) {
    messageSentSound.play();
    const element = document.getElementById("messages");
    element.innerHTML += '<div class="message from ready rtol">' + msg + '</div>';
    element.scrollTop = element.scrollHeight;
    
    // Animation completion
    const index = element.childElementCount - 1;
    setTimeout(changeClass.bind(null, element, index, "message from"), 500);
}

// Add app message with typing indicator, animation, and sound
function addAppMsg(msg) {
    // Show typing indicator
    const indicatorIndex = showTypingIndicator();
    
    // Calculate a realistic typing delay based on message length
    const typingDelay = Math.min(1000, Math.max(500, msg.length * 30));
    
    setTimeout(() => {
        // Remove typing indicator
        removeTypingIndicator(indicatorIndex);
        
        // Play sound and show message
        messageReceivedSound.play();
        const element = document.getElementById("messages");
        element.innerHTML += '<div class="message to ready ltor">' + msg + '</div>';
        element.scrollTop = element.scrollHeight;
        
        // Animation completion
        const index = element.childElementCount - 1;
        setTimeout(changeClass.bind(null, element, index, "message to"), 500);
    }, typingDelay);
}

// Change message class after animation
function changeClass(element, index, newClass) {
    if (element.children[index]) {
        element.children[index].className = newClass;
    }
}

// Get user input and clear input field with improved reliability
function getUserInput() {
    const element = document.getElementById("userInput");
    if (!element) {
        console.error("Input element not found!");
        return;
    }
    
    const msg = element.value.trim();
    if (msg.length !== 0) {
        element.value = "";
        
        // Make sure we focus back on the input after sending
        setTimeout(() => {
            element.focus();
        }, 100);
        
        try {
            eel.getUserInput(msg);
        } catch (error) {
            console.error("Error sending message:", error);
            // Try to recover
            setTimeout(() => {
                eel.getUserInput(msg);
            }, 500);
        }
    }
    
    // Ensure input field remains visible
    ensureInputFieldVisible();
}

// Add pulsing effect to submit button when there's text in the input
document.getElementById("userInput").addEventListener("input", function() {
    const submitButton = document.getElementById("userInputButton");
    if (this.value.trim().length > 0) {
        submitButton.classList.add("glow");
    } else {
        submitButton.classList.remove("glow");
    }
});