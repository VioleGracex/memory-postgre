#models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    bio = models.TextField(blank=True)
    registration_method = models.CharField(max_length=20, choices=[('social', 'Social Network'), ('normal', 'Normal Registration')])
    registration_method = models.CharField(max_length=20, choices=[('social', 'Social Network'), ('normal', 'Normal Registration')])
    last_login = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    two_factor_authentication = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_groups',  # Unique related_name for groups
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_user_permissions',  # Unique related_name for user_permissions
        related_query_name='user',
    )
class Memory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name='memory_likes')
    comments = models.ManyToManyField('Comment', related_name='memory_comments')
    created_at = models.DateTimeField(default=timezone.now)  # Set default value here
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ManyToManyField('Image', related_name='memory_images')
    videos = models.ManyToManyField('Video', related_name='memory_videos')
    
    def __str__(self):
        return f"Memory by {self.user.username} at {self.created_at}"


class Image(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='memory_images/')

    def __str__(self):
        return f"Image for Memory: {self.memory.id}"


class Video(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    video = models.FileField(upload_to='memory_videos/')

    def __str__(self):
        return f"Video for Memory: {self.memory.id}"


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

