import torch
import torchaudio
import sounddevice as sd
import numpy as np
from datetime import datetime
import os
import math
import soundfile as sf
import sys


class VoiceActivityDetector:
    def __init__(self, device="cpu"):
        # Load the Silero VAD model and utilities
        self.model, self.utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
        )
        (_, _, _, self.VADIterator, _) = self.utils

        # Instantiate the VADIterator
        self.vad_iterator = self.VADIterator(self.model)

        # Audio stream parameters
        self.original_sample_rate = 16000  # Default device sample rate
        self.target_sample_rate = 16000  # Required sample rate for the model
        self.channels = 1
        self.dtype = "float32"
        self.frame_size = 512  # This should ideally be aligned with the window size expected by the model

        # Setup resampler
        self.resampler = torchaudio.transforms.Resample(
            self.original_sample_rate, self.target_sample_rate
        )

        # Recording state
        self.recording = False
        self.recorded_frames = []
        self.device = device

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        # Convert the audio buffer to the format expected by the model and resample
        audio_np = np.array(indata[:, 0], dtype=np.float32)
        audio_tensor = torch.from_numpy(audio_np).to(device=self.device)
        # Resample the audio to the target sample rate
        resampled_audio = self.resampler(audio_tensor)

        # Use VAD to check for voice activity
        speech_dict = self.vad_iterator(resampled_audio, return_seconds=True)
        if speech_dict:
            print(speech_dict)
            if "start" in speech_dict:
                self.recorded_frames = []
                self.recording = True
                print(f"Start recording: {speech_dict}")
            if "end" in speech_dict:
                self.recording = False
                print(f"Stop recording: {speech_dict}")
                self.save_recording()
                self.recorded_frames = []

        if self.recording:
            self.recorded_frames.extend(resampled_audio.numpy())

    def save_recording(self):
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.wav")
        filepath = os.path.join(os.getcwd(), "recordings", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save the recording using soundfile
        sf.write(filepath, np.array(self.recorded_frames), self.target_sample_rate)
        print(f"Saved recording to {filename}")

    def run(self):
        with sd.InputStream(
            samplerate=self.original_sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            callback=self.callback,
            blocksize=self.frame_size
            * math.ceil(self.original_sample_rate / self.target_sample_rate),
            # device=1, # change this if you have a different audio input device
        ):
            print("Listening...")
            input(
                "Press Enter to stop..."
            )  # Keeps the stream alive until Enter is pressed

        # Reset the model states after processing
        self.vad_iterator.reset_states()


if __name__ == "__main__":
    # print all the available devices
    print(sd.query_devices())

    vad = VoiceActivityDetector()
    vad.run()
