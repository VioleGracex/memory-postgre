# views.py
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from .models import CustomUser, Memory, UserFeed
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext as _
from django.urls import reverse
from django.views.decorators.http import require_POST

#region Utility Functions



#endregion

#region Views

# Region: Home and Authentication

def home(request):
    return render(request, 'home.html')

def loginpage(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def regpage(request):
    context = {}
    return render(request, 'accounts/reg.html', context)

def admin(request):
    return render(request, 'admin.html')

def login_page(request):
    return render(request, 'accounts/login.html')


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
        user_memories = custom_user.memory_set.all()
        return render(request, 'user_feed.html', {'custom_user': custom_user, 'user_memories': user_memories})
    else:
        # User feed is private and the current user is not the owner
        return HttpResponseForbidden("You don't have permission to view this user's feed.")



User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        first_name = request.POST.get('first_name', '')  # Get the first name field
        last_name = request.POST.get('last_name', '')

        # Validate the password
        try:
            validate_password(password)
        except ValidationError as e:
            # Password validation failed, display error message
            messages.error(request, "\n".join(e))
            return redirect('regpage')

        # Check if the password is the same as the username
        if password == username:
            messages.error(request, "Password cannot be the same as the username.")
            return redirect('regpage')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('regpage')

        try:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('regpage')

            # Create the default User
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name  # Save the first name to the User model
            user.last_name = last_name    # Save the last name to the User model
            user.save()  # Save the user object

            # Create the associated CustomUser object
            custom_user = CustomUser.objects.create(
                user=user,
                bio='', 
                registration_method='normal',  
                email_verified=False,  
                two_factor_authentication=False,  
                # Add other fields as needed
            )

            # Redirect the user to the login page
            return redirect('loginpage')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('regpage')
    else:
        return redirect('regpage')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            custom_user = get_object_or_404(CustomUser, user=request.user)
            return redirect('user_specific_feed', user_id=custom_user.id)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('loginpage')
    else:
        return redirect('loginpage')


# Define the custom pipeline function
def social_auth_user(request, sociallogin, **kwargs):
    user = sociallogin.user
    if sociallogin.account.provider == 'vk-oauth2':
        # Extract user data from VK
        vk_data = sociallogin.account.extra_data
        
        # Create a custom user object and populate it with VK data
        custom_user = CustomUser.objects.create(
            username=vk_data['username'],  
            first_name=vk_data['first_name'],
            last_name=vk_data['last_name'],
            email=vk_data['email'],
            date_of_birth=vk_data.get('date_of_birth'),  # Assuming 'date_of_birth' is a key in vk_data
            profile_picture=vk_data.get('profile_picture'),  # Assuming 'profile_picture' is a key in vk_data
            # Add other fields as needed
        )
        # Associate the custom user with the social account
        sociallogin.connect(request, user=custom_user)
        # Redirect to user-specific feed page after login
        return redirect('user_specific_feed', custom_user.id)
    return

def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout
    
#endregion


#region User Feed and Profile
@login_required
def add_to_feed(request):
    if request.method == 'POST':
        current_user = request.user
        custom_user = get_object_or_404(CustomUser, user=current_user)
        if custom_user:
            content = request.POST.get('content')
            location = request.POST.get('location', 'Default location')
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
            
            custom_user.profile_picture = profile_picture[0] if profile_picture else None
            
            custom_user.cover_image = cover_image[0] if cover_image else None

            custom_user.bio = bio if bio else None

            custom_user.profile_type = profile_type if profile_type else None
            
            #print(profile_picture)                
            
            custom_user.save()

            messages.success(request, _('Changes added to your profile successfully.'))
        else:
            messages.error(request, _('CustomUser not found.')) 
    else:
        pass  # Handle GET request to render profile update form
    return redirect('user_specific_feed', user_id=custom_user.id)


