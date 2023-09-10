import websockets
import asyncio
import base64
import json
from configure import auth_key
import sounddevice as sd
import pyaudio
import keyboard
from twilio.rest import Client
import openai
import pyttsx3
import time

openai.api_key = "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"
# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC13f9ba608877232776f01dfda847b07f"
auth_token = "1cd36ab6c7cf94402a49301f4fd0a531"
client = Client(account_sid, auth_token)

sendToTwillo = []
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

system_audio_device_index = 1

prompt = "Act like a therapist: "


def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt + text,
        max_tokens = 100
    )
    return response.choices[0].text


# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

out = open("output.txt", 'w')
out.close()

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_receive():
    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
            URL,
            extra_headers=(("Authorization", auth_key),),
            ping_interval=5,
            ping_timeout=20
    ) as _ws:

        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while True:
                try:
                    # Check if the space bar is pressed

                    if not keyboard.is_pressed('space'):
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    print('1')
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

                await asyncio.sleep(0.01)

            return True

        async def receive():
            engine = pyttsx3.init()
            while True:
                try:
                    result_str = await _ws.recv()
                    boy = json.loads(result_str)['text']


                    if '.' in boy:
                        gptresponse = generate_response(boy)

                        print("You: " + boy)
                        print("Responder: " + gptresponse.strip())
                        #engine.say(gptresponse)
                        #engine.runAndWait()


                        with open('output.txt', 'w') as file:  # PLACEHOLDER FOR WEBSOCKET
                            file.write(boy)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    print('3')
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())


while True:
    asyncio.run(send_receive())
