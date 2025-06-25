from django.test import TestCase

# Create your tests here.
import os
import django
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectteam.settings')
django.setup()

application = WSGIHandler()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, application)
    print("Сервер запущен на http://127.0.0.1:8000/")
    server.serve_forever()