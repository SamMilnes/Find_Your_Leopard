from django.contrib import admin
from .models import Profile, Post, Roommate_Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Roommate_Post)
