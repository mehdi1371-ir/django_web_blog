from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .models import Post
from .forms import PostForm


def post_list_view(request):
    post_list = Post.objects.filter(status='pub').order_by('-datetime_modified')
    return render(request, 'pages/posts_list.html', {'post_list': post_list})


def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post_detail.html', {'post': post})


def myblog_post_view(request):
    posts_list = Post.objects.filter(author=request.user.id).order_by('-datetime_modified')
    return render(request, 'pages/my_blog.html', {'posts_list': posts_list})


def post_create_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'pages/post_create.html', {'form': form})


def post_update_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'pages/post_create.html', {'form': form})


def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'pages/post_delete.html', {'post': post})
