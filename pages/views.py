from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Post


def post_list_view(request):
    post_list = Post.objects.filter(status='pub').order_by('-datetime_modified')
    return render(request, 'pages/posts_list.html', {'post_list': post_list})


def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post_detail.html', {'post': post})
