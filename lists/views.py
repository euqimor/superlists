from django.shortcuts import redirect, render
from lists.models import Item
from django.views.decorators.csrf import csrf_exempt #delete when possible

@csrf_exempt #delete when possible
def home_page(request):
    return render(request, 'home.html')


@csrf_exempt #delete when possible
def view_list(request):

    items = Item.objects.all()
    return render(request, 'list.html', {
        'items': items
    })

@csrf_exempt #delete when possible
def new_list(request):

    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')



