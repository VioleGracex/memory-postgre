# views.py
from django.shortcuts import render, redirect
#from utils.user_social_utils import get_user_social_info, vk_auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import get_user_model


#region Utility Functions


#endregion

#region Views

# Region: Home and Authentication

def admin(request):
    return render(request, 'admin.html')

def home(request):
    return render(request, 'home.html')

