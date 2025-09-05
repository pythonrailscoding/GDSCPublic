
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from .models import BlogModel, Comment
from .forms import BlogForm, BlogCreateForm
from django.core.paginator import Paginator

def index(request):
    list_blogs = BlogModel.objects.all().order_by('-id')

    p = Paginator(list_blogs, 8)
    page = request.GET.get('page')
    blogs = p.get_page(page)

    is_other = False

    return render(request, 'main/index.html', {"blogs": blogs, "is_other": is_other})

def view_user_all(request, pk):
    user = User.objects.get(pk=pk)
    list_blogs = BlogModel.objects.filter(user=user).order_by('-id')

    p = Paginator(list_blogs, 8)
    page = request.GET.get('page')
    blogs = p.get_page(page)

    is_other = True

    return render(request, 'main/index.html', {"blogs": blogs, "is_other": is_other, "user": user})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog posted successfully!')
            return redirect("index")
    else:
        form = BlogCreateForm(None)

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

@login_required
def edit_blog(request, pk):
    pass

@login_required
def delete_blog(request, pk):
    blog = BlogModel.objects.get(pk=pk)
    if blog.user.id == request.user.id:
        blog.delete()
        """
        # redirect user to whatever post they sent request. Why? Say user was sending from view his blogs.
        # Redirect him to view his blogs. What if he was sending from main page itself, redirect him back
        what_to_redirect_ = request.GET.get('next') or request.POST.get('next')
        if what_to_redirect_:
            return redirect(what_to_redirect_)
            
        My use case for this elapsed. But this is how you delete
        """
        messages.success(request, 'Blog deleted successfully!')
        return redirect("index")
    else:
        messages.error(request, 'You are not authorized to delete this blog!')
        return redirect("index")

@login_required
def update_blog(request, pk):
    blog = BlogModel.objects.get(pk=pk)

    if blog.user.id != request.user.id:
        messages.error(request, 'You are not authorized to edit this blog!')
        return redirect("index")

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)

            # ✅ only replace thumbnail if a new file was uploaded
            if not form.cleaned_data.get("thumbnail"):
                blog.thumbnail = blog.thumbnail  # keep the old file

            blog.was_updated = True
            blog.when_last_updated = timezone.now().date()
            blog.save()

            messages.success(request, 'Blog updated successfully!')
            return redirect("view_blog", pk=pk)
    else:
        form = BlogForm(instance=blog)

    return render(request, "main/update_blog.html", {"blog": blog, "form": form})

