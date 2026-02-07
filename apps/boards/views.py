from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Board
from .forms import BoardForm

@login_required
def board_list(request):
    """List all user's boards"""
    boards = Board.objects.filter(user=request.user)
    return render(request, 'boards/board_list.html', {'boards': boards})

def board_detail(request, board_id):
    """View a board and its pins"""
    board = get_object_or_404(Board, id=board_id)
    pins = board.pins.all()
    
    # Check privacy
    if board.is_private and board.user != request.user:
        messages.error(request, 'This board is private.')
        return redirect('core:home')
    
    is_owner = board.user == request.user
    return render(request, 'boards/board_detail.html', {
        'board': board, 
        'pins': pins,
        'is_owner': is_owner
    })

@login_required
def board_create(request):
    """Create a new board"""
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            messages.success(request, 'Board created successfully!')
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = BoardForm()
    return render(request, 'boards/board_form.html', {'form': form, 'action': 'Create'})

@login_required
def board_edit(request, board_id):
    """Edit an existing board"""
    board = get_object_or_404(Board, id=board_id, user=request.user)
    
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board updated successfully!')
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)
    
    return render(request, 'boards/board_form.html', {'form': form, 'board': board, 'action': 'Edit'})

@login_required
def board_delete(request, board_id):
    """Delete a board"""
    board = get_object_or_404(Board, id=board_id, user=request.user)
    
    if request.method == 'POST':
        board.delete()
        messages.success(request, 'Board deleted successfully!')
        return redirect('boards:board_list')
    
    return render(request, 'boards/board_confirm_delete.html', {'board': board})
