from django.contrib import admin
from .models import Post, PostCategory, Comment, Group, RestrictUserComment, GroupJoinRequest
# Register your models here.
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(RestrictUserComment)
admin.site.register(GroupJoinRequest)