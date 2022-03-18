from django.shortcuts import render
from .models import Post


def post_list_view(request):
    post_list = Post.objects.filter(status='pub').order_by('-datetime_modified')
    return render(request, 'pages/posts_list.html', {'post_list': post_list})
