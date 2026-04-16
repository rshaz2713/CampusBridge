from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("session/extend/", views.extend_session, name="extend_session"),
    path("session/expire/", views.expire_session, name="expire_session"),
    path('pin/<str:resource_id>/', views.toggle_pin, name='toggle_pin'),
]