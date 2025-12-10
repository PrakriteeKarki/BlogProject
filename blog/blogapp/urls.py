from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
   path('dashboard/',views.dashboard,name="dashboard"),
   path('create_post/',views.create_post,name="create_post"),
   path('display_post/',views.display_post,name="display_post"),
   path('home/',views.home,name='home'),
   path('register/',views.register,name='register'),
   path('login/',views.login,name='login'),
   path('profile/',views.profile,name="profile"),
   path('delete_post/<int:id>/',views.delete_post,name='delete_post'),
   path('edit_post/<int:id>/',views.edit_post,name='edit_post'),
   path('logout/',views.login,name='logout'),
   path('like_post/<int:id>/',views.like_post,name="like_post"),
   path('like/<int:id>/',views.like_post,name="like_post"),
   path('feed/',views.feed,name='feed'),
   path('add_comment/<int:id>/',views.add_comment,name="add_comment"),
   path('add_comment_page/<int:id>/',views.add_comment_page,name="add_comment_page"),
]
