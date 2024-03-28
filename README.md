# projectbff

Welcome to Project BFF, your personal space for staying connected with your best friends. It allows you to send and receive heartfelt letters to and from your selected friends, providing a secure and enjoyable way to maintain your most cherished bonds.


## Features

### 1. Secure Messaging 🔒🔑

Project BFF ensures the privacy of your messages by securely encrypting the contents. Your letters are protected, making them accessible only to the intended recipient, ensuring a confidential and closest communication experience. 

### 2. Draft Saving  🧙🏽‍♂️

Life is busy, and sometimes you need to pause and come back to complete your thoughts. Project BFF automatically saves your messages as drafts, allowing you to pick up right where you left off. No need to worry about losing your heartfelt words. Take your time to pour out your feelings into words. Project BFF allows you to save your reading and writing progress, so you can continue where you left off. Whether you're composing a heartfelt letter or savoring a thoughtful message, your progress is safely stored, giving you the flexibility to express yourself at your own pace.

### 3. Optimized Reading Experience 📃

Project BFF provides a delightful reading experience for both senders and receivers. The user interface is thoughtfully designed to enhance the joy of reading and sharing letters, creating a unique and personalized experience.

### 4. Image Attachment 📸

Enhance your communication by attaching images to your letters. Whether it's capturing a special moment or sharing a memorable photograph, Project BFF allows you to enrich your messages with visual content. Share your experiences more vividly and add a personal touch to your letters with image attachments. Enjoy seamless integration and effortless sharing of images to deepen your connections with your friends.

### 5. Mobile-Friendly Progressive Web App (PWA) 📱

Take Project BFF with you wherever you go! Our mobile-friendly Progressive Web App ensures that you can access your letters conveniently from your mobile device. Enjoy the same great features on the go as you do on your desktop.



## Demo
[ProjectBff](https://projectbff.onrender.com/)
Two demo Accounts with the following credentials have been created so you can test it out if you want.
```bash
username: alpha
password: test1234
```
```bash
username: beta
password: test1234
```


## Technical Details  and Local Development
1. **Installation:**

- Clone the repository: 
```bash 
git clone https://github.com/spectrum705/projectbff.git
```
- Navigate to the project directory: 
```bash
cd projectbff
```  
2. **Setup:**
go to project directory
```bash
cd projectbff
```

create a new branch 
```bash 
git branch dev
git checkout dev
```

install requirements
```bash
pip3 install -r requirements.txt 
```


3. **Run the application:**

Running the server
```bash
python3 main.py
```



4. **The consumer instance needs to be run separately :**

Running the consumer processing
```bash
cd consumer
python3 consumer.py
```
## Environment Variables

create a .env file inside message/ and add the following variables
```bash
    DB_URI=""
    account_sid=""
    auth_token=""
    messaging_service_sid=""
    APP_SECRET=""
    MORE TO ADD

```

## Working of the Project
The project is built with simple html and css and certain parts of the project has javascript added to it. The main part, the backend is  built using Flask in python. We are are MongoDB a NoSQL database for safely storing the data. We are using QStash as task queue.
During letter generation the flask backend gets user input, encrypts the letter data(Yes, even the images). The letter is encrypted using the a Unique letter key, which can used only by the intended receiver.In case the user attaches images as well, the image file is validate, the image data is compressed and then encrypted.


##### LETTER OBJECT
```
Letters(            
            letter_id,
            title,
            content,
            symmetric_key,
            author,
            receiver,
            status,
            timestamp, 
            stamp_data,
        )
```

All the required details of the letter are then used to form a json object, Which is then sent to the the QStash using it's API. 
The letter data is stored there for sometime and then safely delivered to the Consumer endpoint which is deployed separtely at another instance. At the consumer side, we Authenticate the data received using the JSON Web Token(JWT). When a request is validated, we process the task according to the task.

The point of using message queue was to reduce the time taken to process the request. There are various external APIs being used at the back, using the QStash to process the tasks at the back, helps save time and user can be freed As soon as we have gather all the gathered all the required user inputs.

Later when the receiver of the letter reads the new letter, the content is decripted using their private key. Only the reciver can read the content. 



## External APIs Used
##### Twillio - for SMS [Link](https://www.twilio.com/en-us)
##### MongoBD - for database [Link](https://www.mongodb.com/atlas/database)
##### AnimImagine AI API - Used for stamp generation [Link](https://rapidapi.com/serhaterfidan/api/animimagine-ai)
##### Upstash QStash  -  For Using the QStash as message Queue. [Link](https://upstash.com/)


## Screenshots
### Home page
![home page](/home.png)
### Writing page
![write Page](/write.png)
### Letter page
![Letter Page](/letter.png)
### Gallery view
![gallery Page](/gallery.png)
### Ecncryption Steps
![Encryption steps](/enc.png)
### Application Structure
![Application structure](/structure.png)




## Contributing

Project BFF is an open-source project and I don't think I can take care of it all, so we welcome contributions from the community. Feel free to submit bug reports, feature requests, or even pull requests to help improve the project for everyone.

## Support

<a href="https://www.buymeacoffee.com/spectrum93"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=spectrum93&button_colour=5F7FFF&font_colour=ffffff&font_family=Poppins&outline_colour=000000&coffee_colour=FFDD00" /></a>


Life goes on and sometimes people lose touch with each other. I never want to lose any of the precious friends I cherish and I don't want anyone else to get distant with your cherished friends either. This is a small way, to create a connection that can exist just between you and the people you cherish. If you support the initiative and sentiments or If you like the work and if you had a happy experience using it feel free to donate or support it any way (remember it's completely optional). It'd sure make me smile. I'm grateful for any of your support.

If you have any questions, encounter issues, or just want to share your feedback, please send a feedback using the site's feedback page.
Thank you for using Project BFF. Strengthen your friendships, one letter at a time! 💌🌟




