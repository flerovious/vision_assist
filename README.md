# VisionAssist: System Overview
![vision-assist-device](https://github.com/user-attachments/assets/3ed2a1e6-11ea-4756-94cc-e872ecac49f6)

**VisionAssist** is an innovative, affordable assistive wearable device tailored for the visually impaired. It offers functionality comparable to advanced systems like Google Glass but focuses on accessibility and affordability, leveraging the Raspberry Pi Zero and its camera module. See the setup instructions secttion below to get started with VisionAssist.

## Key Features

- **Voice-Activated Interaction:** Users can operate VisionAssist using voice commands, which are processed and responded to audibly.
- **Real-Time Object and Text Recognition:** Using cutting-edge machine learning algorithms, the device identifies and verbalizes objects and text in the environment.
- **Hazard Detection and Location Awareness:** The system alerts users to potential dangers and provides positional feedback to enhance navigation safety.

## System Components
![system-overview](https://github.com/user-attachments/assets/d29d4619-dd6f-4f47-bd90-fc83acdf9072)

- **Voice Activity Detection (VAD):** Differentiates between speech and other sounds to enable efficient voice command processing.
- **Audio Processing and Management:** Manages the lifecycle of audio files from capture to processing.
- **Command Processing and Execution:** Utilizes OpenAI's Whisper model for transcription and GPT-3.5-turbo for command understanding.
- **Tool Invocation:** Employs various models such as YoloV8, Tesseract OCR and GPT-4-vision for tasks like environmental description and text reading through LangChain Agents.
- **Image Capture and Processing:** Captures and processes images for object recognition and environmental understanding.
- **Audio Feedback Generation:** Converts text responses into speech, providing real-time auditory feedback to the user.

## Hardware
![hardware](https://github.com/user-attachments/assets/e481f421-dafc-4fc1-97e0-c4d168ddc83b)

- **Raspberry Pi Zero 2 W:** The core of the embedded device.
- **Raspberry Pi Camera Module 3:** Captures high-quality images for processing.
- **Raspberry Pi Zero 15-pin Camera FFC Cable (30cm):** Connects the camera to the Raspberry Pi Zero.

## Setup Instructions

- **Raspberry Pi Zero Setup:** For configuring the Raspberry Pi Zero, refer to the `client` folder which includes detailed instructions for setting up the hardware and software on the device.
- **Server Setup:** For server configuration on your computer or laptop, refer to the `server` folder which contains all necessary setup details to get the system up and running.
