from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Base(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

class Post(Base):
    title=models.TextField(blank=True,null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='blogapp/',blank=True,null=True)
    caption=models.TextField(blank=True,null=True)
    likes=models.ManyToManyField(User,related_name="liked_posts",blank=True)
    
    def __str__(self):
        return self.title



class Comment(Base):
    content=models.TextField(blank=True,null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.content


class Like(Base):
    user=models.ForeignKey(User,on_delete=models.CASCADE)


