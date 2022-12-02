# Daily-news-email-sender
It is an email sender web application. Any one can add his email and subscribe us to can send to him the daily news in Egypt. User can also unsubscribe us if he doesn't need this feature any more.

## Content
* [Setup](#setup)
* [Usage](#usage)
* [Demo](#demo)
* [Author](#author)

## Setup
- make your virtual environment and activate it
- then download the project
```bash
https://github.com/ranawael1/Daily-news-email-sender.git
```
- install requirments 
```bash
pip insttall -r requirements.txt
```
- go to settings file: 
    - change the user and password for database
- makemigrations for the databases and then run the project
```bash
python3 manage.py makemigrations 
python3 manage.py migrate 
python3 manage.py runserver
```
- open another two terminals and activate the virtual environment
- run every command in a terminal 
```bash
celery -A sender_mail worker --loglevel=info
celery -A sender_mail beat -l info
```
These other terminals for the schedule jobs to send emails every day


## Usage
Once the project is all set go to url: https://localhost:8000/ or https://http://127.0.0.1:8000/



## Demo
[Screencast from 02 ديس, 2022 EET 09:07:52 م.webm](https://user-images.githubusercontent.com/42323978/205367924-85d34669-52e9-4811-9f36-29c29555ffad.webm)


## Author

- Created by 
  [@ranawael1](https://github.com/ranawael1)

