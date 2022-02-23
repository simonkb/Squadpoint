from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search/<str:query>", views.search, name="search"),
    path("sport_zone/<int:id>", views.sport_zone, name="sport_zone"),
    path("page/<str:name>", views.page, name="page"),
    path("sport_court/<int:id>", views.sport_court, name="sport_court"),
    path("book/<int:court_id>", views.book, name="book"),
    path("create_match/<int:booking_id>", views.create_match, name="create_match"),
    path("bookings/<int:user_id>", views.bookings, name="bookings"),
    path("matches", views.matches, name="matches"),
    path("join_match/<int:match_id>", views.join_match, name= "join_match"),
]
