from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt #delete when possible

@csrf_exempt #delete when possible
def home_page(request):
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
