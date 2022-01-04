
from django.urls import path

from shortener_app import views

urlpatterns = [
    # main urls
    path("home/", views.ShortUrlView.as_view(), name="home"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("urlslist/", views.urls_list_view, name="urlslist"),

    # redirect urls
    path("", views.home_redirect),
    path("logout/", views.logout_view, name="logout"),
    path("<path:short_url>", views.redirect_view, name="redirect"),
]
