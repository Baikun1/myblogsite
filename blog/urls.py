from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('',home, name='home'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',register_view, name='register'),
    path('category/<slug:category_slug>/', category_view, name='category'),
    path('post/create/',create_post, name='create_post'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', edit_post, name='edit_post'),
    path('post/<slug:slug>/like/', like_post, name='like_post'),
    path('post/<slug:slug>/share/', share_post, name='share_post'),
    path('post/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('dashboard/',user_dashboard, name='dashboard'),
    path('profile/settings/',profile_settings, name='profile_settings'),
    path('profile/<slug:username>/',user_profile, name='profile'),
     # path('contact/', views.submit_contact, name='contact'),
    path('search/',search, name='search'),
    path('admin/dashboard/',admin_dashboard, name='admin_dashboard'),
    path('admin/delete-user/<int:user_id>/',delete_user, name='delete_user'),
    path('admin/delete_user/<int:user_id>/',delete_user, name='delete_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
