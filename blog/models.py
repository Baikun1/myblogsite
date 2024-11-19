from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import EmailValidator
from django.utils.text import slugify

class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('MODERATOR', 'Moderator'),
        ('USER', 'User'),
    )
    
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=50)
    featured_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    
    if not self.excerpt:
        paragraphs = self.content.split('<p>')
        limited_paragraphs = paragraphs[:3]
        excerpt_content = '<p>'.join(limited_paragraphs)
        excerpt_words = excerpt_content.split()
        limited_excerpt = ' '.join(excerpt_words[:100])
        self.excerpt = limited_excerpt + "..."
    
    super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    commentlikes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

class ContactSuggestion(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('REPLIED', 'Replied'),
        ('RESOLVED', 'Resolved'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    post = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True, blank=True, related_name='suggestions')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    admin_response = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Suggestion from {self.user.username}'

class Share(models.Model):
    PLATFORM_CHOICES = (
        ('TWITTER', 'Twitter'),
        ('FACEBOOK', 'Facebook'),
        ('LINKEDIN', 'LinkedIn'),
        ('WHATSAPP', 'WhatsApp'),
    )

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    share_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('post', 'user', 'platform')

    def __str__(self):
        return f'{self.post.title} shared on {self.platform} by {self.user.username}'

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')

    def __str__(self):
        return f'{self.user.username} follows {self.following_user.username}'
