from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.utils.translation import gettext as _


#region User Feed and Profile


@login_required
def profile(request, user_id):
    # Get the current authenticated user
    current_user = request.user

    # Get the CustomUser object associated with the given ID
    custom_user = get_object_or_404(CustomUser, id=user_id)

    # Check if the authenticated user matches the requested user
    if current_user != custom_user.user:
        return HttpResponseForbidden("You don't have permission to view this profile.")

    # Assuming you have a related name 'memory_set' for the user's posts in the Memory model
    user_posts = custom_user.memory_set.all() if custom_user else None  
    
    return render(request, 'profile.html', {'custom_user': custom_user, 'user_posts': user_posts})



@login_required
def user_specific_feed(request, user_id):
    # Get the CustomUser object associated with the given ID
    custom_user = get_object_or_404(CustomUser, id=user_id)

    # Check if the user feed is public or if the current user is the owner
    if custom_user.profile_type == 'public' or request.user == custom_user.user:
        user_memories = custom_user.memory_set.all().order_by('-created_at')
        return render(request, 'user_feed.html', {'custom_user': custom_user, 'user_memories': user_memories})
    else:
        # User feed is private and the current user is not the owner
        return HttpResponseForbidden("You don't have permission to view this user's feed.")
