from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
path('user-info/<int:user_id>',views.user_info,name='user_info'),
path('contact/',views.contact,name='contact'),
path('register/',views.register,name='register'),
path('profile/',views.profile,name='profile'),
path('search_admin/',views.search_admin,name='search_admin'),
path('create-article/',views.create_article,name='create_article'),
path('update-article/<int:single_id>/',views.update_article,name='update_article'),
path('delete-article/<int:single_id>/',views.delete_article,name='delete_article'),
path('<uidb64>/<token>/',views.activate,name='activate')


]