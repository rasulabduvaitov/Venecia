from django.urls import path
from .views import LoginView, CreateUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-admin/', CreateUserView.as_view(), name='create-admin'),
]