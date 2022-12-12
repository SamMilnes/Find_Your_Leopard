from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, Roommate_Post
from django.contrib.auth.decorators import login_required
import string


'''
This is our view for the community feed
- It will grab the user who is logged in
- It will grab all the the posts created by everyone, which then gets passed into the community feed view
'''


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)

    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})


'''
This is our view for being able to delete a community post
- It will grab the user who is logged in
- If the user logged in created the community post, it gives them the ability to delete said post
'''


@login_required(login_url='signin')
def delete_comm_post(request, pk):
    user_object = User.objects.get(username=request.user.username)

    post = Post.objects.get(id=pk)

    if request.method == 'GET':
        user = request.user.username

        if user != post.user:
            return redirect('/')
        else:
            post.delete()

        return redirect('/')
    else:
        print('broken')


'''
This is our view for being able to delete a roommate post
- It will grab the user who is logged in
- If the user logged in created the roommate post, it gives them the ability to delete said post
'''


@login_required(login_url='signin')
def delete_room_post(request, pk):
    user_object = User.objects.get(username=request.user.username)
    post = Roommate_Post.objects.get(id=pk)

    if request.method == 'GET':
        user = request.user.username

        if user != post.user:
            return redirect('/roommate_feed')
        else:
            post.delete()

        return redirect('/roommate_feed')
    else:
        print('broken')


'''
This is our view for a user being able to sign up
This is how all of the user information is stored when the user signs up for the application
'''


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check to make sure the user has a wit email
        if '@wit' not in email:
            messages.info(request, 'Not a Wentworth Email')
            return redirect('signup')
            # return redirect('signup.html')

        # Check to make sure the users password is at least 8 characters
        if len(password) < 8:
            messages.info(request, 'Password must be at least 8 characters')
            return redirect('signup')

        numbers = set(list(string.digits))
        chars = set(list(password))

        # Check to see that the users password has at least one numerical character
        if not numbers.intersection(chars):
            messages.info(request, 'Password must contain at least one number')
            return redirect('signup')

        # Check to make sure that the users password and repeated password both match
        if password == password2:
            # Check to make sure the email is not already in use in the database
            if User.objects.filter(email=email).exists():
                messages.info(request, "This Email Has Already Been Taken")
                return redirect('signup')
            # Check to make sure the username is not already in use in the database
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


'''
This is our view for a user being able to sign in
'''


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticating the user from the database and login information
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Login Credentials')
            return redirect('signin')

    else:
        return render(request, 'signin.html')



'''
This is our view for a user being able to sign out of the application
'''


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


'''
This is our view for a user being able to create there own profile, including bio, gender, etc...
'''


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # if the user does not select a image for their profile, use the default image
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

            # Saving user information in the database
            user_profile.save()

        return redirect('/')
    return render(request, 'setting.html', {'user_profile': user_profile})


'''
This is our view for a user being able to create a community post
'''


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':

        # Grabbing the user and caption of the post
        user = request.user.username
        caption = request.POST.get('caption')

        # Check to make sure the user does not upload a blank post
        if caption == '':
            return redirect('/')

        new_post = Post.objects.create(user=user, caption=caption)

        # Saving new post in the database
        new_post.save()

        return redirect('/')

    else:
        return redirect('/')


'''
This is our view for the roommate feed
- It will grab the user who is logged in
- It will grab all the the roommate posts created by everyone, which then gets passed into the roommate feed view
'''


@login_required(login_url='signin')
def roommate_feed(request):
    # Getting user profile
    user_object = User.objects.get(username=request.user.username)

    user_profile = Profile.objects.get(user=user_object)

    # Grabbing all roommate posts
    posts = Roommate_Post.objects.all().order_by('-created_at')

    return render(request, 'roommate_feed.html', {'user_profile': user_profile, 'posts': posts})


'''
This is our view for a user being able to create a roommate post
'''


@login_required(login_url='signin')
def roommate_upload(request):
    if request.method == 'POST':
        # Getting user
        user = request.user.username
        # Getting post caption
        caption = request.POST.get('caption')

        # Check to make sure the user does not upload a blank post
        if caption == '':
            return redirect('/')

        new_post = Roommate_Post.objects.create(user=user, caption=caption)

        # Saving post in the database
        new_post.save()

        return redirect('/roommate_feed')

    else:
        return redirect('/roommate_feed')


'''
This is our view for the user profiles
'''


def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    user_community_posts = Post.objects.filter(user=pk)
    user_community_posts_len = len(user_community_posts)

    user_roommate_posts = Roommate_Post.objects.filter(user=pk)
    user_roommate_posts_len = len(user_roommate_posts)

    # Passing in all user profile information
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_community_posts_len': user_community_posts_len,
        'user_roommate_posts': user_roommate_posts,
        'user_roommate_posts_len': user_roommate_posts_len
    }

    return render(request, 'profile.html', context)

