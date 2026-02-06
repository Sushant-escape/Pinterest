from django.shortcuts import render


def home(request):
    """Home page view"""
    return render(request, 'base/home.html')


def explore(request):
    """Explore page view"""
    return render(request, 'base/explore.html')
