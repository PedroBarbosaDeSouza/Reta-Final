from django.shortcuts import render

# Views de cada página secundária
def mapa_view(request):
    return render(request, 'secundarios/mapa.html')

def login_view(request):
    return render(request, 'secundarios/login.html')

def criaConta_view(request):
    return render(request, 'secundarios/criaConta.html')