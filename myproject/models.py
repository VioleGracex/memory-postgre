#models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import uuid

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True, default='')
    registration_method = models.CharField(max_length=20, choices=[('social', 'Social Network'), ('normal', 'Normal Registration')])
    last_login = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    two_factor_authentication = models.BooleanField(default=False)
    profile_type = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='private')

    def __str__(self):
        return self.user.username

# Memory Model using ForeignKey
class Memory(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='memory_likes')
    comments = models.ManyToManyField('Comment', related_name='memory_comments')

class Image(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='memory_images/')
    image_id = models.CharField(max_length=50, unique=True, editable=False, default=uuid.uuid4)

class Video(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='memory_videos/')


class Comment(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on Memory: {self.memory.id}"


class UserFeed(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_feed')
    memories = models.ManyToManyField(Memory, related_name='user_feed_memories')

    def __str__(self):
        return f"Feed for {self.user.username}"

    def add_memory(self, memory):
        """
        Method to add a memory to the user feed.
        """
        self.memories.add(memory)

    def remove_memory(self, memory_id):
        """
        Method to remove a memory from the user feed.
        """
        try:
            memory = Memory.objects.get(pk=memory_id)
            self.memories.remove(memory)
            memory.delete()
            return True
        except Memory.DoesNotExist:
            return False

