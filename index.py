from flask import Flask, request
import os
import json 
import requests
from heyoo import WhatsApp

secret_token = "EAAFvPm54i34BO9R3GIaR0B5y4aaklyOHJ7abuZCIRDQmvg9hRk41WcZAUAaI1t1pLWIAJb2WymE5nduKQYt9moMf8Fpx5YVtBJN7TSjMlaecdahDGSAx94nhalYAmSZCOMma1eX4lSbf7wze3cyZBFeSYhN5jhPR1AjmViiecAt5DZBqlWwmZAz6Shm5I5ZBo0nqSgObSNmmPYGGLgQOpKc"
os.environ.get("secret.config")
app = Flask(__name__)

@app.route("/")
def func():
    return "project is working"

@app.route("/messages", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("Received data:", json.dumps(data, indent=2))

    # Extracting relevant information from the incoming message
    sender_phone = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    message_text = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]

    # Perform any processing or respond to the message as needed
    # For example, you can use the WhatsApp API to send a response
    messenger = WhatsApp('EAAFvPm54i34BO9R3GIaR0B5y4aaklyOHJ7abuZCIRDQmvg9hRk41WcZAUAaI1t1pLWIAJb2WymE5nduKQYt9moMf8Fpx5YVtBJN7TSjMlaecdahDGSAx94nhalYAmSZCOMma1eX4lSbf7wze3cyZBFeSYhN5jhPR1AjmViiecAt5DZBqlWwmZAz6Shm5I5ZBo0nqSgObSNmmPYGGLgQOpKc', phone_number_id='156388757567283')
    messenger.send_message(f"Received your message: {message_text}", sender_phone)

    return "Message received", 200

@app.route("/messages" , methods = ["POST" , "GET"])
def message():
    if request.method == "GET":
        sent_token = str(request.args.get("hub.verify _token")).split(" ")[0]
        print (sent_token , "/n" , secret_token) 
        # if sent_token != secret_token:
        #     return app.make_response((f"forbidden token {sent_token} ans {secret_token}", 403)) 
        # if request.args.get("hub.mode") != "subscribe":
        #     return app.make_response(("forbidden mode", 403))

        res = request.args.get("hub.challenge")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify _token")
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == "mytestingtoken":
                print("WEBHOOK_VERIFIED")
                return app.make_response((str(res) , 200))
            else:
                return app.make_response((str(res) , 403))
        else:    
            # url = "https://graph.facebook.com/v18.0/156388757567283/messages"
            # header = {'Content-type': 'application/json', 'Authorization': 'Bearer '+ str(secret_token)}
            # char = request.json
            # phone = char ["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            # ans = "hey , how u doin"
            # data = {
            #     "messaging product": "whatsapp",
            #     "to": 60192585268,
            #     "type": "text", 
            #     "text": {
            #         "body": ans}}
            # answer = requests.post(url, headers=header, data=json.dumps(data))
            messenger = WhatsApp('EAAFvPm54i34BO9R3GIaR0B5y4aaklyOHJ7abuZCIRDQmvg9hRk41WcZAUAaI1t1pLWIAJb2WymE5nduKQYt9moMf8Fpx5YVtBJN7TSjMlaecdahDGSAx94nhalYAmSZCOMma1eX4lSbf7wze3cyZBFeSYhN5jhPR1AjmViiecAt5DZBqlWwmZAz6Shm5I5ZBo0nqSgObSNmmPYGGLgQOpKc',phone_number_id='156388757567283')
# For sending a Text messages
            messenger.send_message('Hello I am WhatsApp Cloud API', '60192585268')

        return app.make_respose(("valid response" , 200))
    else:
        return app.make_response(("valid response", 200))
    
    return "project us working"

if __name__ == "__main__":
    app.debug = True
    app.run()