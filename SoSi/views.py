from django.shortcuts import redirect, render, redirect, get_object_or_404 # type: ignore
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like
from .forms import ProfileUpdateForm, UserRegisterForm, ProfileForm, PostForm, CommentForm
from django.http import HttpResponseForbidden

# Create your views here.

# def index(request):
#     posts = Post.objects.select_related('author').prefetch_related('comments', 'liked_by')[:100]
#     post_form = PostForm()
#     comment_form = CommentForm()
#     context = {'posts': posts, 'post_form': post_form, 'comment_form': comment_form}
#     return render(request, 'index.html', context)

def index(request):
    posts = Post.objects.all()
    for p in posts:
        p.is_liked = False
        if request.user.is_authenticated:
            p.is_liked = p.liked_by.filter(id=request.user.id).exists()

    return render(request, "index.html", {
        "posts": posts
    })


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, bio=profile_form.cleaned_data.get('bio', ''))
            avatar = profile_form.cleaned_data.get('avatar')
            if avatar:
                profile.avatar = avatar
                profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('SoSi:index')
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "users/edit_profile.html", {"form": form})

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("feed")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username) # type: ignore
    posts = user.posts.all()
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == "POST" and request.user == user:
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profile updated.")
            return redirect('SoSi:profile', username=user.username)
    else:
        pform = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts, 'pform': pform})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created.")
            return redirect('SoSi:index')
    return redirect('SoSi:index')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # type: ignore
    comment_form = CommentForm()
    return render(request, 'postdetail.html', {'post': post, 'comment_form': comment_form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) # type: ignore
    if request.user != post.author:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect('SoSi:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk) # type: ignore
    if request.user != post.author:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect('SoSi:index')
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk) # type: ignore
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    # redirect back to where the request came from
    return redirect(request.META.get('HTTP_REFERER', 'SoSi:index'))

@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk) # type: ignore
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
    return redirect('SoSi:post_detail', pk=post_pk)


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('SoSi:login')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('SoSi:index')  # Already logged in

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('SoSi:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})
