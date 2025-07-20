from django.urls import path
from blog.views import *
from rest_framework.urlpatterns import format_suffix_patterns
app_name="blog"

urlpatterns = [
  
    path('',blog_view,name='index'),
    path('<int:pid>/',blog_single,name='single'),
    path('category/<str:cat_name>/',blog_view,name='category'),
    path('author/<str:author_username>/',blog_writer,name='writer'),
    path('posts/',Post_great.as_view(),name='post-list'),
    path('detail/<int:pk>/',post_detail_great.as_view(),name='post-detail'),
    path('users/<int:pk>/', UserDetail.as_view(),name='user-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('api/',api_root,name='api')

]
urlpatterns = format_suffix_patterns(urlpatterns)