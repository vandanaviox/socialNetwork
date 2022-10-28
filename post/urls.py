from django.contrib import admin
from django.urls import path
from .views import LikeView, AllPostListing, PostListing, OthersPostListing, LikeCount,PostDetail

urlpatterns = [
    
    path('post/', PostListing.as_view()),
    path('postdetail/<int:pk>', PostDetail.as_view()),
    path('otherposts/', OthersPostListing.as_view()),
    path('postlikes/<int:pk>', LikeView.as_view()),
    path('allposts/', AllPostListing.as_view()),
    path('likescount/<int:pk>', LikeCount.as_view())
    
]
