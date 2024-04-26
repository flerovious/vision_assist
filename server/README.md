# Developer Environment
This codebase is developed using Python 3.11.9 on an M2 Mac. It has not been tested on other platforms.

## Requirements
- Python 3.11.9
- M2 Mac (recommended)

# Setup Instructions

## Prepare the Environment
1. Navigate to the server directory:
   ```
   cd server
   ```
2. Create and activate a virtual environment:
   ```
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configure Environment Variables
1. Create a `.env` file by referencing `.env.example`:
   - Obtain a valid OpenAI API key and update the `OPENAI_API_KEY` variable.
   - Determine the IP address of your Raspberry Pi Zero 2 W device. Set the `IMG_GET_URL` in the `.env` file, for example: `IMG_GET_URL=http://192.168.10.108:8000/`
   - Verify the IP address by accessing the FastAPI documentation at `http://192.168.10.108:8000/docs`. If the documentation is visible, the IP address is configured correctly.

## Running the Project
1. Launch the audio capture process:
   ```
   python capture.py
   ```
   This captures audio input from the default system microphone. Modify the device ID in the code to use a different microphone. Initialization may take a few seconds as model weights may need to download.
   
2. Start the watcher process:
   ```
   python watcher.py
   ```
   This monitors the `recordings` directory, activates the agent, and processes the audio files. Initial startup may be delayed while model weights are downloaded.
