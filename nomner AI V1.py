import keyboard
import pyautogui
import random
import time
import re
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the coordinates of the region on the left monitor where you want to capture text
# Adjust these coordinates to match the position and size of the area on your left monitor
region_left_monitor = (1, 1095, 708, 251)  # Example: (left, top, width, height)

# List of random sentences to send
random_sentences = [
    "Yes",
    "No",
    "Not sure",
    "Nuh uh",
    "Let me think...",
    "Maybe",
    "No way!",
    "Totally!",
    "Hmm... interesting!",
    "That's a tough one!",
    "I'll have to consult my crystal ball on that.",
    "Ask again later, I'm busy playing Mindustry!",
    "In another universe, perhaps.",
    "The answer lies within the heart of the reactor...",
    "Have you tried turning it off and on again?",
    "I'd tell you, but then I'd have to delete your save file.",
    "A wise man once said, 'I don't know.'",
    "Why ask me when you can Google it?",
    "Are you sure you want to know the answer?",
    "Let me check the game's source code for you...",
    "I'll flip a coin. Heads for yes, tails for no.",
    "Why not both?",
    "Let's agree to disagree.",
    "I'm not programmed to answer that, but I can tell you a joke!",
    "How about we focus on building more silicon instead?",
    "The probability of a satisfactory answer is directly proportional to the quality of your question.",
    "If I had a pixel for every time I was asked that question, I'd have a full-screen display by now.",
    "That's classified information!",
    "Do you really want to know, or are you just testing me?",
    "Let's keep it mysterious, shall we?",
    "The answer is out there... somewhere.",
    "Why settle for a simple answer when you can have a complex one?",
    "I'm not omniscient, but I play one in this game!",
    "Let me consult with the other bots and get back to you.",
    "I could tell you, but then I'd have to delete this conversation.",
    "If I told you, I'd have to ban you from the server.",
    "Let's keep it a secret between you and me, okay?",
    "You'll have to earn that information through hours of gameplay!",
    "Sorry, I'm on a coffee break right now.",
    "I'll give you a hint: it rhymes with 'mindustry'.",
    "Why don't we tackle that question in the next software update?",
    "That's above my pay grade!",
    "I'm not a fortune teller, but I do play one on the internet.",
    "Let's not spoil the mystery of the game, shall we?",
    "If I had a byte for every time I was asked that question, I'd be rich in data!"
]

print("Starting in 5 seconds...")
time.sleep(5)

# Function to capture a screenshot of the specified region and extract text
def capture_and_extract_text(region):
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    return text

# Function to check if "nomner" is asked a question
def check_for_command_or_question(text):
    # Define a regular expression pattern to match "nomner" followed by a command or question
    pattern = r'nomner\s*(?:\w+\s*)+[?]'
    # Search for the pattern in the text
    match = re.search(pattern, text, re.IGNORECASE)
    # Return the matched text if found, None otherwise
    if match:
        return match.group()
    else:
        return None

# Function to send a random message
def send_random_message():
    # Shuffle the list of random sentences
    random.shuffle(random_sentences)

    # Select a random sentence
    message = random.choice(random_sentences)

    # Press Enter using keyboard module
    keyboard.press_and_release('enter')

    # Wait for a brief moment
    time.sleep(0.5)

    # Type the message
    pyautogui.typewrite(message)

    # Press Enter again using keyboard module
    keyboard.press_and_release('enter')

    print("Sent:", message)

# Function to send "Nomner AI is online" message
def send_online_message():
    # Press Enter to activate the chat
    keyboard.press_and_release('enter')

    # Wait for a brief moment
    time.sleep(0.5)

    # Type "Nomner AI is online"
    pyautogui.typewrite("[cyan]Nomner AI is online.[yellow] Ask me a question ending in a question mark.")

    # Press Enter again to send the message
    keyboard.press_and_release('enter')

    # Wait for a moment before starting to send random messages
    time.sleep(5)

    # Print message
    print("Nomner AI is online")

last_question = ""  # Initialize the variable to store the last question

# Main function
def main():
    global last_question  # Declare last_question as global so it can be accessed and modified inside the function

    # Send "Nomner AI is online" message
    send_online_message()

    # Print message
    print("Will start checking for commands or questions every 5 seconds...")

    try:
        while True:
            # Capture and extract text from the specified region on the left monitor
            extracted_text = capture_and_extract_text(region_left_monitor)
            print("Extracted Text:", extracted_text)

            # Check if "nomner" is followed by a command or question
            command_or_question = check_for_command_or_question(extracted_text)
            if command_or_question and command_or_question != last_question:  # Check if it's a new question
                print(f"Detected command or question: {command_or_question}")
                send_random_message()  # Send a random message
                last_question = command_or_question  # Update the last question

            # Wait for 5 seconds before checking again
            time.sleep(3)

    except KeyboardInterrupt:
        print("Script stopped.")

if __name__ == "__main__":
    main()