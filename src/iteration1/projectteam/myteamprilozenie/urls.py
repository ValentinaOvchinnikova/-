from django.urls import path
from . import views

app_name = 'myteamprilozenie'  # Добавляем пространство имен
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.home, name='home'),
# ]

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_patient, name='register_patient'),
    path('medical-history/', views.medical_history, name='medical_history'),
    path('result/<int:prediction_id>/', views.prediction_result, name='prediction_result'),
]