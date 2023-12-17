from django.contrib import admin
from django.urls import path,include
from helpdesktool.views import frontpage

from helpdesktool.views import create_form,edit,delete_data,nothing,copy

urlpatterns = [

    path("frontpage", frontpage,name = "frontpage"),
    #path("a",registration),
    #control_idをintで取得して

    path("edit/<int:control_id>/" ,edit ,name = "edit"),

    path("copy/<int:control_id>" ,copy ,name ="copy"),

    path('create/', create_form, name='create'),

    #ここから
    path('delete/<int:control_id>',delete_data, name = 'delete'),

    path('nothing', nothing, name='nothing'),
]