from twilio.twiml.messaging_response import MessagingResponse
import logging
from flask import Flask, request, make_response



app = Flask(__name__)


secret_token = 'EAAFvPm54i34BO8xpWV1nXwrk5ZB7KPXMO9BqB7o8bWq1zlciT4ZArpTB2T7mizPkPrzYGnjWTSrkuCkNZBWBZAjsjI32Qt3f3mhtZCvqQ4b0ltYAihSNKIbKygcOlSFiBrZCcBzZAAAeFQPwsC1crAbGFSKNcflMZATutxwuSl2yB5RjD7Hk6Ko8PB1jmwvr2TS8OXvtt1bYyKWqhKgZD'
VERIFY_TOKEN = 'mytestingtoken'

@app.route("/")
def func():
    return "project is working"

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.get("/")
def verify_token():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        logging.info("Verified webhook")
        response = make_response(request.args.get("hub.challenge"), 200)
        response.mimetype = "text/plain"
        return response
    logging.error("Webhook Verification failed")
    return "Invalid verification token"

@app.route('/messages', methods=['POST'])
def webhook():
    # Get the incoming message
    incoming_message = request.values.get('Body', '')

    # Create a response
    response = MessagingResponse()

    # Process the incoming message and create a reply
    reply_message = process_message(incoming_message)

    # Add the reply to the TwiML response
    response.message(reply_message)

    return str(response)

def process_message(message):
    # Add your logic to process the incoming message and generate a reply
    # For simplicity, let's just echo the received message
    return f"You said: {message}"

if __name__ == '__main__':
    app.run(port=5000)
