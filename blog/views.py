from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.utils.text import slugify
import random

from .models import (
    BlogPost,
    Comment,
    Category,
    ContactSuggestion,
    Share,
    User
)

from .forms import (
    ShareForm,
    ContactSuggestionForm,
    CategoryForm,
    CommentForm,
    BlogPostForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)

def home(request):
    featured_posts = BlogPost.objects.filter(published=True).order_by('-views_count')[:3]
    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:5]
    categories = Category.objects.all()
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        new_category_name = request.POST.get('new_category', '').strip()  # Get the new category name
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Check if a new category is provided and create it if it doesn't exist
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                post.category = category  # Assign the category to the post
            else:
                post.category = Category.objects.get(id=request.POST['category'])  # Use selected category
            
            # Generate a unique slug
            slug = slugify(post.title)
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{slug}-{random.randint(1, 1000000)}"  # Append a random number to make it unique
            post.slug = slug
            
            try:
                post.save()
                messages.success(request, 'Blog post created successfully!')
                return redirect('post_detail', slug=post.slug)
            except IntegrityError:
                messages.error(request, 'An error occurred while creating the blog post. Please try again.')
    else:
        form = BlogPostForm()
    
    categories = Category.objects.all()  # Fetch all categories
    
    return render(request, 'blog/create_post.html', {
        'form': form,
        'categories': categories,
    })
@login_required
def edit_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('dashboard')
    return render(request, 'blog/delete_post.html', {'post': post})

def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    comments = post.comments.filter(parent=None).order_by('-created_at')
    related_posts = BlogPost.objects.filter(
        category=post.category
    ).exclude(id=post.id)[:3]
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    # Increment view count
    post.views_count += 1
    post.save()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', slug=post_slug)
    return render(request, 'blog/delete_comment.html', {'comment': comment})

@login_required
def like_post(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, slug=slug)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def share_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            share = form.save(commit=False)
            share.post = post
            share.user = request.user
            share.save()
            messages.success(request, f'Post shared on {share.platform}!')
            return redirect('post_detail', slug=slug)
    else:
        form = ShareForm()
    
    return render(request, 'blog/share_post.html', {
        'form': form,
        'post': post
    })

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts_list = BlogPost.objects.filter(category=category, published=True)
    paginator = Paginator(posts_list, 9)  # 9 posts per page
    
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts
    })

@login_required
def user_dashboard(request):
    user_posts = BlogPost.objects.filter(author=request.user)
    context = {
        'user_id': request.user.id,
        'user_email': request.user.email,
        'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
        'draft_posts': user_posts.filter(published=False),
        'published_posts': user_posts.filter(published=True),
        'liked_posts': BlogPost.objects.filter(likes=request.user),
    }
    
    template, admin_context = get_dashboard_template(request.user.role)
    context.update(admin_context)  # Merge admin context if user is admin or moderator
    
    return render(request, template, context)

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = BlogPost.objects.filter(author=user)  # Fetch user's posts for profile view
    context = {
        'user_id': user.id,
        'user_email': user.email,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
        'draft_posts': user_posts.filter(published=False),
        'published_posts': user_posts.filter(published=True),
        'liked_posts': BlogPost.objects.filter(likes=user),
    }
    
    template, admin_context = get_dashboard_template(request.user.role)
    context.update(admin_context)  # Merge admin context if user is admin or moderator
    context.update({'user': user})  # Include the user in the context
    
    return render(request, template, context)

def get_dashboard_template(role):
    if role in ['ADMIN', 'MODERATOR']:
        template = 'blog/admin_dashboard.html'
        
        # Fetch all user details
        users = User.objects.all()
        posts = BlogPost.objects.all()
        suggestions = ContactSuggestion.objects.filter(status='PENDING')

        context = {
            'users': users,
            'posts': posts,
            'suggestions': suggestions,
        }
    else:
        template = 'blog/user_dashboard.html'  # Ensure this matches the user dashboard template name
        context = {}
    
    return template, context


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')  # Redirect to the admin dashboard after deletion
    return render(request, 'confirm_delete.html', {'user': user}) 

def submit_contact_suggestion(request):
    if request.method == 'POST':
        form = ContactSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            messages.success(request, 'Your suggestion has been submitted!')
            return redirect('home')
    else:
        form = ContactSuggestionForm()
    
    return render(request, 'blog/contact_suggestion.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all().order_by('-date_joined')
    posts = BlogPost.objects.all().order_by('-created_at')
    suggestions = ContactSuggestion.objects.filter(status='PENDING')
    
    context = {
        'users': users,
        'posts': posts,
        'suggestions': suggestions,
    }
    return render(request, 'blog/admin_dashboard.html', context)
@login_required
def profile_settings(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_settings')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'blog/profile_settings.html', {'form': form})

@login_required
def submit_contact_suggestion(request):
    if request.method == 'POST':
        form = ContactSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            messages.success(request, 'Your suggestion has been submitted!')
            return redirect('home')
    else:
        form = ContactSuggestionForm()
    
    return render(request, 'blog/contact_suggestion.html', {'form': form})

def search(request):
    query = request.GET.get('q')
    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            published=True
        )
    else:
        results = BlogPost.objects.none()  # No results if no query
    
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User  deleted successfully!')
        return redirect('admin_dashboard')
    
    return render(request, 'blog/delete_user.html', {'user': user})
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
