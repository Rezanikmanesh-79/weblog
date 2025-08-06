from django.urls import path
from blog.views import ListOfPostView,PostDetail

app_name = 'blog'
urlpatterns = [
    path('',ListOfPostView.as_view(),name="post-list"),
    path('post/<int:pk>/',PostDetail.as_view(),name="post-detail"),
]
