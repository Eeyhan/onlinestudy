from django.urls import path
from LoginAuth import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('auth', views.LoginAuthView.as_view()),
    path('register', views.RegisterView.as_view()),
    path('index', views.IndexView.as_view()),
]
