from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns=[
path('',views.blog,name='index'),
path('blog/<int:single_id>',views.single,name='single'),
path('search/',views.search,name='search'),
path('preview/<int:single_id>',views.preview,name='preview'),

]
