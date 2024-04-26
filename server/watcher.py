from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from datetime import datetime

import wave
import numpy as np
import sounddevice as sd

from utils import get_generated_audio, get_transcription
from agent import agent_executor
import os


class FileCreationHandler(FileSystemEventHandler):
    """Handles the event of new file creations."""

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file created: {event.src_path}")

        if not event.src_path.endswith(".wav"):
            print("Ignoring non-WAV file")
            return

        # Get transcript with OpenAI Whisper and print it
        user_text = get_transcription(event.src_path)

        if not user_text:
            print("Did not get any transcription")
            return

        print(f"[User]: {user_text}")

        # Invoke the agent
        agent_reply = agent_executor.invoke({"input": user_text})

        # Check that the agent has an output
        if "output" not in agent_reply:
            print("Agent did not return any output")
            return

        # Print the agent's reply
        agent_reply_text = agent_reply["output"]
        print(f"[Agent]: {agent_reply_text}")

        # Generate audio response
        generated_audio_path = get_generated_audio(agent_reply_text)

        # Open the file for reading
        with wave.open(generated_audio_path, "rb") as file:
            fs = file.getframerate()
            # get the numpy array of the audio file
            audio = np.frombuffer(file.readframes(file.getnframes()), dtype=np.int16)

            # print(f"Sampling frequency: {fs} Hz")
            # print(f"Audio length: {len(audio)/fs} seconds")

            # play the audio
            sd.play(
                audio,
                fs,
                device=0,  # specify the device to use based on the sd.device
            )

            # Wait for the audio to finish playing
            sd.wait()

        print("Agent responded")


def start_monitoring(path):
    """Monitors the recordings directory for new files."""
    event_handler = FileCreationHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    directory_to_watch = os.path.join(os.getcwd(), "recordings")
    print(f"Monitoring directory: {directory_to_watch}")
    start_monitoring(directory_to_watch)
