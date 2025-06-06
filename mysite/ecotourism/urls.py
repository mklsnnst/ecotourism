from django.urls import path
from . import views

app_name = 'ecotourism'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('add_tour/', views.add_tour, name='add_tour'),
    path('tour/<int:tour_id>/edit/', views.edit_tour, name='edit_tour'),
    path('tour/<int:tour_id>/delete/', views.delete_tour, name='delete_tour'),
]