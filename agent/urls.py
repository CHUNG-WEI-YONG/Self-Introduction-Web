from django.urls import path
from . import views

app_name='agent'

urlpatterns=[
    path('chat/',views.chat_api_view,name='chat_api')
]