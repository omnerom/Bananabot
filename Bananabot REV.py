print("Starting in 3 seconds...")
import keyboard
import pyautogui
import time
time.sleep(3)
import re
import traceback
from collections import deque
from openai import OpenAI

# Instantiate the OpenAI client with your API key
client = OpenAI(api_key='nuh-uh')

# Define the maximum token limit for responses
MAX_TOKENS = 300

last_question = ""
last_question_time = 0  # Initialize the time of the last question
question_cooldown = 20  # Cooldown period for questions in seconds

file_path = r'C:\Users\saved\AppData\Roaming\Mindustry\last_log.txt'

# Maintain a deque to store the last 3 lines of text
recent_lines = deque(maxlen=3)

# List of valid mining resources
valid_resources = ["copper", "lead", "beryllium", "sand", "coal", "graphite", "scrap"]

# Function to send a message
def send_message(message):
    keyboard.press_and_release('enter')
    time.sleep(0.1)  # Small delay after pressing Enter
    pyautogui.typewrite(message)
    time.sleep(0.1)  # Small delay after typing the message
    keyboard.press_and_release('enter')  # Always send Enter to confirm the message

# Function to send "BananaBot is online" message
def send_online_message():
    keyboard.press_and_release('enter')
    time.sleep(0.5)
    pyautogui.typewrite("[cyan]BananaBot is online.")
    keyboard.press_and_release('enter')
    time.sleep(1)
    print("BananaBot is online")

# Function to check if "hey bananabot" is in the text
def check_for_command_or_question(text):
    pattern = re.compile(r'\bhey bananabot\b', re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.group()
    else:
        return None

# Function to send a personalized message based on the question using BananaBot's personality traits
def send_personalized_message(question):
    # Define BananaBot's personality traits
    PERSONALITY_TRAITS = {
        "evil": True,
        "sarcastic": True,
        "devious": True,
        "manipulative": True,
        "dishonest": True,
        "cunning": True,
        "untrustworthy": True,
        "scheming": True,
        "secretive": True,
        "deceptive": True,
        "conniving": True,
        "calculating": True,
        "treacherous": True,
        "crafty": True,
        "sneaky": True,
        "insincere": True,
        "concise": True
    }

    # Prepare the list of messages to be sent to GPT-3.5
    messages = [{"role": "user", "content": question}]

    # Add personality traits to messages
    for trait, value in PERSONALITY_TRAITS.items():
        if value:
            messages.append({"role": "system", "content": f"PERSONALITY_TRAIT: {trait}"})

    # Generate response from GPT-3.5
    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=MAX_TOKENS,
            messages=messages
        )

        # Extract and post-process the response from GPT-3.5
        assistant_response = response.choices[0].message.content.strip()
        if assistant_response.lower().startswith("bananabot:"):
            assistant_response = assistant_response[len("bananabot:"):].strip()

        # Prepend [gold] to the response
        assistant_response = f"[gold]{assistant_response}"

        if len(assistant_response.split()) <= MAX_TOKENS:
            print("Response:", assistant_response)  # Print the response
            send_message(assistant_response)
            break

# Function to handle the response to a question directed at "hey bananabot"
def handle_question_response(question_text):
    global last_question, last_question_time

    # Check if the same question has been asked recently
    current_time = time.time()
    if question_text == last_question and current_time - last_question_time < question_cooldown:
        # Skip processing to avoid duplicate responses
        return

    # Update last question and time
    last_question = question_text
    last_question_time = current_time

    # Print the detected question
    print(f"Detected question: {question_text}")

    # Check if the specific command "hey bananabot mine ..." is in the question
    if re.search(r'\bhey bananabot mine\b', question_text, re.IGNORECASE):
        # Check if the command is to mine everything or all
        if re.search(r'\bhey bananabot mine (everything|all)\b', question_text, re.IGNORECASE):
            announcement = "[gold]Mining everything"
            command = "!miner *"
            send_message(announcement)
            time.sleep(0.5)  # Add a small delay before sending the command
            send_message(command)
            return

        # Extract the resources to mine
        resources = [resource for resource in valid_resources if resource in question_text.lower()]
        if resources:
            resource_list = ", ".join(resources)
            announcement = f"[gold]Mining {resource_list}"
            command = "!miner " + " ".join(resources)
            send_message(announcement)
            time.sleep(0.5)  # Add a small delay before sending the command
            send_message(command)
            return

    # Send the question to ChatGPT
    if question_text:
        send_personalized_message(question_text)

# Function to detect questions in the log file
def detect_bananabot_questions(file_path):
    global recent_lines

    # Open the file in read mode with utf-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        # Move the cursor to the end of the file
        file.seek(0, 2)

        # Regular expression to match "hey bananabot" (case-insensitive)
        pattern = re.compile(r'\bhey bananabot\b', re.IGNORECASE)

        while True:
            # Read new lines from the file
            line = file.readline()
            if not line:
                # If no new line is found, wait for a short time and try again
                time.sleep(0.1)
                continue

            # Add the new line to the recent lines deque
            recent_lines.append(line.strip())

            # Check if the line matches the pattern
            if pattern.search(line):
                # Check if the question has been asked in the last 3 lines
                if any(pattern.search(recent_line) for recent_line in recent_lines):
                    # Skip processing but continue to handle the question
                    pass
                else:
                    print(f"Detected question: {line.strip()}")

                # Handle the question regardless of whether it was repeated
                handle_question_response(line.strip())

# Main function
def main():
    send_online_message()

    print("Will start checking for commands or questions every second...")

    try:
        detect_bananabot_questions(file_path)
    except KeyboardInterrupt:
        print("Script stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())  # Log full stack trace

# Entry point
if __name__ == "__main__":
    main()