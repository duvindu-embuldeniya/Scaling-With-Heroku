from django.shortcuts import render, redirect
from . forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

def home(request):
    return render(request, 'home/index.html')



def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = new_user.username
            new_user.username = username.lower()
            new_user.save()
            auth.login(request, new_user)
            messages.success(request, "User created successfully!")
            return redirect('home')
        # else:
            # messages.error(request, "Something went wrong,Try Again!")
            # return redirect('register')
    context = {'form':form}
    return render(request, 'home/register.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You've already Loged-In!")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username = username, password = password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, "Successfully Loged-In!")
            return redirect('home')
        else:
            messages.error(request, "User doesn't exist!")
            return redirect('login')
    return render(request, 'home/login.html')



def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You've not Loged-In")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "Successfully Loged-Out!")
    return redirect('home')



@login_required
def profile(request, username):
    current_user = User.objects.get(username = username)
    if current_user.username != request.user.username:
        return HttpResponse("<h1>403</h1>")
    context = {'current_user':current_user}
    return render(request, 'home/profile.html', context)



@login_required
def profile_update(request,username):
    current_user = User.objects.get(username = username)
 
    if current_user.username != request.user.username:
        return HttpResponse("<h1>403</h1>")
    u_form = UserUpdateForm(instance=current_user)
    p_form = ProfileUpdateForm(instance=current_user.profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=current_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=current_user.profile)

        if u_form.is_valid() and p_form.is_valid():
            updated_user = u_form.save()
            p_form.save()
            messages.success(request, "Profile Updated Successfully !")
            return redirect('profile', username = updated_user.username)
        else:
            messages.error(request, "Something Went Wrong!")
            # return redirect('profile_update', username = current_user.username)
    context = {'current_user':current_user, 'u_form':u_form ,'p_form':p_form}
    return render(request, 'home/profile_update.html', context)




@login_required
def profile_delete(request,username):
    current_user = User.objects.get(username = username)
    if current_user.username != request.user.username:
        return HttpResponse("<h1>403</h1>")
    if request.method == 'POST':
        current_user.delete()
        messages.success(request, "Account Deleted Successfully!")
        return redirect('home')
    context = {'current_user':current_user}
    return render(request, 'home/profile_delete.html', context)
