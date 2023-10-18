from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

#  get_user_model give the in built User model 
User=get_user_model()
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    profile_img=models.ImageField(null=True)# have to add defulat here
    location=models.CharField(max_length=100,blank=True)
    work=models.CharField(max_length=20,null=True)
    relationship=models.CharField(max_length=20,null=True)
    dob=models.DateField(null=True)
    contact_no=models.CharField(max_length=10,null=True)

    def __str__(self) -> str:
        return f'{self.user}'
    
class Post(models.Model):
    
    # id=models.UUIDField(primary_key=True)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    image=models.ImageField(null=True)# we have update this fild
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.caption}"

class LikePost(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_id}'

class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follow_list = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_list')

    def __str__(self):
        return f'{self.user}'
    
class Comment(models.Model):
    post_commented=models.ForeignKey(Post,on_delete=models.CASCADE)
    content=models.TextField(null=False)
    user_commented=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.content}{self.user_commented}'
