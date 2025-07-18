import os
import requests
import json
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load credentials from .env file
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
HF_API_URL = os.getenv("HF_API_URL") # Your Hugging Face API URL

def get_ai_response(message):
    """Calls the Hugging Face API to get a response."""
    if not HF_API_URL:
        return "Error: Hugging Face API URL not set."

    # This is the corrected payload format
    payload = {"user_input": message}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=180)
        response.raise_for_status()
        
        result = response.json()
        # The new API returns a 'response' key
        ai_message = result.get("response", "Sorry, I got a strange reply.")
        return ai_message

    except requests.exceptions.RequestException as e:
        print(f"Error calling Hugging Face API: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now."
    except (IndexError, KeyError) as e:
        print(f"Error parsing Hugging Face response: {e}")
        return "Sorry, I received an unusual response from my brain."


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