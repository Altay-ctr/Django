from django.shortcuts import render, get_object_or_404
from .models import Blog

# --- Новое представление для списка ---
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/list.html', {'blogs': blogs})

# --- Ваше старое представление (не трогаем) ---
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.likes += 1
    blog.save()
    return render(request, 'blog/detail.html', {'blog': blog})