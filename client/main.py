from fastapi import FastAPI
import uvicorn
from picamera2 import Picamera2
import io
import base64

# Initialize Pi Camera and start it
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.start()

app = FastAPI()


@app.get("/")
async def get_image():
    """Returns a base64 encoded image from an always-active Pi Camera."""
    # Autofocus before taking the picture
    try:
        picam2.autofocus_cycle()
    except Exception as e:
        print("Could not autofocus")

    # Capture the image to a BytesIO buffer
    data = io.BytesIO()
    picam2.capture_file(data, format="jpeg")

    # Reset stream position and encode the image
    data.seek(0)
    encoded_image = base64.b64encode(data.read()).decode("utf-8")

    return {"image": encoded_image}


@app.on_event("shutdown")
def shutdown_event():
    """Stops the camera when the FastAPI application is shutting down."""
    print("Stopping the camera")
    picam2.stop()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Server is up and running on port 8000.")
