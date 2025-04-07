import keyboard
import pyautogui
import time
import re
import pytesseract
import random
from openai import OpenAI
import traceback
from datetime import datetime

# Function to wait 5 seconds before starting
print("Will start in 5 seconds...")
time.sleep(5)


# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Instantiate the OpenAI client with your API key
client = OpenAI(api_key='put your API key here!!!!')


# Define the coordinates of the region on the left monitor where you want to capture text
region_left_monitor = (1, 1160, 2000, 270)  # Example: (left, top, width, height)


# Define the maximum token limit for responses
MAX_TOKENS = 300


last_question = ""
last_question_time = 0  # Initialize the time of the last question
question_cooldown = 20  # Cooldown period for questions in seconds


last_extracted_text_time = time.time()  # Initialize the time of the last extracted text


# Function to capture a screenshot of the specified region and extract text
def capture_and_extract_text(region):
   global last_extracted_text_time


   screenshot = pyautogui.screenshot(region=region)
   text = pytesseract.image_to_string(screenshot)


   # Autocorrect "|" to "I"
   text = text.replace('|', 'I')


   # Update the time of the last extracted text
   last_extracted_text_time = time.time()


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
   pyautogui.typewrite("[cyan]BananaBot is online.")
   keyboard.press_and_release('enter')
   time.sleep(1)
   print("BananaBot is online")


# Function to check if "bananabot" is asked a question
def check_for_command_or_question(text):
   pattern = r'bananabot\s*(?:[\w\',]+\s*)+[?]'  # Updated pattern to allow for apostrophes and commas
   match = re.search(pattern, text, re.IGNORECASE)
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
       "devious": True
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


       # Extract and send the response from GPT-3.5
       assistant_response = response.choices[0].message.content
       if len(assistant_response.split()) <= MAX_TOKENS:
           send_message(assistant_response)
           break


# Function to handle the response to a question directed at "bananabot"
def handle_question_response(question_text):
   global last_question, last_question_time


   # Check if the same question has been asked recently
   current_time = time.time()
   if question_text == last_question and current_time - last_question_time < question_cooldown:
       print("Ignoring repeated question:", question_text)
       return


   last_question = question_text
   last_question_time = current_time


   if question_text:
       send_personalized_message(question_text)


# Main function
def main():
   send_online_message()


   print("Will start checking for commands or questions every second...")


   try:
       while True:
           start_time = time.time()  # Start timer
           extracted_text = capture_and_extract_text(region_left_monitor)
           print("Extracted Text", extracted_text)


           # Check for a question directed at "bananabot"
           command_or_question = check_for_command_or_question(extracted_text)
           if command_or_question:
               print(f"Detected command or question: {command_or_question}")
               handle_question_response(command_or_question)


           # Calculate elapsed time
           elapsed_time = time.time() - start_time
           if elapsed_time < 1:  # Adjust timeout threshold as needed
               time.sleep(1 - elapsed_time)  # Wait for the remaining time


   except KeyboardInterrupt:
       print("Script stopped by user.")
   except Exception as e:
       print(f"An error occurred: {e}")
       print(traceback.format_exc())  # Log full stack trace


# Entry point
if __name__ == "__main__":
   main()

