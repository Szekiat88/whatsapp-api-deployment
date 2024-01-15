from flask import Flask, request, make_response
import os
import json 
import requests
from heyoo import WhatsApp
import logging

#secret_token = "EAAFvPm54i34BO9R3GIaR0B5y4aaklyOHJ7abuZCIRDQmvg9hRk41WcZAUAaI1t1pLWIAJb2WymE5nduKQYt9moMf8Fpx5YVtBJN7TSjMlaecdahDGSAx94nhalYAmSZCOMma1eX4lSbf7wze3cyZBFeSYhN5jhPR1AjmViiecAt5DZBqlWwmZAz6Shm5I5ZBo0nqSgObSNmmPYGGLgQOpKc"
os.environ.get("secret.config")
app = Flask(__name__)

secret_token = 'EAAFvPm54i34BO8xpWV1nXwrk5ZB7KPXMO9BqB7o8bWq1zlciT4ZArpTB2T7mizPkPrzYGnjWTSrkuCkNZBWBZAjsjI32Qt3f3mhtZCvqQ4b0ltYAihSNKIbKygcOlSFiBrZCcBzZAAAeFQPwsC1crAbGFSKNcflMZATutxwuSl2yB5RjD7Hk6Ko8PB1jmwvr2TS8OXvtt1bYyKWqhKgZD'
messenger = WhatsApp(secret_token,  phone_number_id='156388757567283')
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

