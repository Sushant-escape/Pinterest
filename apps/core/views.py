import requests
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from apps.pins.models import Pin


class UnsplashImage:
    def __init__(self, url):
        self.url = url

class UnsplashUser:
    def __init__(self, data):
        self.username = data['username']
        self.profile_image = UnsplashImage(data['profile_image']['medium'])

class UnsplashPin:
    def __init__(self, data):
        self.id = data['id']
        self.title = data.get('description') or data.get('alt_description') or "Unsplash Image"
        self.image = UnsplashImage(data['urls']['regular'])
        self.user = UnsplashUser(data['user'])
        self.is_external = True
        self.remote_link = data['links']['html']

def search_unsplash(query):
    if not settings.UNSPLASH_ACCESS_KEY:
        return None  # Explicitly return None to indicate missing key

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": settings.UNSPLASH_ACCESS_KEY,
        "per_page": 20,
        "content_filter": "high",  # Filter out inappropriate content
        "order_by": "relevant",  # Get most relevant results first
        "orientation": "landscape"  # Prefer landscape images for better display
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [UnsplashPin(item) for item in data.get('results', [])]
        else:
            print(f"Unsplash API Error: Status {response.status_code}")
    except Exception as e:
        print(f"Unsplash API Error: {e}")
    
    return []


def home(request):
    """Home page view with search"""
    query = request.GET.get('q')
    missing_key = False
    
    # Strip whitespace if query exists
    if query:
        query = query.strip()
    
    if query:
        # Local search
        local_pins = list(Pin.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct())
        
        # Unsplash search
        api_pins = search_unsplash(query)
        
        if api_pins is None:
            # API key is missing
            missing_key = True
            api_pins = []
            
        pins = local_pins + api_pins
    else:
        pins = Pin.objects.all().order_by('-created_at')
    
    return render(request, 'base/home.html', {
        'pins': pins, 
        'query': query,
        'missing_key': missing_key
    })
    

def explore(request):
    """Explore page view"""
    pins = Pin.objects.all().order_by('?')
    return render(request, 'base/explore.html', {'pins': pins})


def download_unsplash_image(request):
    """Download Unsplash image via backend to avoid CORS issues"""
    from django.http import HttpResponse, JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    import io
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    image_url = request.POST.get('image_url')
    filename = request.POST.get('filename', 'unsplash_image.jpg')
    
    if not image_url:
        return JsonResponse({'error': 'No image URL provided'}, status=400)
    
    try:
        # Download the image from Unsplash
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            # Return the image as a downloadable file
            http_response = HttpResponse(response.content, content_type='image/jpeg')
            http_response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return http_response
        else:
            return JsonResponse({'error': 'Failed to download image'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def save_unsplash_to_board(request):
    """Save an Unsplash image to a user's board"""
    from django.http import JsonResponse
    from django.core.files.base import ContentFile
    from django.contrib.auth.decorators import login_required
    import urllib.parse
    
    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to save images'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    image_url = request.POST.get('image_url')
    title = request.POST.get('title', 'Untitled')
    board_id = request.POST.get('board_id')
    author = request.POST.get('author', '')
    
    if not image_url:
        return JsonResponse({'error': 'No image URL provided'}, status=400)
    
    try:
        # Download the image from Unsplash
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to download image'}, status=500)
        
        # Create a new pin
        pin = Pin()
        pin.title = title
        pin.description = f"From Unsplash by {author}" if author else "From Unsplash"
        pin.link = image_url
        pin.user = request.user
        pin.is_uploaded = False
        
        # Set board if provided
        if board_id:
            try:
                from apps.boards.models import Board
                board = Board.objects.get(id=board_id, user=request.user)
                pin.board = board
            except Board.DoesNotExist:
                pass
        
        # Save the image file
        filename = f"{title.replace(' ', '_')[:50]}.jpg"
        pin.image.save(filename, ContentFile(response.content), save=True)
        
        return JsonResponse({
            'success': True,
            'pin_id': pin.id,
            'message': 'Image saved successfully!'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

