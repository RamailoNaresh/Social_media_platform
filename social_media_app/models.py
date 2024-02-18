from django.db import models
from django.core.validators import MaxValueValidator

class CustomUser(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.TextField()
    
class UserProfile(models.Model):
    address =  models.CharField(max_length = 100)
    country = models.CharField(max_length  = 100)
    phone_number = models.PositiveIntegerField(validators = [MaxValueValidator(999999999)])
    profile_img = models.ImageField(upload_to = "profile/")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
class Post(models.Model):
    caption = models.TextField(null = True, blank = True)
    post_img = models.ImageField(upload_to = "post/", null = True, blank = True)
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, related_name="post_owner")
    like = models.ManyToManyField(CustomUser, related_name="likers")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    


    
    