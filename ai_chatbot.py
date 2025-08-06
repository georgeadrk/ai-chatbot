# Import all required modules
import time
import os
import joblib
import google.generativeai as genai
from dotenv import load_dotenv

# Step 1: Introduction
print("💬 Welcome to the George AI Chatbot Project!")
print("We'll build a chatbot step by step using Google Gemini API.")
print("Follow the prompts to set up your chatbot. 🚀\n")

# Step 2: Configure the API Key
print("Step 1: Configure your API Key")
print("Hint: Add your API Key to a `.env` file or enter it now.")
GOOGLE_API_KEY = input("Enter your Google API Key: ")

print("\nSetting up Gemini API...")
load_dotenv()

# Load the API key from `.env` if not provided
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Exit if no API key is found
if not GOOGLE_API_KEY:
    print("❌ Error: API Key not found. Please set it in `.env` or input it manually.")
    exit(1)

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
print("✅ Gemini API configured successfully!\n")

# Step 3: List Available Models
print("\nStep 2: List Available Models")
models = genai.list_models()  # List available models
print("Available models:")
for model in models:
    print(f"- {model}")

# Ask user to select a model from the list
model_name = input("\nEnter the model name you'd like to use (e.g., 'gemma-3n-e2b-it'): ")

# Step 4: Create a Unique Chat Session
print("\nStep 3: Create a unique chat session.")
chat_title = input("Enter a name for your chat session (default: 'ChatSession'): ") or "ChatSession"
new_chat_id = f"{time.time()}"

# Step 5: Ensure the data folder exists
if not os.path.exists('data/'):
    os.mkdir('data/')

# Load previous chat sessions if available
try:
    past_chats = joblib.load('data/past_chats_list')
    print("\nPrevious chat sessions loaded successfully.")
except FileNotFoundError:
    past_chats = {}
    print("\nNo previous chat sessions found. Starting fresh.")

# Step 6: Initialize the Gemini Model
print("\nInitializing the generative model...")
try:
    # Use the correct model name (adjust based on available models)
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat()
    print(f"✅ Model '{model_name}' initialized successfully!")
except Exception as e:
    print(f"❌ Error: Could not initialize model '{model_name}'. Details: {e}")
    exit(1)

# Step 7: Load Chat History
try:
    messages = joblib.load(f"data/{new_chat_id}-messages")
except FileNotFoundError:
    messages = []  # Initialize an empty list if no history exists

# Step 8: Start the Chat Session
print("\n🎉 Your chatbot is ready! Let's start chatting.")
print("Type 'exit' to end the chat.\n")

# Save the new chat session if it doesn't already exist
if new_chat_id not in past_chats:
    past_chats[new_chat_id] = chat_title
    joblib.dump(past_chats, 'data/past_chats_list')

# Step 9: Chat Loop
while True:
    user_input = input(f"{chat_title} (You): ")
    if user_input.lower() == 'exit':
        print("🛑 Chat session ended.")
        break

    try:
        # Send the user's input to the model and receive a response
        response = chat.send_message(user_input)
        print(f"Best Buddy: {response.text}")

        # Append user and AI messages to the chat history
        messages.append({'role': 'user', 'content': user_input})
        messages.append({'role': 'ai', 'content': response.text})

        # Save the updated chat history
        joblib.dump(messages, f"data/{new_chat_id}-messages")
        print("💾 Chat history saved.\n")

    except Exception as e:
        print(f"❌ Error: Something went wrong while sending the message. Details: {e}")
