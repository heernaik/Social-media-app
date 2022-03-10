from enum import unique
from turtle import title
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class DateTimemixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)   

    class Meta:
        abstract = True

class PostCategory(DateTimemixin):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name         
    
class Post(DateTimemixin):
    group_key = models.ForeignKey("Group", on_delete=models.CASCADE, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    user_key = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null = True)
    category_key = models.ManyToManyField(PostCategory,  blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to = 'photos/')
    slug = models.SlugField(null=True, blank=True)
    like_key = models.ManyToManyField(User, blank = True, related_name='like_user')
    dislike_key = models.ManyToManyField(User, blank = True, related_name='dislike_user')


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) 
        super(Post, self).save(*args, **kwargs)   

class Comment(DateTimemixin):
    post_key = models.ForeignKey(Post, on_delete=models.CASCADE, null = True, blank=True) 
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_user')  

    def __str__(self):
        return str(self.post_key) 

        

class Group(DateTimemixin):
    admin_user = models.ManyToManyField(User, related_name='admin_user')
    name = models.CharField(max_length=100)
    user_key = models.ManyToManyField(User, related_name='user_key')
    slug = models.SlugField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) 
        super(Group, self).save(*args, **kwargs) 

    def __str__(self):
        return str(self.name)

class GroupJoinRequest(DateTimemixin):
    user_key = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    group_key = models.ForeignKey(Group, on_delete=models.CASCADE, blank = True, null = True)
    is_accept = models. BooleanField(default=False)
    is_reject = models.BooleanField(default=False)
    next_date = models.DateField(null = True, blank = True) 

    def __str__(self):
        return str(self.user_key)


class RestrictUserComment(DateTimemixin):
    user_key = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank=True)
    restrict_user_key = models.ManyToManyField(User, related_name='restrict_key')

    def __str__(self):
        return str(self.user_key)

