from django.shortcuts import render,redirect
from .models import Post,Comment
from django.db import models
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import EditForm,CommentForm
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
@never_cache
def dashboard(request):
    return render(request,'blogapp/dashboard.html')

def create_post(request):
    if request.method=="POST":
        title=request.POST.get('title')
        image=request.FILES.get('image')
        caption=request.POST.get('caption')
        Post.objects.create(author=request.user,caption=caption,image=image,title=title)
        return redirect('dashboard')
    return render(request,'blogapp/create_post.html')

@login_required
def display_post(request):
    posts=Post.objects.filter(author=request.user)
    posts=posts.annotate(
        total_likes=models.Count('likes',distinct=True),
        total_comments=models.Count('comments',distinct=True)
        )
    return render(request,'blogapp/display_post.html',{'posts':posts})


def feed(request):
    posts=Post.objects.all()
    posts=posts.annotate(
        total_likes=models.Count('likes',distinct=True),
        total_comments=models.Count('comments',distinct=True),
        )
    return render(request,'blogapp/feed.html',{'posts':posts})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
          form.save()
          messages.success(request,"User Registered Successfully✅")
          return redirect('login')
        

        messages.error(request,"Invalid Credentials❌")


    return render(request,'blogapp/home.html',{'form':form })
        

def home(request):
    form=RegisterForm()
    return render(request,'blogapp/home.html',{'form':form })

def login(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            auth_login(request,user)
            messages.success(request,"User LogIn successful🎉")
            return redirect('dashboard')
        else:
            messages.error(request,"Either the password or username is incorrect❌")


    else:
        form = AuthenticationForm()
        
    return render(request,'blogapp/login.html',{"form":form})

@never_cache
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request,"Logged Out successfully!🎉")
    return redirect('login')


@login_required
def profile(request):
    user_posts=Post.objects.filter(author=request.user)
    return render(request,'blogapp/profile.html',{"user_posts":user_posts})

@login_required
def edit_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=="POST":
      form=EditForm(request.POST,request.FILES,instance=post)
      if form.is_valid():
        form.save()
        return redirect('profile')
    else:
        form=EditForm(instance=post)

    return render(request,'blogapp/edit_post.html',{"form":form})

@login_required
def delete_post(request,id):
    post=get_object_or_404(Post,id=id,author=request.user)
    post.delete()
    return redirect("profile")

@login_required
def like_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.user not in post.likes.all():
       post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    next_url=request.POST.get('next','display_post')
    return redirect(next_url)



@login_required
def add_comment(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=="POST":
        content=request.POST.get('comment')
        if content:
          Comment.objects.create(
              content=content,
              post=post,
              user=request.user,
              )
          
          next_url=request.POST.get('next','display_post')
          return redirect(next_url)
        else:
            messages.error(request,"Comment cannot be empty❗")
        
    return redirect('display_post')

@login_required  
def add_comment_page(request,id):
    post=get_object_or_404(Post,id=id)
    posts=Post.objects.all()
    next_url=request.GET.get('next','display_post')
    context={
          "post":post,
          "posts":posts,
          "next_url":next_url,
    }

    return render(request,'blogapp/add_comment.html',context)