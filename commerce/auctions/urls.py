from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("catji", views.catji, name="catji"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch/<int:id>",views.watch,name="watch"),
    path("comment/<int:id>",views.comment,name="comment"),
    path("removewatch/<int:id>", views.removewatch, name="removewatch"),
    path("addwatch/<int:id>", views.addwatch, name="addwatch"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),

]
