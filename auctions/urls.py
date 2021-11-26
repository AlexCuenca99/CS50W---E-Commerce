from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addAuctionList", views.addAuctionList, name="addAuctionList"),
    path("watchedAuctionLists", views.watchedAuctionLists, name="watchedAuctionLists"),
    path(
        "watchedAuctionLists/<int:auctionListId>/changeAuctionList/<str:currentPage>",
        views.changeWatchList,
        name="changeWatchList",
    ),
    path("activeCatAucLists", views.activeAuctionLists, name="activeCatAucLists"),
    path("activeCatAucLists/<int:filterCategory>", views.activeAuctionLists, name="activeCatAucLists"),
    path("auctionList/<int:auctionListId>", views.auctionList, name="auctionList"),
    path("auctionList/<int:auctionListId>/bid", views.makeBid, name="makeBid"),
    path("auctionList/<int:auctionListId>/close", views.closeAuctionList, name="closeAuctionList"),
    path("auctionList/<int:auctionListId>/comment", views.addComment, name="addComment"),
]
