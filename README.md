# YaMDd projecct
This is a final project of API module, part of python-developer course
by yandex-practicum

## Authors:
- Dmitriy Merkulov
- Anton Ignatiev
- Ivan Tsyganov

## Description 
We've prepared next features:

- Django project YaMDb keeps reviews by users on many titles of:
  - books
  - films
  - music

  You cal also give rating for all of them from 1 to 10 score 
  or make a comment for any review from another user.

  All titles are divided in many categories and genres.


- REST API with CRUD functions

- JWT-Token Authentication

## Technical issue

This project contains next roles:

- Anon - can only read reviews, comments and titles descriptions.
- User - All authorised users. Like Anon but also can publish reviews, give rates scores for all titles.
- Moderator - Like User but he/she can also delete any reviews and comments.
- Admin - everything you want, bro.
- Django superuser - like Admin.

## ReDoc

http://127.0.0.1:8000/redoc.html  

## How to start it:
1. fork this project
2. Open terminal and clone this repository:
```
(bash) git clone https://github.com/<your_git>/api_yamdb.git
```
3. create and start virtual environment(windows):
```
python -m venv venv
```
```
. venv/Scripts/activate
```
4. Install dependencies from requirements.txt
```
pip install -r requirements.txt
```
5. Make migrations:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
6. Start project:
```
python manage.py runserver
```

## How it works
(registration and JWT-token getting example)

0. Download and install any app for sending requests (I prefer "Postman") and start project

<sub>(Next instruction was made for Postman)</sub>

1. Create workspace and Paste this url /api/v1/auth/signup/
2. Below url open raw tab ```Body -> raw```
3. Write dict with keys "username" and "password" 
```
{
"email": "email",
"username": "user"
} 
```
5. You'll get on email confirmation_code. Use it for getting JWT-token
6. Paste this url http://127.0.0.1:8000/api/v1/auth/token/ and write this dict in raw
```
{
"username": "user",
"confirmation_code": "code from email"
} 
```
7. Select type "post" and send request
8. If you made all right you will get http response with 201 status and JWT-token
9. Now send any response with this token (paste in Bearer)


- run server
```
 python manage.py runserver
```
- go to:
```
go to - http://127.0.0.1:8000/redoc.html
```