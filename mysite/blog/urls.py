from django.urls import path
from . import views

app_name = 'blog'  # Добавьте эту строку!

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
]