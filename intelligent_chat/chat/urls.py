from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('process/', views.process_chat_input, name='process_chat_input'),
    path('api/feedback/', views.provide_feedback, name='provide_feedback'),
    path('api/stats/<str:session_id>/', views.get_session_stats, name='get_session_stats'),
]
