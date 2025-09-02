from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_blog, name='create'),
    path('<int:pk>/', views.view_blog, name='view_blog'),
    path('add-comment/blogs/<int:pk>', views.add_comment, name='add_comment'),
    path('list-blogs/<int:pk>/', views.view_user_all, name='view_user_all'),
]
