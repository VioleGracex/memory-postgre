from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm  # Import the login_required decorator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# Region: Home and Authentication

def home(request):
    return render(request, 'home.html')

def register_page(request, errors=None):
    form = RegistrationForm()  # Create an instance of the RegistrationForm
    context = {'form': form, 'errors': errors} if errors else {'form': form}
    return render(request, 'accounts/reg.html', context)

def admin(request):
    return render(request, 'admin.html')

def login_page(request, errors=None):
    form = LoginForm()  # Create an instance of the LoginForm
    context = {'form': form, 'errors': errors} if errors else {'form': form}
    return render(request, 'accounts/login.html', context)


User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('loginp_age')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/reg.html', {'form': form})


def login_user(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                custom_user = get_object_or_404(CustomUser, user=request.user)
                return redirect('user_specific_feed', user_id=custom_user.id)
            else:
                errors.append("Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    return login_page(request, errors, form=form)

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