import keyboard
import pyautogui
import random
import time
import re
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the coordinates of the region on the left monitor where you want to capture text
region_left_monitor = (1, 1095, 708, 251)  # Example: (left, top, width, height)

# Define the response dictionary
response_dict = {
    "mod": [
        "No, you may not have mod",
        "No way bro",
        "That's a bad idea",
        "Sure."
    ],
    "when": [
        "In about 10 minutes",
        "I dunno when",
        "Never",
        "How about now?",
        "Tomorrow perhaps..."
    ],
    "mindustry": [
        "Mindustry is an awesome game!",
        "I love playing Mindustry!",
        "Mindustry is a combination of mining and industry, hence the name!",
        "Have you built any complex factories in Mindustry yet?"
    ],
    "how": [
        "Try googling it",
        "Why would I know?",
        "Tbh idk",
        "Have you tried turning it off and on again?",
        "I'll give you a hint: it rhymes with 'mindustry'.",
        "One banana at a time, my friend, one banana at a time."
    ],
    "why": [
        "Because bananas!",
        "The bananas told me to",
        "To find the answer, you must peel back the layers of existence."
    ],
    "where": [
        "Somewhere over the rainbow.",
        "In a land far, far away...",
        "Right here, in the heart of the banana jungle!"
    ],
    "who": [
        "I am batman",
        "Batman",
        "The batman",
        "The hero that Gotham needs",
        "Gotham's protector"
    ],
    "8ball": [
        "I am better.",
        "I'm stronger.",
        "Who?"
    ],
    "bananabot help": [
        "[cyan]Bananabot is a chatbot made by Nomner. What can I improve?"
    ],
    "flip a coin": [
        "I'll flip a coin. Heads for yes, tails for no...... Heads!",
        "I'll flip a coin. Heads for yes, tails for no...... Tails!",
    ],
    # Add more keywords and corresponding responses as needed
}

# Define trigger word and response
trigger_word = "#bananabot-help"
response = "bananabot is here to help"

print("Starting in 5 seconds...")
time.sleep(5)

# Function to capture a screenshot of the specified region and extract text
def capture_and_extract_text(region):
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)

    # Autocorrect "|" to "I"
    text = text.replace('|', 'I')

    return text

# Function to send a message
def send_message(message):
    keyboard.press_and_release('enter')
    time.sleep(0.1)  # Small delay after pressing Enter
    pyautogui.typewrite(message)
    time.sleep(0.1)  # Small delay after typing the message
    keyboard.press_and_release('enter')  # Always send Enter to confirm the message
    print("Sent:", message)

# Function to send "BananaBot is online" message
def send_online_message():
    keyboard.press_and_release('enter')
    time.sleep(0.5)
    pyautogui.typewrite("[cyan]BananaBot is online.[yellow] Ask me for help. I can answer Who, Where, When, Why, and How questions")
    keyboard.press_and_release('enter')
    time.sleep(1)
    print("BananaBot is online")

last_question = ""

# Function to check if "bananabot" is asked a question
def check_for_command_or_question(text):
    pattern = r'bananabot\s*(?:\w+\s*)+[?]'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    else:
        return None

# Function to send a personalized message based on the question
def send_personalized_message(question):
    matching_keywords = [keyword for keyword, responses in response_dict.items() if keyword in question.lower()]
    if matching_keywords:
        selected_keyword = random.choice(matching_keywords)
        selected_response = random.choice(response_dict[selected_keyword])
        send_message(selected_response)
    else:
        send_random_message()  # If no matching keyword is found, send a random message


# Function to handle the response to a question directed at "bananabot"
def handle_question_response(question_text):
    if question_text:
        send_personalized_message(question_text)

# Function to send a random message
def send_random_message():
    random_sentences = [
        "Yes",
        "No",
        "Not sure",
        "Nuh uh",
        "Let me think...",
        "Maybe",
        "No way!",
        "Totally!",
    ]

    message = random.choice(random_sentences)
    send_message(message)


# Main function
def main():
    global last_question

    send_online_message()

    print("Will start checking for commands or questions every second...")

    try:
        while True:
            extracted_text = capture_and_extract_text(region_left_monitor)
            print("Extracted Text:", extracted_text)

            # Check for a question directed at "bananabot"
            command_or_question = check_for_command_or_question(extracted_text)
            if command_or_question and command_or_question != last_question:
                print(f"Detected command or question: {command_or_question}")
                handle_question_response(command_or_question)
                last_question = command_or_question

            time.sleep(1)  # Reduced sleep time to 1 second

    except KeyboardInterrupt:
        print("Script stopped.")


# Entry point
if __name__ == "__main__":
    main()