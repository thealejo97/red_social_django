from social.models import Post
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import PostForm, UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def feed(request):
    posts = Post.objects.all() #Pasandole todos los post del modelo
    
    context = {'posts':posts} #Atraves de un contexto
    return render(request, 'social/feed.html', context)

def register(request): #Vista del Registro
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #Creo la form por defecto de Django
        if form.is_valid():
            form.save()
            messages.success(request, f'El Usuario ha sido creado')
            return redirect('feed')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'social/register.html', context)

def post(request):
    current_user = get_object_or_404(User, pk= request.user.pk)
    print("Hall", request.method)
    print("Hall", request.POST)
    print("Hall", request.FILES.get('image_post'))
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print("")
            print("")
            print("")
            print("")
            print(request.__dict__)
            
            
            post= form.save(commit=False)
            
            post.user = current_user
            post.img_post = request.FILES.get('image_post')
            
            form.save()
            messages.success(request, 'Publicado')
            return redirect('feed')
    else:
        form= PostForm()
    
    context = {'form':form}
    return render(request, 'social/post.html', context)

def profile(request, username = None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        user = current_user
        posts = current_user.posts.all()

    return render(request, 'social/profile.html' , {'user':user , 'posts':posts})