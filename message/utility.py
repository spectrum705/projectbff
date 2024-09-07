from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv
import time
load_dotenv()
import base64
import requests
from threading import Thread
import queue
import base64
from message.security import encrypt_file_chunked
from message import Tasks
from dotenv import load_dotenv
load_dotenv()
   



           
def send_to_queue(task):
    endpoint = os.getenv('ConsumerAPI') or os.environ["ConsumerAPI"]
    currentUrl = os.getenv('CurrentUrl') or os.environ["CurrentUrl"] 
    callbackUrl = os.getenv('CallbackUrl') or os.environ["CallbackUrl"] 
    QSTASH_TOKEN =  os.getenv('QSTASH_TOKEN') or os.environ["QSTASH_TOKEN"] 
    
    headers = {
    'Authorization': f'Bearer {QSTASH_TOKEN}',
    'Content-Type': 'application/json',
    'Upstash-Method': 'POST',
    'Upstash-Delay': '5s',
    'Upstash-Retries': '3',
    'Upstash-Forward-Custom-Header': 'custom-value',
    'callback': currentUrl+"/process",
    'Upstash-Failure-Callback'   : callbackUrl+ "/process"
    
    }

    # try:
    response = requests.post(
    f'https://qstash.upstash.io/v2/publish/{endpoint}/process',
    headers=headers,
    json=task
    )
    

    # print("Message produced without Avro schema!")
    # print("sent to Qstash:",response)
        
    # except Exception as e:
    #     print(f"Error producing message: {e}")
    return True

def process_attached_links(content):
    # List of known URL schemes to check
    url_schemes = ["http://", "https://", "www."]
    
    # Split the content into paragraphs
    paragraphs = content.split("\n")
    paragraphs = [x for x in paragraphs if x not in [""," ","\r"]]           
    
    # Initialize lists for links and normal paragraphs
    links = []
    normal_paragraphs = []

    # Iterate through each paragraph
    for para in paragraphs:
        # Split the paragraph into words
        words = para.split()
        
        # Initialize a temporary list for non-link words
        non_link_words = []
        
        # Check each word to see if it's a link
        for word in words:
            if any(word.startswith(scheme) for scheme in url_schemes):
                links.append(word)  # If a link, add to the links list
            else:
                non_link_words.append(word)  # Otherwise, keep it as part of the normal paragraph
        
        # Rebuild the paragraph from non-link words
        if non_link_words:
            normal_paragraphs.append(" ".join(non_link_words))
    
    return normal_paragraphs, links

def process_links(content):
    # List of known URL schemes to check
    url_schemes = ["http://", "https://", "www."]
    
    # Split the content into words
    words = content.split()
    
    # Initialize lists for links and non-link content
    links = []
    non_link_content = []

    # Iterate through each word to check if it's a link
    for word in words:
        if any(word.startswith(scheme) for scheme in url_schemes):
            links.append(word)
        else:
            non_link_content.append(word)

    # Reconstruct the content without links
    content_without_links = ' '.join(non_link_content)

    # Add the links at the end under a "Links" label if any were found
    if links:
        content_without_links += "\n\nLINKS:\n" + "\n".join(links)
    
    return content_without_links

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
    if type(file) is bytes:
        file = BytesIO(file)
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




def attach_images(image_data_list,content, key):
    print("IMAGE FUNC STARTED")

    
    
    final_image_list = []
    print("ATTACH-IMAGA-DATA:",image_data_list,type(image_data_list))
    for file in image_data_list:
    
        print("file type",type(file))
        # filename = secure_filename(file.filename)
        # print("filename", filename)
    
        img=compress_image(file)               
        enc_img=encrypt_file_chunked(img,key)
    
        # print("ENC IMAGE",type(enc_img))
        encoded_image = base64.b64encode(enc_img).decode('utf-8')
        final_image_list.append(encoded_image)
    content["attached"] = True
    content["image_data_list"] = final_image_list
    
    # send_to_queue(content)
    print("ÏMAGES SENT TO QUEUE!!! ")
    return True


def make_letter_json(title, content, author,key, receiver, timestamp):

        enc_content_base64 = base64.b64encode(content).decode('utf-8')
        encrypt_symmetric_key_base64 = base64.b64encode(key).decode('utf-8')
        url=os.getenv('ConsumerAPI') or os.environ["ConsumerAPI"]
        

        content={
            "task_name":Tasks.make_letter.value,
            # print("2. symmentric key used on letter for enc:", symmetric_key)
            "letter_title":title,
            # content=form.content.data
            "enc_content" :enc_content_base64,#encrypt_message_chunked( form.content.data, symmetric_key),

            "encrypted_symmetric_key":encrypt_symmetric_key_base64 ,#encrypt_symmetric_key(symmetric_key, recipient_public_key),
            "author":author ,
            "receiver":receiver,
            "timestamp":str(timestamp),
            "url": url+"/process",
            "attached":False,


    }
        return content








# Using AI GEN
def make_stamp(title):
   
    url = "https://animimagine-ai.p.rapidapi.com/generateImage"
    RAPID_API_KEY = os.getenv('RAPID_API_KEY') or os.environ["RAPID_API_KEY"]


    payload = {
        "selected_model_id": "anything-v5",
        "selected_model_bsize": "512",
        "prompt": "create an beautiful art for the following title: "+title
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
    except:
        stamp_url="https://i.pinimg.com/originals/83/cd/ef/83cdef4f9b31d3aa9da285d1219a4d7b.jpg"

    response = requests.get(stamp_url)
    img = response.content    

    return img




def compress_images(image_data_list, compressed_queue):
    
    compressed_images = []
    print("IMAGE COMPRESSION STARTED")
    for file in image_data_list:
        img = compress_image(file)
        compressed_images.append(img)
    compressed_queue.put(compressed_images)

def encrypt_images(compressed_queue, encrypted_queue, symmetric_key):
    compressed_images = compressed_queue.get()
    encrypted_images = []
    print("IMAGE ENC STARTED")
    
    for img in compressed_images:
        enc_img = encrypt_file_chunked(img, symmetric_key)
        encrypted_images.append(enc_img)
    encrypted_queue.put(encrypted_images)

def queue_images(encrypted_queue, content):
    encrypted_images = encrypted_queue.get()
    # image_task = {
    #     "task_name": "ADD_IMAGES",
    #     "letter_id": letter_id,
    # }
    
    final_image_list = []
    for img in encrypted_images:
        encoded_image = base64.b64encode(img).decode('utf-8')
        final_image_list.append(encoded_image)
    content["attached"] = True
    content["image_data_list"] = final_image_list
    send_to_queue(content)
    
    print("Images sent to the queue")

def process_images(letter_content, image_data_list, symmetric_key):
    compressed_queue =  queue.Queue()
    encrypted_queue =  queue.Queue()
    print("MAIN IMG TASK STARTED")
    
    # Compression in a separate thread
    t1 = Thread(target=compress_images, args=(image_data_list, compressed_queue))
    t1.start()
    
  
    p1 = Thread(target=encrypt_images, args=(compressed_queue, encrypted_queue, symmetric_key))
    p1.start()
    
    # Queueing in the main thread
    queue_images(encrypted_queue, letter_content)
        

    