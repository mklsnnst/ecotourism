from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.published.all()  # Только опубликованные посты
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)  # Фильтр по статусу
    return render(request, 'blog/post/detail.html', {'post': post})