from twilio.rest import Client
import openai
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
from flask_cors import CORS, cross_origin

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

openai.api_key = "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"
# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC13f9ba608877232776f01dfda847b07f"
auth_token = "1cd36ab6c7cf94402a49301f4fd0a531"
client = Client(account_sid, auth_token)

responder="+18553896103"

received_messages = client.messages.list(
    to=responder  # Your Twilio trial number
)

prompt = "Act like a therapist: "

global oldMessage, firstLine
oldMessage, firstLine = ('hi', '15712440826'), 'abcdef'

def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt + text,
        max_tokens = 100
    )
    return response.choices[0].text

@app.route('/send_message', methods=['POST'])
def send_message():
    message_text = request.json.get('message')
    # Send the message using Twilio
    message = client.messages.create(
        body=message_text,
        to=oldMessage[1],
        from_=responder
    )
    return jsonify({"status": "success", "message": "Message sent successfully!"})

@app.route('/check_new_messages', methods=['GET'])
@cross_origin()
def check_new_messages():
    global oldMessage
    allNew = client.messages.list(to=responder)
    newMessage = (allNew[0].body, allNew[0].from_)
    if oldMessage != newMessage:
        recommendation = generate_response(newMessage[0])
        oldMessage = newMessage
        return jsonify({"new_message": newMessage[0], "prompt": recommendation})
    return jsonify({})

@app.route('/get_first_line', methods=['GET'])
def get_first_line():
    global firstLine
  # Update with the actual path to your file
    try:
        with open('output.txt', 'r') as file:
            first_line = file.readline().strip()  # Read the first line and remove leading/trailing whitespace
            if first_line != firstLine:
                recommendation = generate_response(first_line)
                firstLine = first_line
                print(first_line,recommendation)
                return jsonify({"first_line": first_line, "prompt": recommendation})
            else:
                jsonify({})
    except FileNotFoundError:
        return jsonify({"error": "File not found"})
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)




