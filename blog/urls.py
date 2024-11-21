from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('',home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',register_view, name='register'),

    path('category/<slug:category_slug>/', category_view, name='category'),

    path('dashboard/',user_dashboard, name='dashboard'),
    path('profile/<slug:username>/',user_profile, name='profile'),
    path('profile/settings/<slug:username>/', profile_settings, name='profile_settings'),

    path('admin/dashboard/',admin_dashboard, name='admin_dashboard'),
    path('admin/delete-user/<int:user_id>/',delete_user, name='delete_user'),
    path('admin/delete_user/<int:user_id>/',delete_user, name='delete_user'),

    path('post/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('comment/reply/<int:comment_id>/', reply_comment, name='reply_comment'),


    path('post/create/',create_post, name='create_post'),

    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/<slug:slug>/like/', like_post, name='like_post'),

    path('post/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('post/<slug:slug>/edit/', edit_post, name='edit_post'),

    path('user/<str:username>/', user_dashboard, name='user_dashboard'),

    path('user-management/', user_management, name='user_management'),

    path('api/subscribe/', subscribe, name='subscribe'),
    path('developing', developing, name='devlopming')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
