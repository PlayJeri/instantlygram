from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Profile, Meep
from django.contrib.auth.models import User
from .forms import MeepForm, RegisterForm, CommentForm, ProfilePictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            meep_form = MeepForm(request.POST, request.FILES)
            if meep_form.is_valid():
                meep = meep_form.save(commit=False)
                meep.user = request.user
                if 'meep_image_url' in request.FILES:
                    meep.meep_image_url = request.FILES['meep_image_url']
                meep.save()
                return redirect('home')
            
        current_user = request.user.profile
        meep_form = MeepForm()
        comment_form = CommentForm()
        suggested_users = User.objects.order_by('?')[:5]
        meeps = Meep.objects.filter(user__profile__in=current_user.follows.all()).order_by("-created_at")
        paginator = Paginator(meeps, 5)
        page = request.GET.get('page')
        meeps = paginator.get_page(page)

        context = {
            "meeps":meeps,
            "meep_form":meep_form,
            "comment_form":comment_form,
            "suggested_users":suggested_users
        }

        return render(request, 'musker/home.html', context)
    
    else:
        return redirect('login')

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'musker/profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, "You must be logged in to view this page!", extra_tags='warning')
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        return render(request, "musker/profile.html", {
            "profile":profile,
            "meeps":meeps,
        })
    else:
        messages.success(request, "You must be logged in to view this page!", extra_tags='success')
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials", extra_tags='danger')
            return redirect('login')

    else:
        return render(request, 'musker/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out", extra_tags='success')
    return redirect('home')
    
def follow(request):
    id = request.GET.get('id')
    current_user = request.user.profile
    current_user.follows.add(id)
    redirect_id = request.GET.get('user_id')

    return redirect('profile', pk=redirect_id)

def unfollow(request):
    id = request.GET.get('id')
    current_user = request.user.profile
    current_user.follows.remove(id)
    redirect_id = request.GET.get('user_id')

    return redirect('profile', pk=redirect_id)

def register_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You are now logged in", extra_tags='success')

            return redirect('home')

    return render(request, 'musker/register.html', {'form':form})

@login_required(login_url='login')
def update_user(request):
    current_user = User.objects.get(id=request.user.id)
    profile_user = Profile.objects.get(user__id=request.user.id)
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES, instance=current_user)
        pp_form = ProfilePictureForm(request.POST, request.FILES, instance=profile_user)

        if pp_form.is_valid() and form.is_valid():
            pp_form.save()
            form.save()
            login(request, current_user)

            messages.success(request, "User updated successfully", extra_tags='success')
            return redirect('profile', pk=current_user.id)
    else:
        form = RegisterForm(instance=current_user)
        pp_form = ProfilePictureForm()
    return render(request, 'musker/update_user.html', {'form':form, 'ppf':pp_form})



@login_required
def comment(request, meep_id):
    comment_data = {'body': '', 'user': '', 'created_at': ''}
    form = CommentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.meep = Meep.objects.get(id=meep_id)
            comment.save()
            comment_data['body'] = comment.body
            comment_data['user'] = comment.user.username
            comment_data['created_at'] = comment.created_at
            return JsonResponse({'success': True, 'comment': comment_data})
    else:
        return JsonResponse({'success': False})

@login_required
def like(request, meep_id):
    meep = Meep.objects.get(id=meep_id)
    if request.user in meep.likes.all():
        meep.likes.remove(request.user)
        return JsonResponse({'like': False})

    else:
        meep.likes.add(request.user)
        return JsonResponse({'like': True})


@login_required
def search(request, search_query):
    if not search_query:
        return JsonResponse({'error': 'Missing search query parameter'})
    users = User.objects.filter(username__icontains=search_query)[:3]

    users = {
        'users': [{'username': user.username, 'user_id': user.id} for user in users]
    }
    return JsonResponse(users)