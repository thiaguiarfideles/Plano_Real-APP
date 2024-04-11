from django.contrib import admin
from django.urls import path
from todolist import views

urlpatterns = [
       #Todolist
    path('', views.hometodo, name='home_todo'),
    path('createtodolist/',views.createtodolist, name='createtodolist'),
    path('currenttodolist/',views.currenttodolist, name='currenttodolist'),
    path('completedtodolist/',views.completedtodolist,name='completedtodolist'),
    path('todolist/<int:todolist_pk>',views.displaytodolist,name='displaytodolist'),
    path('todolist/<int:todolist_pk>/completetodolist',views.completetodolist, name='completetodolist'),
    path('todolist/<int:todolist_pk>/deletetodolist',views.deletetodolist,name='deletetodolist'),
]