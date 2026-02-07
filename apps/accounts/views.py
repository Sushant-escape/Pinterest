from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .models import User


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Try to authenticate with username or email
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('core:home')


@login_required(login_url='accounts:login')
def profile_view(request):
    """Display user profile"""
    user = request.user
    created_pins = user.pins.filter(is_uploaded=True).order_by('-created_at')
    saved_pins = user.pins.filter(is_uploaded=False).order_by('-created_at')
    boards = user.boards.all().order_by('-created_at')
    
    return render(request, 'accounts/profile.html', {
        'user': user,
        'created_pins': created_pins,
        'saved_pins': saved_pins,
        'boards': boards
    })

@login_required(login_url='accounts:login')
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        
        # Update basic fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.bio = request.POST.get('bio', '')
        user.website = request.POST.get('website', '')
        
        # Handle profile picture upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile_edit.html', {'user': request.user})
@login_required(login_url='accounts:login')
def profile_delete(request):
    """Delete user profile"""
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('core:home')
    
    return render(request, 'accounts/profile_confirm_delete.html')
