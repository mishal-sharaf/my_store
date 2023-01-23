from django.urls import path
from owner import views



urlpatterns = [
    path("register",views.SignupView.as_view()),
    path("home",views.HomeView.as_view()),
    path("signin",views.SigninView.as_view()),
    path("products/add", views.ProductCreateView.as_view()),

] 