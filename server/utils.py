from datetime import datetime
import requests
from typing import Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# URL of the FastAPI server running on the Raspberry Pi Zero 2 W.
# Change this to the IP address of your Raspberry Pi Zero 2 W.
IMG_GET_URL = os.getenv("IMG_GET_URL")
if not IMG_GET_URL:
    raise ValueError("IMG_GET_URL is not set in the environment")

client = OpenAI()


def fetch_image(url):
    # Send GET request to the FastAPI server running on the Raspberry Pi Zero 2 W
    response = requests.get(url)
    response.raise_for_status()  # Raises stored HTTPError, if one occurred

    # The response should be JSON with the image encoded in Base64
    data = response.json()
    image_base64 = data["image"]

    return image_base64


def get_transcription(path: str) -> Optional[str]:
    # Read the audio file from path and send it to OpenAI's API for transcription
    print(path)
    with open(path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file, model="whisper-1"
        )

        # Check if we got a transcription
        if not transcription:
            print("Did not get any transcription")
            return

    return transcription.text


def get_generated_audio(text: str) -> Optional[str]:
    # Generate audio from the text using OpenAI's API
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=text, response_format="wav"
    )

    # Check if we got an audio response
    if not response:
        print("Did not get any audio response")
        return

    # Save the audio response
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.wav")
    filedir = os.path.join(os.getcwd(), "generated_audio")
    os.makedirs(filedir, exist_ok=True)
    filepath = os.path.join(filedir, filename)
    response.write_to_file(filepath)

    return filepath
