from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    post_image = models.ImageField(upload_to="posts/")
    release_date = models.DateField(auto_now_add=True)
    content= models.TextField()
    
    def get_likes(self, post_id):

        data = Likes.objects.filter(post_id = post_id)
        return list(map(lambda x:{"user_id":x.user.id,"user_email":x.user.email},data))


    def __str__(self)-> str:
        return self.title

class Likes(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self)-> str:
        return self.post.title
