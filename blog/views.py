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
from django.core.paginator import Paginator
from django.db.models import Count

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


from django.db.models import Q

from django.db.models import Q, Count

# def home(request):
#     # Fetch category and order query parameters
#     query = request.GET.get('q', '')  # Get the search query from the URL
#     search_results = BlogPost.objects.none()  # Default to no results

#     # Check if there's a search query
#     if query:
#         posts = posts.filter(
#             Q(title__icontains=query) | Q(content__icontains=query),
#             published=True
#         ).annotate(likes_count=Count('likes'), comments_count=Count('comments'))
#     category_slug = request.GET.get('category')
#     order = request.GET.get('order', 'recent')

#     # Base query for published posts
#     posts = BlogPost.objects.filter(published=True)

#     # Filter by category if a category is selected
#     if category_slug:
#         posts = posts.filter(category__slug=category_slug)

#     # Order posts
#     if order == 'most_liked':
#         posts = posts.annotate(likes_count=Count('likes')).order_by('-likes_count')
#     elif order == 'most_commented':
#         posts = posts.annotate(comments_count=Count('comments')).order_by('-comments_count')
#     elif order == 'most_viewed':
#         posts = posts.order_by('-views_count')
#     else:  # Default: 'recent'
#         posts = posts.order_by('-created_at')

#     # Pagination for filtered posts
#     paginator = Paginator(posts, 12)  # Show 12 posts per page
#     page_number = request.GET.get('page')
#     paginated_posts = paginator.get_page(page_number)

#     # Featured posts (top 3 by views)
#     featured_posts = BlogPost.objects.filter(published=True)\
#         .annotate(likes_count=Count('likes'), comments_count=Count('comments'))\
#         .order_by('-views_count')[:3]

#     # Pass categories for filter dropdown
#     categories = Category.objects.all()

#     context = {
#         'posts': paginated_posts,
#         'featured_posts': featured_posts,
#         'categories': categories,
#         'selected_category': category_slug,
#         'selected_order': order,
#         'query': query,
#         'search_results': search_results,
#     }
#     return render(request, 'home.html', context)

def home(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category')
    order = request.GET.get('order', 'recent')

    # Base query for published posts
    posts = BlogPost.objects.filter(published=True)

    # Apply search filter
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__username__icontains=query) |
        Q(created_at__icontains=query),
        published=True
    )

    # Filter by category
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Apply ordering
    if order == 'most_liked':
        posts = posts.annotate(likes_count=Count('likes')).order_by('-likes_count')
    elif order == 'most_commented':
        posts = posts.annotate(comments_count=Count('comments')).order_by('-comments_count')
    elif order == 'most_viewed':
        posts = posts.order_by('-views_count')
    else:
        posts = posts.order_by('-created_at')

    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    # Featured posts
    featured_posts = BlogPost.objects.filter(published=True).order_by('-views_count')[:3]

    categories = Category.objects.all()

    context = {
        'posts': paginated_posts,
        'featured_posts': featured_posts,
        'categories': categories,
        'selected_category': category_slug,
        'selected_order': order,
        'query': query,
    }
    return render(request, 'home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        new_category_name = request.POST.get('new_category', '').strip()  
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                post.category = category 
            else:
                post.category = Category.objects.get(id=request.POST['category'])  # Use selected category
            
            slug = slugify(post.title)
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{slug}-{random.randint(1, 1000000)}"  
            post.slug = slug
            
            try:
                post.save()
                messages.success(request, 'Blog post created successfully!')
                return redirect('post_detail', slug=post.slug)
            except IntegrityError:
                messages.error(request, 'An error occurred while creating the blog post. Please try again.')
    else:
        form = BlogPostForm()
    
    categories = Category.objects.all() 
    
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

@login_required
def like_post(request, slug):
    try:
        post = get_object_or_404(BlogPost, slug=slug)
        
        if request.method == 'POST':
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True
            
            return JsonResponse({
                'liked': liked,
                'likes_count': post.likes.count(),
                'message': 'Action successful'
            })
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    
    comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
    related_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id)[:3]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                
                # Check if it's a reply
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    parent_comment = get_object_or_404(Comment, id=parent_id)
                    comment.parent = parent_comment  # Set the parent comment
                
                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('post_detail', slug=slug)
            else:
                messages.error(request, 'You must be logged in to comment.')
    else:
        comment_form = CommentForm()

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
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user

            # Check if it's a reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()

            # Return JSON response for AJAX
            response = {
                'comment_id': comment.id,
                'content': comment.content,
                'user': comment.user.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'parent_id': comment.parent.id if comment.parent else None,
            }
            return JsonResponse(response)

    # For GET request or invalid form
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def like_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.method == 'POST':
            if request.user in comment.likes.all():
                comment.likes.remove(request.user)
                liked = False
            else:
                comment.likes.add(request.user)
                liked = True
            
            return JsonResponse({
                'success': True,
                'likes_count': comment.likes.count(),
                'liked': liked
            })
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post  # Get the associated post

    if request.method == 'POST':
        reply_form = CommentForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.parent = parent_comment  # Set the parent to the comment being replied to
            reply.save()
            messages.success(request, 'Reply added successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'There was an error with your reply. Please try again.')
    else:
        reply_form = CommentForm()

    return render(request, 'blog/reply_comment.html', {
        'form': reply_form,
        'parent_comment': parent_comment,
        'post': post,
    })
@login_required
def edit_comment(request, comment_id):
    # Retrieve the comment to be edited or return a 404 if not found
    comment = get_object_or_404(Comment, id=comment_id)

    # Handle form submission
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)  # Bind the form with POST data and the existing comment instance
        if form.is_valid():
            form.save()  # Save the updated comment
            messages.success(request, 'Comment updated successfully!')  # Add a success message
            return redirect('post_detail', slug=comment.post.slug)  # Redirect to the post detail page
    else:
        form = CommentForm(instance=comment)  # Pre-fill the form with the current comment data

    # Render the edit comment template with the form and comment
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

def user_management(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query)  # Filter users by username
    else:
        users = User.objects.all()  # Get all users if no query is provided

    return render(request, 'blog/admin_dashboard.html', {'users': users})


def user_dashboard(request, username):
    author = get_object_or_404(User, username=username)
    logged_in_user = request.user
    context = {
        'author': author,  # The post's author
        'user': logged_in_user,  # The currently logged-in user
    }
    return render(request, 'user/dashboard.html', context)


@login_required
def profile_settings(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_settings', username=user.username)
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'blog/profile_settings.html', {'form': form, 'user': user})

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
