from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Pin
from .forms import PinForm

def pin_detail(request, pin_id):
    """View a single pin"""
    pin = get_object_or_404(Pin, id=pin_id)
    return render(request, 'pins/pin_detail.html', {'pin': pin})

@login_required
def pin_create(request):
    """Create a new pin"""
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user
            pin.save()
            messages.success(request, 'Pin created successfully!')
            return redirect('pins:pin_detail', pin_id=pin.id)
    else:
        form = PinForm(user=request.user)
    return render(request, 'pins/pin_form.html', {'form': form, 'action': 'Create'})

@login_required
def pin_edit(request, pin_id):
    """Edit an existing pin"""
    pin = get_object_or_404(Pin, id=pin_id, user=request.user)
    
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES, instance=pin, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pin updated successfully!')
            return redirect('pins:pin_detail', pin_id=pin.id)
    else:
        form = PinForm(instance=pin, user=request.user)
    
    return render(request, 'pins/pin_form.html', {'form': form, 'pin': pin, 'action': 'Edit'})

@login_required
def pin_delete(request, pin_id):
    """Delete a pin"""
    pin = get_object_or_404(Pin, id=pin_id, user=request.user)
    
    if request.method == 'POST':
        pin.delete()
        messages.success(request, 'Pin deleted successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'pins/pin_confirm_delete.html', {'pin': pin})

@login_required
def pin_save(request, pin_id):
    """Save/unsave a pin (AJAX endpoint)"""
    if request.method == 'POST':
        pin = get_object_or_404(Pin, id=pin_id)
        # This could be extended to add pins to user's saved collection
        # For now, just return success
        return JsonResponse({'success': True, 'message': 'Pin saved!'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
