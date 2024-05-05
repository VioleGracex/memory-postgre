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
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext as _
from django.urls import reverse

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
def profile(request, username):
    # Get the current authenticated user
    current_user = request.user

    # Get the CustomUser object associated with the given username
    custom_user = get_object_or_404(CustomUser, user__username=username)

    # Check if the authenticated user matches the requested user
    if current_user != custom_user.user:
        return HttpResponseForbidden("You don't have permission to view this profile.")

    # Assuming you have a related name 'memory_set' for the user's posts in the Memory model
    user_posts = custom_user.memory_set.all() if custom_user else None  
    
    return render(request, 'profile.html', {'custom_user': custom_user, 'user_posts': user_posts})



@login_required
def user_specific_feed(request, username):
    # Get the CustomUser object associated with the given username
    custom_user = get_object_or_404(CustomUser, user__username=username)

    # Check if the user feed is public or if the current user is the owner
    if custom_user.profile_type == 'public' or request.user == custom_user.user:
        user_posts = custom_user.memory_set.all()
        return render(request, 'user_feed.html', {'custom_user': custom_user, 'user_posts': user_posts})
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
            # Redirect to the user's specific feed based on their username
            return redirect('user_specific_feed', username=username)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('loginpage')  # Redirect back to login page if login fails
    else:
        return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout
    
#endregion


#region User Feed and Profile
@login_required
def add_to_feed(request):
    if request.method == 'POST':
        # Get the current authenticated user
        current_user = request.user
        
        # Retrieve the associated CustomUser instance
        custom_user = CustomUser.objects.filter(user=current_user).first()  # Assuming user is the ForeignKey field in CustomUser model
        
        # Assuming you have a related name 'memory_set' for the user's posts in the Memory model
        if custom_user:
            content = request.POST.get('content')
            location = request.POST.get('location', 'Default location')
            images = request.FILES.getlist('images')  # Corrected to match the form input name
            videos = request.FILES.getlist('videos')

            if content:
                # Create a new Memory object and associate it with the user
                memory = custom_user.memory_set.create(text=content, location=location)
                
                # Add images to the memory if they exist
                for image in images:
                    memory.image_set.create(image=image)
                
                # Add videos to the memory if they exist
                for video in videos:
                    memory.video_set.create(video=video)
                
                messages.success(request, 'Memory added to your feed successfully.')
                return redirect('user_specific_feed', username=request.user)
            else:
                messages.error(request, 'Content is required.')
                return redirect('user_specific_feed', username=request.user)
        else:
            messages.error(request, 'CustomUser not found.')
            return redirect('user_specific_feed', username=request.user)
    else:
        messages.error(request, 'Method not allowed.')
        return redirect('user_specific_feed', username=request.user)  # Redirect to user feed page for GET requests

#endregion


@login_required
def add_to_profile(request):
    if request.method == 'POST':
        # Get the current authenticated user
        current_user = request.user
        
        # Retrieve the associated CustomUser instance
        custom_user = CustomUser.objects.filter(user=current_user).first()  # Assuming user is the ForeignKey field in CustomUser model
        
        if custom_user:
            # Extract form data
            profile_picture = request.FILES.get('avatar')
            cover_image = request.FILES.get('cover')
            date_of_birth = request.POST.get('date_of_birth')
            bio = request.POST.get('bio')
            profile_type = request.POST.get('profile_type')  # Default to 'public' if not provided
            if profile_picture:
                print("profile_picture:", profile_picture.name)
            else:
                print("No profile picture uploaded.")

            # Check if date of birth is valid
            if date_of_birth is not None:
                try:
                    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                except ValueError:
                    # Handle case where date is not valid
                    date_of_birth = None
            # Update CustomUser instance with new data
            if profile_picture is not None:
                custom_user.profile_picture = profile_picture
            if cover_image is not None:
                custom_user.cover_image = cover_image
            if date_of_birth is not None:
                custom_user.date_of_birth = date_of_birth
            if bio is not None:
                custom_user.bio = bio
            if profile_type is not None:
                custom_user.profile_type = profile_type
            
            custom_user.save()

            messages.success(request, _('Changes added to your profile successfully.'))
            return redirect('user_specific_feed', username=request.user)
        else:
            messages.error(request, _('CustomUser not found.'))
            return redirect('user_specific_feed', username=request.user)  
    else:
        # Handle GET request to render profile update form
        # You can render the form template here
        pass



