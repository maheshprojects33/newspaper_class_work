from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>", views.PostDetailView.as_view(), name="post-detail"),
    path("post-by-category/<int:cat_id>", views.PostByCategoryView.as_view(), name="post-by-category"),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),
    path("comment/", views.CommentView.as_view(), name="comment"),
]
