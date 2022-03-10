from tokenize import group
from django.shortcuts import render, redirect
from .models import Comment, Post, Group, GroupJoinRequest
from django.contrib.auth.models import User
from django.contrib import auth 
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify


# Create your views here.

    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user:
            auth.login(request,user)
            return redirect('showlist')
        else:
            return redirect('login')    
    return render(request, "index.html")


def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = make_password(request.POST['password'])

        User.objects.create(username = username, email = email, password = password)
        return redirect('login')

    return render(request, "index.html")

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('login')

def index(request):
    total_count = Post.objects.filter(is_group = False).count()
    context = {"total_count":total_count}
    return render(request, "base.html",context)

def searchview(request):
    queryset = Post.objects.all()
    query = request.GET["q"] or ''
    if query:
        queryset = queryset.filter(title__startswith=query)
    context = {
        "queryset": queryset
    }    
    return render(request, "searchresult.html",context)

def showlist(request):
    from django.db.models import Count

    if request.method == 'POST':
        query = request.POST["q"]
        post_data = Post.objects.filter(title__startswith = query, is_group = False).annotate(like_count = Count('like_key')).order_by('-like_count','-created_at')
    else:
        post_data = Post.objects.filter(is_group = False).annotate(like_count = Count('like_key')).order_by('-like_count','-created_at')
    total_count = Post.objects.filter(is_group = False).count()
    comment_data = Comment.objects.all().annotate(like_count = Count('liked_by')).order_by('-like_count','-created_at')

    context = {
         'post_data':post_data,
         "total_count":total_count,
         "comment_data":comment_data,
    }

    return render(request, "showlist.html", context)

def createpost(request):

    if not request.user.is_authenticated:
        return redirect('login')

    total_count = Post.objects.filter(is_group = False).count()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']
        obj = Post.objects.create(user_key = request.user,title=title,description=description, thumbnail = image)
        obj.save()
    return render(request, "createpost.html",{"total_count":total_count})    


def updateview(request, slug):

    post_obj = Post.objects.get(slug = slug)
    total_count = Post.objects.filter(is_group = False).count()

    if request.method == 'POST':
        title = request.POST['title']
        thumbnail = request.FILES['image']
        description = request.POST['description']
        post_obj.title = title 
        post_obj.desciption = description
        post_obj.thumbnail = thumbnail
        post_obj.save()
        return redirect('showlist')


    return render(request, "updatepage.html",{'post_obj':post_obj,"total_count":total_count})    

def deleteview(request, id):
    Post.objects.filter(id=id).delete()
    return redirect('showlist')    

def LikeView(request,id):

    post_obj = Post.objects.get(pk = id)

    if request.user in post_obj.dislike_key.all():
        post_obj.dislike_key.remove(request.user)
        post_obj.like_key.add(request.user)
    elif request.user in post_obj.like_key.all():
        post_obj.like_key.remove(request.user)    
    else:
        post_obj.like_key.add(request.user)
        post_obj.save()
    return redirect('showlist')


def dislikeView(request,id):

    post_obj = Post.objects.get(pk = id)

    if request.user in post_obj.like_key.all():
        post_obj.like_key.remove(request.user)
        post_obj.dislike_key.add(request.user)
    elif request.user in post_obj.dislike_key.all():
        post_obj.dislike_key.remove(request.user)    
    else:
        post_obj.dislike_key.add(request.user)
        post_obj.save()
    return redirect('showlist')

def commentView(request, id):
    post_obj = Post.objects.get(id=id)
    if request.method == 'POST':
        comment_text = request.POST['comment']
        comm_obj = Comment.objects.create(post_key=post_obj,comment=comment_text,created_by=request.user)
        comm_obj.save()
        return redirect('showlist')


def commentlike(request, id):
    comment_obj = Comment.objects.get(id=id)

    if request.user in comment_obj.liked_by.all():
        comment_obj.liked_by.remove(request.user)
    else:
        comment_obj.liked_by.add(request.user)
    return redirect('showlist')


def groupview(request):
    group_obj = Group.objects.all()
    total_count = Post.objects.filter(is_group = False).count()


    context = {
        "group_obj":group_obj,
        "total_count":total_count,
    }
    return render(request, "group.html",context)

def groupList(request, slug):
    group_data = Group.objects.get(slug = slug)
    
    post_list = Post.objects.filter(group_key = group_data.id, is_group = True)
    comment_data = Comment.objects.all()
    context = {"post_list":post_list, "group_data":group_data,"comment_data":comment_data}


    return render(request, "grouplist.html",context)


def followView(request, id):
    grp_obj = Group.objects.get(id=id)
    # if request.user not in grp_obj.user_key.all():
    #     grp_obj.user_key.add(request.user)
    GroupJoinRequest.objects.create(group_key = grp_obj, user_key = request.user)

    return redirect('group')


def unfollowView(request, id):
    grp_obj = Group.objects.get(id=id)
    if request.user in grp_obj.user_key.all():
        grp_obj.user_key.remove(request.user)
    return redirect('group')    


def setting_view(request):
    user_obj = User.objects.all()

    context = {
        'user_obj':user_obj
    }

    return render(request, 'settings.html', context)    


def create_group(request):
    if request.method == 'POST':
        name = request.POST["name"]
        grp_obj = Group.objects.create(name=name)
        grp_obj.admin_user.add(request.user)
        grp_obj.user_key.add(request.user)
        grp_obj.save()
    return render(request, 'creategroup.html')

def adminView(request, id):
    grp_obj = Group.objects.get(id=id)
    if request.method == 'POST':
        request_user_var = request.POST.getlist('checks[]')
        user_join = GroupJoinRequest.objects.filter(user_key__in = request_user_var)
        for user in user_join:
            grp_obj.user_key.add(user.user_key)
            grp_obj.save()

        user_join.delete()

    join_obj = GroupJoinRequest.objects.filter(group_key=grp_obj, is_accept = False)    

    context = {
        "grp_obj":grp_obj,
        "join_obj":join_obj,
    }
    return render(request,'adminpanel.html',context)
