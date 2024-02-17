# projectbff

Welcome to Project BFF, your personal space for staying connected with your best friends. Project BFF allows you to send and receive heartfelt letters to and from your selected partners, providing a secure and enjoyable way to maintain your most cherished relationships.


## Features

### 1. Secure Messaging

Project BFF ensures the privacy of your messages by securely encrypting the contents. Your letters are protected, making them accessible only to the intended recipient, ensuring a confidential and intimate communication experience.

### 2. Draft Saving

Life is busy, and sometimes you need to pause and come back to complete your thoughts. Project BFF automatically saves your messages as drafts, allowing you to pick up right where you left off. No need to worry about losing your heartfelt words.

### 3. Optimized Reading Experience

Project BFF provides a delightful reading experience for both senders and receivers. The user interface is thoughtfully designed to enhance the joy of reading and sharing letters, creating a unique and personalized experience.

### 4. Image Attachment

Enhance your communication by attaching images to your letters. Whether it's capturing a special moment or sharing a memorable photograph, Project BFF allows you to enrich your messages with visual content. Share your experiences more vividly and add a personal touch to your letters with image attachments. Enjoy seamless integration and effortless sharing of images to deepen your connections with your friends.

### 5. Mobile-Friendly Progressive Web App (PWA)

Take Project BFF with you wherever you go! Our mobile-friendly Progressive Web App ensures that you can access your letters conveniently from your mobile device. Enjoy the same great features on the go as you do on your desktop.



## Demo
[ProjectBff](https://tinyurl.com/projectbffs)
Two demo Accounts with the following credentials have been created so you can test it out if you want.
```bash
username: alpha
password: test1234
```
```bash
username: beta
password: test1234
```


## Local Development
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
## Environment Variables

create a .env file inside message/ and add the following variables
```bash
    DB_URI=""
    account_sid=""
    auth_token=""
    messaging_service_sid=""
    APP_SECRET=""

```

## Screenshots
![home page](/home.png)
![write Page](/write.png)
![Letter Page](/letter.png)
![gallery Page](/gallery.png)
![Encryption steps](/enc.png)


## Contributing

Project BFF is an open-source project and I don't think I can take care or it all, so we welcome contributions from the community. Feel free to submit bug reports, feature requests, or even pull requests to help improve the project for everyone.

## Support

If you have any questions, encounter issues, or just want to share your feedback, please send a feedback using the site.

Thank you for choosing Project BFF. Strengthen your friendships, one letter at a time! 💌🌟
[You need to add a Spacefile before deployment ](https://deta.space/docs/en/reference/spacefile)