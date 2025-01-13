from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('edit/', views.user_edit, name='user_edit'),
    path('leave/', views.leave, name='leave'),
]
