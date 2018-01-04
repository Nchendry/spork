from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Item
from django.contrib import messages



def index(request):
    return render(request, "dos/index.html")

def login(request):
    result = User.objects.login(request.POST)
    print "test"
    if result[0]:
        request.session['user_id'] = result[1].id    
        # id = str(request.session['id'])
        return redirect("/home")
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect('/')

def registration(request):
    return render(request, "dos/register.html")

def register(request):
    result = User.objects.validate_registration(request.POST)
    if result[0]:
        request.session['user_id'] = result[1].id
        return redirect("/home")
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect('/registration')

def logout(request):
    def logout(request):
        request.session.clear()
    return redirect('/')

def home(request):
    user = User.objects.get(id=request.session['user_id'])
    all_items = Item.objects.all()
    my_items = Item.objects.filter(wisher_lister = user) 
    my_wishes = Item.objects.filter(also_wants = user)
    other_items = all_items.exclude(wisher_lister = user)
    other_items = other_items.exclude(also_wants = user)
    context = {
        'user': user,
        'my_items': my_items,
        'my_wishes': my_wishes,
        'other_items': other_items,
    }
    return render(request, "dos/home.html", context)

def additem(request):
    return render(request, "dos/additem.html")

def createitem(request):
    id = request.session['user_id']
    result = Item.objects.validateItem(request.POST, id)
    if result[0]:
        return redirect("/home")
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect("/additem")

def item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {
        'item': item
    }
    return render(request, "dos/item.html", context)

def addwishlist(request, item_id):
    user = User.objects.get(id = request.session['user_id'])
    item = Item.objects.get(id = item_id)
    user.wanted_by.add(item)
    return redirect('/home')

def remove(request, item_id):
    user = User.objects.get(id = request.session['user_id'])
    item = Item.objects.get(id = item_id)
    user.wanted_by.remove(item)
    return redirect('/home')

def delete(request, item_id):
    item = Item.objects.get(id = item_id)
    item.delete()    
    return redirect('/home')


