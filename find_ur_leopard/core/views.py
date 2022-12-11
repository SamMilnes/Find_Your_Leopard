from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, Roommate_Post
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)

    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if '@wit' not in email:
            messages.info(request, 'Not a Wentworth Email')
            return redirect('signup')
            # return redirect('signup.html')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "This Email Has Already Been Taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "This Username Has Already Been Taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Passwords Do Not Match')
            return redirect('signup.html')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Login Credentials')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            sleeping_habits = request.POST.get('sleeping_habits')
            number_of_roommates = request.POST.get('number_of_roommates')
            personality_types = request.POST.get('personality_types')
            interests = request.POST.get('interests')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.gender = gender
            user_profile.age = age
            user_profile.sleeping_habits = sleeping_habits
            user_profile.number_of_roommates = number_of_roommates
            user_profile.personality_types = personality_types
            user_profile.interests = interests

            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            sleeping_habits = request.POST.get('sleeping_habits')
            number_of_roommates = request.POST.get('number_of_roommates')
            personality_types = request.POST.get('personality_types')
            interests = request.POST.get('interests')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.gender = gender
            user_profile.age = age
            user_profile.sleeping_habits = sleeping_habits
            user_profile.number_of_roommates = number_of_roommates
            user_profile.personality_types = personality_types
            user_profile.interests = interests

            user_profile.save()

        return redirect('/')
    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        caption = request.POST.get('caption')

        if caption == '':
            return redirect('/')

        new_post = Post.objects.create(user=user, caption=caption)

        new_post.save()

        return redirect('/')

    else:
        return redirect('/')


@login_required(login_url='signin')
def roommate_feed(request):
    user_object = User.objects.get(username=request.user.username)

    user_profile = Profile.objects.get(user=user_object)

    posts = Roommate_Post.objects.all()

    return render(request, 'roommate_feed.html', {'user_profile': user_profile, 'posts': posts})


@login_required(login_url='signin')
def roommate_upload(request):
    if request.method == 'POST':
        user = request.user.username
        caption = request.POST.get('caption')

        new_post = Roommate_Post.objects.create(user=user, caption=caption)

        new_post.save()

        return redirect('/roommate_feed')

    else:
        return redirect('/roommate_feed')


def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    user_community_posts = Post.objects.filter(user=pk)
    user_community_posts_len = len(user_community_posts)

    user_roommate_posts = Roommate_Post.objects.filter(user=pk)
    user_roommate_posts_len = len(user_roommate_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_community_posts_len': user_community_posts_len,
        'user_roommate_posts': user_roommate_posts,
        'user_roommate_posts_len': user_roommate_posts_len
    }

    return render(request, 'profile.html', context)

# @login_required(login_url='signin')
# def delete_post(request):
#     if request.method == 'POST':
#         user = request.user.username
#         id = request.POST.get('id')
#
#         post_to_delete = Post.objects.delete(user=user, id=id)
#
#         post_to_delete.save()
#
#         # need to update model and views to correspond with user deleting specific post, must be updated
#
#         return redirect('/')
#
#     else:
#         return redirect('/')
