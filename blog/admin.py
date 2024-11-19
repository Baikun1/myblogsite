from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, BlogPost, Comment, ContactSuggestion, Share, UserFollowing

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'created_at', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'created_at')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

admin.site.register(User, CustomUserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('published', 'category', 'author')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username', 'content')
    list_filter = ('post', 'user')

@admin.register(ContactSuggestion)
class ContactSuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'status', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('status',)

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'platform', 'created_at')
    search_fields = ('post__title', 'user__username')
    list_filter = ('platform',)

@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'following_user', 'created_at')
    search_fields = ('user__username', 'following_user__username')