@app.post("/messages")
def hook():
    # Handle Webhook Subscriptions
    logging.info("Sister its work")
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    
 
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.is_message(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                messenger.send_message(f"Hi {name}, nice to connect with you", mobile)
                messenger.send_reply_button(
                    recipient_id="60192585268",
                    button={
                        "type": "button",
                        "body": {
                            "text": "This is a test button"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "b1",
                                        "title": "This is button 1"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "b2",
                                        "title": "this is button 2"
                                    }
                                }
                            ]
                        }
                },
                )
                messenger.send_button(
                    recipient_id="60192585268",
                    button={
                        "header": "Header Testing",
                        "body": "Body Testing",
                        "footer": "Footer Testing",
                        "action": {
                            "button": "Button Testing",
                            "sections": [
                                {
                                    "title": "iBank",
                                    "rows": [
                                        {"id": "row 1", "title": "Send Money", "description": ""},
                                        {
                                            "id": "row 2",
                                            "title": "Withdraw money",
                                            "description": "",
                                        },
                                    ],
                                }
                            ],
                        },
                    },
                )

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                interactive_type = message_response.get("type")
                message_id = message_response[interactive_type]["id"]
                message_text = message_response[interactive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "document":
                file = messenger.get_document(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                logging.info(f"{mobile} sent {message_type} ")
                logging.info(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                logging.info(f"Message : {delivery}")
            else:
                logging.info("No new message")
    return "OK", 200

# @app.route("/messages" , methods = ["POST" , "GET"])
# def message():
#     if request.method == "GET":
#         sent_token = str(request.args.get("hub.verify _token")).split(" ")[0]
#         print (sent_token , "/n" , secret_token) 
#         # if sent_token != secret_token:
#         #     return app.make_response((f"forbidden token {sent_token} ans {secret_token}", 403)) 
#         # if request.args.get("hub.mode") != "subscribe":
#         #     return app.make_response(("forbidden mode", 403))

#         res = request.args.get("hub.challenge")
#         mode = request.args.get("hub.mode")
#         token = request.args.get("hub.verify _token")
#         challenge = request.args.get('hub.challenge')
#         if mode and token:
#             if mode == 'subscribe' and token == "mytestingtoken":
#                 print("WEBHOOK_VERIFIED")
#                 return app.make_response((str(res) , 200))
#             else:
#                 return app.make_response((str(res) , 403))
#         else:    
#             # url = "https://graph.facebook.com/v18.0/156388757567283/messages"
#             # header = {'Content-type': 'application/json', 'Authorization': 'Bearer '+ str(secret_token)}
#             # char = request.json
#             # phone = char ["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
#             # ans = "hey , how u doin"
#             # data = {
#             #     "messaging product": "whatsapp",
#             #     "to": 60192585268,
#             #     "type": "text", 
#             #     "text": {
#             #         "body": ans}}
#             # answer = requests.post(url, headers=header, data=json.dumps(data))
            
#             # messenger = WhatsApp('EAAFvPm54i34BO9R3GIaR0B5y4aaklyOHJ7abuZCIRDQmvg9hRk41WcZAUAaI1t1pLWIAJb2WymE5nduKQYt9moMf8Fpx5YVtBJN7TSjMlaecdahDGSAx94nhalYAmSZCOMma1eX4lSbf7wze3cyZBFeSYhN5jhPR1AjmViiecAt5DZBqlWwmZAz6Shm5I5ZBo0nqSgObSNmmPYGGLgQOpKc',phone_number_id='156388757567283')
# # For sending a Text messages
#               # Handle Webhook Subscriptions
#             messenger.send_message('Hello I am WhatsApp Cloud API', '60192585268')
#             data = request.get_json()
#             data = request.json()
#             logging.info("Received webhook data: %s", data)
#             changed_field = messenger.changed_field(data)
#             if changed_field == "messages":
#                 new_message = messenger.get_mobile(data)
#                 if new_message:
#                     mobile = messenger.get_mobile(data)
#                     name = messenger.get_name(data)
#                     message_type = messenger.get_message_type(data)
#                     logging.info(
#                         f"New Message; sender:{mobile} name:{name} type:{message_type}"
#                     )
#                     if message_type == "text":
#                         message = messenger.get_message(data)
#                         name = messenger.get_name(data)
#                         logging.info("Message: %s", message)
#                         messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

#                     elif message_type == "interactive":
#                         message_response = messenger.get_interactive_response(data)
#                         interactive_type = message_response.get("type")
#                         message_id = message_response[interactive_type]["id"]
#                         message_text = message_response[interactive_type]["title"]
#                         logging.info(f"Interactive Message; {message_id}: {message_text}")

#                     elif message_type == "location":
#                         message_location = messenger.get_location(data)
#                         message_latitude = message_location["latitude"]
#                         message_longitude = message_location["longitude"]
#                         logging.info("Location: %s, %s", message_latitude, message_longitude)

#                     elif message_type == "image":
#                         image = messenger.get_image(data)
#                         image_id, mime_type = image["id"], image["mime_type"]
#                         image_url = messenger.query_media_url(image_id)
#                         image_filename = messenger.download_media(image_url, mime_type)
#                         print(f"{mobile} sent image {image_filename}")
#                         logging.info(f"{mobile} sent image {image_filename}")

#                     elif message_type == "video":
#                         video = messenger.get_video(data)
#                         video_id, mime_type = video["id"], video["mime_type"]
#                         video_url = messenger.query_media_url(video_id)
#                         video_filename = messenger.download_media(video_url, mime_type)
#                         print(f"{mobile} sent video {video_filename}")
#                         logging.info(f"{mobile} sent video {video_filename}")

#                     elif message_type == "audio":
#                         audio = messenger.get_audio(data)
#                         audio_id, mime_type = audio["id"], audio["mime_type"]
#                         audio_url = messenger.query_media_url(audio_id)
#                         audio_filename = messenger.download_media(audio_url, mime_type)
#                         print(f"{mobile} sent audio {audio_filename}")
#                         logging.info(f"{mobile} sent audio {audio_filename}")

#                     elif message_type == "document":
#                         file = messenger.get_document(data)
#                         file_id, mime_type = file["id"], file["mime_type"]
#                         file_url = messenger.query_media_url(file_id)
#                         file_filename = messenger.download_media(file_url, mime_type)
#                         print(f"{mobile} sent file {file_filename}")
#                         logging.info(f"{mobile} sent file {file_filename}")
#                     else:
#                         print(f"{mobile} sent {message_type} ")
#                         print(data)
#                 else:
#                     delivery = messenger.get_delivery(data)
#                     if delivery:
#                         print(f"Message : {delivery}")
#                     else:
#                         print("No new message")
#             return "ok"

#         return app.make_respose(("valid response" , 200))
#     else:
#         return app.make_response(("valid response", 200))
    
#     return "project us working"

if __name__ == "__main__":
    app.debug = True
    app.run()