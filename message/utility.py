from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv
load_dotenv()






def compress_image(file, max_width=1024, max_height=1024):
    """
    Compresses an image without cropping.

    Parameters:
        file: FileStorage object or file-like object
            The image file to compress.
        max_width: int, optional
            The maximum width of the compressed image.
        max_height: int, optional
            The maximum height of the compressed image.

    Returns:
        bytes: The compressed image data.
    """
    # Open the image using PIL
    image_file = Image.open(file)
    image = image_file.convert('RGB')
    # Calculate the aspect ratio of the original image
    aspect_ratio = image.width / image.height

    # Calculate the new dimensions to fit within the maximum dimensions while preserving aspect ratio
    new_width = min(max_width, image.width)
    new_height = min(max_height, image.height)
    if aspect_ratio > 1:
        # Landscape orientation
        new_height = int(new_width / aspect_ratio)
    else:
        # Portrait or square orientation
        new_width = int(new_height * aspect_ratio)

    # Resize the image without cropping
    resized_image = image.resize((new_width, new_height))

    # Create a BytesIO object to store the compressed image
    compressed_image = BytesIO()

    # Save the compressed image to the BytesIO object
    resized_image.save(compressed_image, format='JPEG')

    # Get the compressed image data as bytes
    compressed_image_data = compressed_image.getvalue()

    return compressed_image_data





# Using AI GEN
def make_stamp(title):
    url = "https://animimagine-ai.p.rapidapi.com/generateImage"
    RAPID_API_KEY = os.getenv('RAPID_API_KEY') or os.environ["RAPID_API_KEY"]


    payload = {
        "selected_model_id": "anything-v5",
        "selected_model_bsize": "512",
        "prompt": title
    }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "animimagine-ai.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        stamp_url=response.json()["imageUrl"]
    # print(response.json())
    except:
        stamp_url="https://i.pinimg.com/originals/83/cd/ef/83cdef4f9b31d3aa9da285d1219a4d7b.jpg"

    return stamp_url
