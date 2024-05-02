# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from .models import CustomUser, UserFeed, Memory, Image, Video
from django.contrib.auth import get_user_model


#region Utility Functions

def login_user(request, user_name):
    try:
        user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        try:
            user = CustomUser.objects.create(username=user_name)
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('home')

    request.session['auto_login'] = True
    login(request, user)
    return redirect('userfeed')

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

def reg_page(request):
    context = {}
    return render(request, 'accounts/reg.html', context)

def login_page(request):
    return render(request, 'accounts/login.html')

@login_required  
def userfeed(request):
    user = request.user  # Access the authenticated user object
    #user_posts = user.memory_set.all()  # Assuming you have a related name 'memory_set' for the user's posts
    return render(request, 'user_feed.html', {'user': user})

@login_required 
def profile(request):
    user = request.user  # Access the authenticated user object
    return render(request, 'profile.html')

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        confirm_password = request.POST.get('confirm_password','')
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

            # Create the user
            user = get_user_model().objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name  # Save the first name to the CustomUser model
            user.last_name = last_name    # Save the last name to the CustomUser model
            user.save()  # Save the user object

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
        print (user)
        if user is not None:
            login(request, user)
            return redirect('userfeed')  # Redirect to user feed page after successful login
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
        user = request.user  # Get the current user
        content = request.POST.get('content')
        location = request.POST.get('location', 'Default location')
        images = request.FILES.getlist('images')  # Corrected to match the form input name
        videos = request.FILES.getlist('videos')

        if content:
            # Create a new Memory object and associate it with the user
            memory = Memory.objects.create(user=user, text=content, location=location)
            
            # Add images to the memory if they exist
            for image in images:
                Image.objects.create(memory=memory, image=image)
            
            # Add videos to the memory if they exist
            for video in videos:
                Video.objects.create(memory=memory, video=video)
            
            user_feed = UserFeed.objects.get_or_create(user=user)[0]
            user_feed.memories.add(memory)
            messages.success(request, 'Memory added to your feed successfully.')
            return redirect('userfeed')
        else:
            messages.error(request, 'Content is required.')
            return redirect('userfeed')  # Redirect to user feed page if content is missing
    else:
        messages.error(request, 'Method not allowed.')
        return redirect('userfeed')  # Redirect to user feed page for GET requests 

#endregion



""" def add_to_feed(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)  # Include request.FILES to handle uploaded files
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            content = form.cleaned_data['content']
            location = form.cleaned_data['location']
            images = request.FILES.getlist('images')  # Get list of uploaded images
            videos = request.FILES.getlist('videos')  # Get list of uploaded videos

            # Create Memory object
            memory = Memory.objects.create(user_id=user_id, text=content, location=location)

            # Save images
            for image in images:
                Image.objects.create(memory=memory, image=image)

            # Save videos
            for video in videos:
                Video.objects.create(memory=memory, video=video)

            # Optionally, you can add a success message here
            return redirect('success_url')
    else:
        form = MemoryForm()
    return render(request, 'user_feed.html', {'form': form})
 """

""" def logout_view(request):
    logout(request)
    request.session.flush()  # Flush the session data
    return redirect("home") """

""" def signup(request, signup_data=None):
    if request.method == 'POST' or signup_data:
        name = request.POST.get('name') if request.method == 'POST' else signup_data.get('name')
        email = request.POST.get('email') if request.method == 'POST' else signup_data.get('email')
        username = request.POST.get('username') if request.method == 'POST' else signup_data.get('username')
        password = request.POST.get('password') if request.method == 'POST' else signup_data.get('password')

        if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, "Username or email already exists.")
            return redirect('home')

        try:
            user = CustomUser.objects.create(
                name=name,
                email=email,
                username=username,
                password=password,
                # Assign other fields as needed
            )
            messages.success(request, "Account created successfully. You can now log in.")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('userfeed')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('home')

    else:
        return redirect('home') """