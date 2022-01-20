from django.urls import path

from users.views import RegistrationAPIView, LoginAPIView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('<int:user_id>/details', UserDetailView.as_view(), name='user_details')
]