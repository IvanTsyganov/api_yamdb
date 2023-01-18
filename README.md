# YaMDb projecct
**This is a final project of API module, part of python-developer course
by yandex-practicum**

# НАПОМИНАЛКА. НЕ ЗАБУДЬ РАСКОММЕНТИТЬ В gitignore всё в абзаце django stuff

**Authors:**
- Dmitriy Merkulov
- Anton Ignatiev
- Ivan Tsyganov


We've prepared next features:

- Django project with custom models, views and urls

- REST API with CRUD functions

- JWT-Token Authentication

# How to start it:
1. fork this project
2. Open terminal and clone this repository:
```
git clone https://github.com/<your_git>/api_yamdb.git
```
2. create and start virtual environment(windows):
```
python -m venv venv
```
```
. venv/Scripts/activate
```
3. Install dependencies from requirements.txt
```
pip install -r requirements.txt
```
4. Make migrations:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
5. Start project:
```
python manage.py runserver
```

# How it works
(JWT-token getting example)

0. Download and install any app for sending requests (I prefer "Postman") and start project

<sub>(Next instruction was made for Postman)</sub>

1. Create workspace and paste this url http://127.0.0.1:8000/api/v1/users/
2. Below url open raw tab ```Body -> raw```
3. Write dict with keys "username" and "password" 
```
{
"username": "user",
"password": "password"
} 
```
4. Select type "post" and send request
5. If you made all right you will get http response with 201 status
6. Now send post request to http://127.0.0.1:8000/api/v1/jwt/create 
with same dict in raw
7. You will accept dict with "refresh" and "access" keys (lifetime =  1 day)
8. Go to "Headers"
9. Paste "Authorization" in "KEY" and "Bearer <your_access>" in "VALUE" variables
10. Congrats. You can send any request in other urls. See examples here:

- run server
```
 python manage.py runserver
```
- go to:
```
go to - http://127.0.0.1:8000/redoc.html
```