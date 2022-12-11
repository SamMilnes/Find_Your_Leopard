from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    gender = models.TextField(blank=True)
    location = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    age = models.TextField(blank=True)
    sleeping_habits = models.TextField(blank=True)
    number_of_roommates = models.TextField(blank=True)
    personality_types = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.user


class Roommate_Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user
