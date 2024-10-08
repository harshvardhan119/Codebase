from slack import WebClient
from datetime import datetime, timedelta
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key = gemini_api_key)

# Set your Slack API token
slack_token = slack_bot_token
client = WebClient(token=slack_token)


# Define a function to get messages from a channel
def get_messages_from_channel(channel_id, since_timestamp):
    messages = []
    try:
        response = client.conversations_history(channel=channel_id, oldest=since_timestamp)
        messages = response.get('messages', [])
    except Exception as e:
        print(f"Error fetching messages from channel {channel_id}: {e}")
    return messages

# Define a function to get messages from all channels
def get_messages_from_all_channels(channel_id, since_timestamp):
    all_messages = []
    messages = get_messages_from_channel(channel_id, since_timestamp)
    all_messages.extend(messages)
    return all_messages

# concatenate all the messages to form a string
def get_full_text_string(channel_id, past_hours):
    since_timestamp = (datetime.now() - timedelta(hours=int(past_hours))).timestamp()  # Timestamp for given past_hours ago
    messages = get_messages_from_all_channels(channel_id, since_timestamp)
    print("Total Messages Retrieved:", len(messages))
    final_text = ""
    for message in messages:
        final_text += message["text"] + " "
    return final_text



def process_using_gemini(input_string, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        f"{prompt} {input_string}")
    return response.text
