from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post_list/', views.post_list, name='post_list'),
    re_path('post_detail/(?P<post>[-\w]+)/', views.post_detail, name='detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

]
