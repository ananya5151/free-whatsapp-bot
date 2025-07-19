import os
import requests
import json
from flask import Flask, request
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# Load credentials from .env file
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
HF_API_URL = os.getenv("HF_API_URL") # Your Hugging Face API URL

# This is the NEW function that uses the fast Google AI
def get_ai_response(message):
    """Calls the Google Gemini API to get a response."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        return "Error: Google AI API key not set."

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash') # Fast and powerful model
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        print(f"Error calling Google AI API: {e}")
        return "Sorry, my new Google brain seems to be offline."

def send_whatsapp_message(to_number, message):
    """Sends a message back to the user via WhatsApp."""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending WhatsApp message: {e}")

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # WhatsApp webhook verification
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Verification token mismatch", 403

    # Handle incoming messages
    data = request.get_json()
    if data and data.get("object") == "whatsapp_business_account":
        try:
            changes = data["entry"][0]["changes"][0]
            if changes.get("value") and changes["value"].get("messages"):
                message_data = changes["value"]["messages"][0]
                if message_data.get("type") == "text":
                    from_number = message_data["from"]
                    msg_body = message_data["text"]["body"]

                    # Get AI response and send it
                    ai_response = get_ai_response(msg_body)
                    send_whatsapp_message(from_number, ai_response)
        except (IndexError, KeyError) as e:
            print(f"Error parsing incoming webhook: {e}")

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)