from django.urls import path
from .import views

app_name = 'superheroes'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:superhero_id>/', views.superhero_detail, name='superhero_detail'),
    path('superheroes/$', views.create, name='create_new_superhero'),
    path('superheroes/', views.delete_hero, name='delete_hero'),

]
