from django.shortcuts import render

def home(request):
    return render(request, 'ConectaEsporte/home.html')