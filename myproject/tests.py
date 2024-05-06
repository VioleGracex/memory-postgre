from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Memory, UserFeed, Image, Video
from django.contrib.auth.models import User
from datetime import datetime

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.custom_user = CustomUser.objects.create(user=self.user)

    def test_register_user_view(self):
        # Assuming your register_user view is associated with a URL named 'register_user'
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            
        }
        response = self.client.post(reverse('register_user'), data)
        
        # Check if the registration redirects to the login page (status code 302)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginpage'))

    def test_login_view(self):
        # Assuming your login view is associated with a URL named 'loginpage'
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('loginpage'), data=data)
        self.assertEqual(response.status_code, 200)  # Assuming successful login returns status code 200
        # Add more assertions to test the behavior of logging in

    def test_add_to_feed_view(self):
        # Assuming your add_to_feed view is associated with a URL named 'add_to_feed'
        data = {
            'content': 'Test content',
            'location': 'Test location',
        }
        self.client.force_login(self.user)  # Log in the test user
        response = self.client.post(reverse('add_to_feed'), data=data)
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after adding to feed
        # Assert that the redirect goes to the user-specific feed page
        self.assertRedirects(response, reverse('user_specific_feed', args=(self.user.id,)))


    def test_user_feed_view(self):
        # Assuming your user_feed view is associated with a URL named 'user_specific_feed' and user ID as argument
        response = self.client.get(reverse('user_specific_feed', kwargs={'user_id': self.custom_user.id}))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to test the content of the response as needed


    def test_add_to_profile_view(self):
        # Assuming your add_to_profile view is associated with a URL named 'add_to_profile'
        data = {
            'profileAvatar': 'profile_pic.jpg',
            'coverImg': 'cover_img.jpg',
            'date_of_birth': datetime.now().strftime('%Y-%m-%d'),
            'bio': 'Test bio',
            'profile_type': 'public',
        }
        self.client.force_login(self.user)  # Log in the test user
        response = self.client.post(reverse('add_to_profile'), data=data)
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after adding to profile
        # Add more assertions to test the behavior of adding to profile

    

    def test_logout_view(self):
        # Assuming your logout view is associated with a URL named 'logout'
        response = self.client.get(reverse('logout_user'))  # Changed to match the URL name in urlpatterns
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after logout
        # Add more assertions to test the behavior of logging out

    # Add more test methods for other views if needed
