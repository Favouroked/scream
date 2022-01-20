from django.urls import path

from posts.views import PostAPIView, LikeAPIView

app_name = 'posts'

urlpatterns = [
    path('', PostAPIView.as_view(), name='index'),
    path('<int:pk>', PostAPIView.as_view(), name='details'),
    path('<int:post_id>/like', LikeAPIView.as_view(), name='like')
]