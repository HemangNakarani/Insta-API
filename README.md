# Insta-Api-Clone
- Attempt to clone some of functionalities of Instagram
- Frontend in React.js

## Tools and Tech.
- Python
- Django
- Django Rest Framework
- PostgreSQL Database
- Web Sockets
- Django Channels
- Redis Server
- Cronjob for Scheduling
- pip
- virtual env
- PyCharm

## Features
- User Management
- Post Management
- Request-Follow-Unfollow
- Like, Comment
- Chat
- Real time Notifications
- Story for 24 hours
- Archived Stories,Posts

## Development
- You should have PostgreSQL and Redis-Server running on your machine
  - For setting up Database and Password run
  ```
  psql -U postgres  -For Windows
  sudo -u postgres psql -For Linux

  postgres=# CREATE USER instagram WITH SUPERUSER CREATEDB CREATEROLE PASSWORD 'instagram';
  postgres=# CREATE DATABASE instagram OWNER instagram;
  ```
- Create Virtual Environment
- Install Following Dependencies using pip
  - django, pillow, channels, channels_redis, djangorestframework, python-decouple, psycopg2 or psycopg2-binary
- Configure Database, Username and Password in .env File
  - If you need to change server urls then you can change it in ```Instagram > settings.py``` file.
- Run following Commands
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## Debugging
- Chrome Browser
- Postman
- WebSocket King

## License
This project is licensed under the MIT License - Copyright (c) 2020 Hemang Nakarani
