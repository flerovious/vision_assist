# Raspberry Pi Zero 2 W Setup Instructions

## Preparing the Raspberry Pi

### 1. Install the Operating System
- Download the Raspberry Pi OS Lite (32-Bit, dated 2024-03-12, Bullseye version) from the official Raspberry Pi website.
- Use the Raspberry Pi Imager to flash the `2024-03-12-raspios-bullseye-armhf-lite.img.xz` image onto a microSD card.
- During the flashing process, set your WiFi credentials, and define the username and password for the device. Ensure SSH is enabled to facilitate remote access.

### 2. Connect the Camera Module
- Attach the Camera Module 3 (12.3 MP) to your Raspberry Pi Zero 2 W. Note that the default cable is for the Pi 4, so you will need a compatible ribbon cable. For example, a 30 cm Standard - Mini Raspberry Pi Camera Cable works well.

### 3. Power Up and Initial Configuration
- Insert the flashed microSD card into the Raspberry Pi Zero 2 W.
- Power the device using a 5000 mAh power bank with a 5V output.
- SSH into the device using a terminal on your computer.

## Setting Up the Project Environment

### 4. Prepare the Project Directory
- Create a new directory on your Raspberry Pi and navigate into it:
    ```
    mkdir myproject
    cd myproject
    ```

### 5. Set Up a Virtual Environment
- Establish a virtual environment that includes system site packages (necessary for the picamera2 package):
    ```bash
    python3 -m venv .venv --system-site-packages
    source .venv/bin/activate
    ```

### 6. Transfer Project Files
- Copy `main.py` and `requirements.txt` from the client directory in the repository to the project directory on your Raspberry Pi.

### 7. Install Dependencies
- Install the necessary packages to set up the FastAPI server:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

### 8. Launch the FastAPI Server
- Start the server by running:
    ```bash
    python main.py
    ```

### 9. Access the Server
- The FastAPI server should now be accessible at the Raspberry Pi's IP address on port 8000. For example, access the server at `http://192.168.10.108:8000/docs` to view the Swagger UI documentation.
