from django.shortcuts import render

# Create your views here.

def landingpage(request):
    return render(request, 'landingPage/index.html')

def home(request):
    return render(request, 'landingPage/home.html')
