
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm  # Import the login_required decorator
from .models import CustomUser, Memory, UserFeed
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
@login_required
def add_to_feed(request):
    if request.method == 'POST':
        current_user = request.user
        custom_user = get_object_or_404(CustomUser, user=current_user)
        if custom_user:
            content = request.POST.get('content','')
            location = request.POST.get('location','')
            images = request.FILES.getlist('images')
            videos = request.FILES.getlist('videos')

            if content:
                memory = custom_user.memory_set.create(text=content, location=location)
                for image in images:
                    memory.image_set.create(image=image)
                for video in videos:
                    memory.video_set.create(video=video)
                messages.success(request, 'Memory added to your feed successfully.')
            else:
                messages.error(request, 'Content is required.')
        else:
            messages.error(request, 'CustomUser not found.')
    else:
        messages.error(request, 'Method not allowed.')
    return redirect('user_specific_feed', user_id=custom_user.id)

@login_required
@require_POST
def delete_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)
    custom_user = get_object_or_404(CustomUser, user=request.user)
    try:
        user_feed = UserFeed.objects.get(user=custom_user)
    except UserFeed.DoesNotExist:
        user_feed = UserFeed.objects.create(user=custom_user)
    if memory.custom_user == custom_user:
        if user_feed.remove_memory(memory_id):
            memory.delete()
            messages.success(request, 'Memory deleted successfully.')
        else:
            messages.error(request, 'Failed to delete memory from user feed.')
    else:
        messages.error(request, 'You are not authorized to delete this memory.')
    return redirect('user_specific_feed', user_id=custom_user.id)
#endregion


@login_required
def add_to_profile(request):
    if request.method == 'POST':
        current_user = request.user
        custom_user = get_object_or_404(CustomUser, user=current_user)
        if custom_user:  
            profile_picture = request.FILES.getlist('profileAvatar')
            cover_image = request.FILES.getlist('coverImg')
            date_of_birth = request.POST.get('date_of_birth')
            bio = request.POST.get('bio')
            profile_type = request.POST.get('profile_type')

            if date_of_birth is not None:
                try:
                    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                except ValueError:
                    date_of_birth = None
            
            if profile_picture:
                custom_user.profile_picture = profile_picture[0]

            if cover_image:
                custom_user.cover_image = cover_image[0]

            if bio:
                custom_user.bio = bio

            custom_user.profile_type = profile_type if profile_type else None               
            
            custom_user.save()

            messages.success(request, _('Changes added to your profile successfully.'))
        else:
            messages.error(request, _('CustomUser not found.')) 
    else:
        pass  # Handle GET request to render profile update form
    return redirect('user_specific_feed', user_id=custom_user.id)


@login_required
def edit_memory(request, memory_id):
    if request.method == 'POST':
        current_user = request.user
        custom_user = get_object_or_404(CustomUser, user=current_user)
        memory = Memory.objects.get(pk=memory_id)
        
        # Update memory fields with new values from the form
        text = request.POST.get('memory_text')
        location = request.POST.get('memory_location')
        
        # Check if text and location are not empty before assigning
        if text is not None:
            memory.text = text
        if location:
            memory.location = location
        
        # Get the IDs of remaining images from the form
        remaining_image_ids = request.POST.get('remaining_image_ids')  # Comma-separated string of image IDs
        
        # Convert comma-separated string to a list of integers
        try:
            remaining_image_ids = [int(id) for id in remaining_image_ids.split(',')]
        except ValueError:
            raise ValidationError("Invalid image IDs")
        
        # Clear existing images not in the remaining list
        memory.image_set.exclude(id__in=remaining_image_ids).delete()
        
        # Save the memory instance
        memory.save()
        
        messages.success(request, 'Memory updated successfully.')
        return redirect('user_specific_feed', user_id=custom_user.id)
    else:
        memory = Memory.objects.get(pk=memory_id)
        return render(request, 'edit_memory.html', {'memory': memory})