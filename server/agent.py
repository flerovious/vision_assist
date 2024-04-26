import base64
from io import BytesIO
from utils import fetch_image, IMG_GET_URL
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
import requests
from langchain_openai import ChatOpenAI
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
import os
from ultralytics import YOLO
from PIL import Image
from pytesseract import image_to_string


api_key = os.getenv("OPENAI_API_KEY")

# Load a pretrained YOLOv8 model
model = YOLO("yolov8n.pt")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


@tool
def describe_image():
    """Only use this if the user wants the description of what they see in front of them."""

    # Getting the base64 string representing the image from the camera
    base64_image = fetch_image(IMG_GET_URL)

    # Convert from base64 image to PIL image
    image = Image.open(BytesIO(base64.b64decode(base64_image)))

    # Perform object detection on the image
    results = model.predict(source=image)

    # Detected objects
    detected_objects = set([d["name"] for d in results[0].summary()])

    if detected_objects:
        return (
            f"The following objects are in front of you: {', '.join(detected_objects)}."
        )

    return "I'm sorry, I couldn't find any objects in front of you."


@tool
def describe_dangers():
    """Only use this if the user wants to know about immediate dangers in their environment."""

    # Getting the base64 string representing the image from the camera
    base64_image = fetch_image(IMG_GET_URL)

    # Load a pretrained YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Convert from base64 image to PIL image
    image = Image.open(BytesIO(base64.b64decode(base64_image)))

    # Perform object detection on the image
    results = model.predict(source=image)

    # Detected objects
    detected_objects = set([d["name"] for d in results[0].summary()])

    # Check for dangers
    dangers = [
        "bicycle",
        "car",
        "motorcycle",
        "bus",
        "train",
        "truck",
        "traffic light",
        "stop sign",
    ]

    if detected_objects.intersection(dangers):
        return f"The following dangers are present: {', '.join(detected_objects.intersection(dangers))}."

    return "You're safe."


@tool
def describe_location():
    """Only use this if the user wants to find out where they are."""

    # Getting the base64 string representing the image from the camera
    base64_image = fetch_image(IMG_GET_URL)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give a short description of where the blind person could be based on what they might see.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return response.json()["choices"][0]["message"]["content"]


@tool
def read_text():
    """Only use this to read text from an image."""

    # Getting the base64 string representing the image from the camera
    base64_image = fetch_image(IMG_GET_URL)

    # Convert from base64 image to PIL image
    image = Image.open(BytesIO(base64.b64decode(base64_image)))

    # Perform optical character recognition on the image
    text = image_to_string(image)

    # Clean out newlines and extra spaces
    if not text:
        text = ""
    text = " ".join(text.split())

    return text


tools = [describe_image, describe_dangers, describe_location, read_text]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Keep your responses concise and informative.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Custom agent
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)


agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # print debug information
    max_iterations=2,  # maximum number of iterations
    max_execution_time=30,  # timeout in seconds
)
