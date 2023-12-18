# projectbff



Hi, This is  the projectbff Code base


## Deployed Link


[ProjectBff](https://tinyurl.com/projectbffs)



## Local Development
```bash
git clone https://github.com/spectrum705/projectbff.git
```
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

[You need to add a Spacefile before deployment ](https://deta.space/docs/en/reference/spacefile)