from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

# Views de cada página secundária
def mapa_view(request):
    return render(request, 'secundarios/mapa.html')
def login_view(request):
    return render(request, 'secundarios/login.html')

def criaConta_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form_is_valid():
            user = form.save()
            login(request, user)
            return redirect('home.html')
    else:
        form = SignUpForm()
    return render(request, 'secundarios/criaConta.html', {'form': form})

@login_required
def perfil_view(request):
    return render(request, 'secundarios/perfil.html')