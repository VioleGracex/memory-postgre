# views.py
from django.shortcuts import render, redirect
from .auth_view import admin, home, register_page, login_page, register_user, login_user, logout_user, social_auth_user
from .profile_views import profile, user_specific_feed
from .memory_views import  add_to_profile, add_to_feed, delete_memory, edit_memory
def page_view(request, page_name):
    """Render the given page template."""
    return render(request, f'{page_name}.html')