
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .models import BlogModel, Comment
from .forms import BlogForm
from django.core.paginator import Paginator

def index(request):
    list_blogs = BlogModel.objects.all().order_by('-id')

    p = Paginator(list_blogs, 8)
    page = request.GET.get('page')
    blogs = p.get_page(page)

    return render(request, 'main/index.html', {"blogs": blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog posted successfully!')
            return redirect("index")
    else:
        form = BlogForm(None)

    return render(request, 'main/create_blog.html', {'form': form})

def view_blog(request, pk):
    blog = BlogModel.objects.get(pk=pk)
    comments = blog.comments.all()
    form = BlogForm(None)
    return render(request, 'main/view_blog.html', {'blog': blog, 'comments': comments, 'form': form})

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        content = request.POST.get('text')
        blog_to_be_commented = get_object_or_404(BlogModel, id=pk)
        comment = Comment.objects.create(content=content, user=request.user, blog=blog_to_be_commented)
        html = render_to_string("partials/comment.html", {"comment": comment}, request=request)
        return JsonResponse({"html": html})
    return JsonResponse({"error": "Invalid request"}, status=400)

