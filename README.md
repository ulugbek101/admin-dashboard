# CMS platform mainly focused to manage Study centers and Private schools 

## Create virtual environment
- Windows
```python
python -m venv venv
```

- MacOS
```python
python3 -m venv venv
```

## Install dependencies
```python
pip install -r requirements.txt
```

## Setup environment variables
```
CLOUD_NAME=YOUR_CLOUDINARY_NAME
API_KEY=YOUR_CLOUDINARY_API_KEY
API_SECRET=YOUR_CLOUDINARY_API_SECRET

DJANGO_SECRET_KEY=DJANGO_SECRET

DB_NAME=DATEBASE_NAME
DB_USER=DATABASE_USER
DB_PASSWORD=DATABASE_PASSWORD
DB_PORT=DATABASE_PORT
DB_HOST=DATABASE_HOST

ESKIZ_EMAIL=YOUR_ESKIZ_EMAIL
ESKIZ_PASSWORD=YOUR_ESKIZ_SECRET_PASSWORD
```

## Create and make migrations
```python
python manage.py makemigrations
python manage.py migrate
```

## Run development server
```python
python manage.py runserver
```

Add superuser and some DUMMY data make it look like this 👇

Website has 2 color schemes:
- Dark
- Light

<img width="1417" alt="Screenshot 2024-03-22 at 15 05 57" src="https://github.com/ulugbek101/admin-dashboard/assets/94630185/a55e7238-931b-4264-a229-eea6d42765d8">
<img width="1400" alt="Screenshot 2024-03-22 at 15 07 03" src="https://github.com/ulugbek101/admin-dashboard/assets/94630185/e3babea5-88c6-46ee-8981-e26d50f5bce7">
