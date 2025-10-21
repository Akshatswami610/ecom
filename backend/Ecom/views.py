from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def product(request):
    return render(request,'product.html')

def aboutus(request):
    return render(request,'aboutus.html')

def contact(request):
    return render(request,'contact.html')

def profile(request):
    return render(request,'profile.html')

def orders(request):
    return render(request,'orders.html')

def cart(request):
    return render(request,'cart.html')

def trackorder(request):
    return render(request,'trackorder.html')