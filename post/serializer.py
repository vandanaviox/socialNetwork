from rest_framework import serializers
from post.models import Posts, Likes


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Posts
        fields = ('user', 'title', 'post_image', 'content')


class LikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Likes
        fields = '__all__'
