from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Place, Post, Resposta

# Views de cada página secundária
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

def feed_view(request):
    return render(request, 'secundarios/feed.html')

def home_conta_view(request):
    return render(request, 'secundarios/home_conta.html')

def login_view(request):
    return render(request, 'secundarios/login.html')

def mapa_view(request):
    return render(request, 'secundarios/mapa.html')

@login_required
def perfil_view(request):
    return render(request, 'secundarios/perfil.html')

<<<<<<< HEAD
def places_api(request):
    "retorna JSON com base no nome, filtros e se está aberto"
    qs = Place.objects.filter(ativo=True)
    q = request.GET.get('q')
    tipo = request.GET.get('tipo')
    ativo = request.GET.get('ativo')

    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(descricao__icontains=q) | Q(endereco__icontains=q))
    if tipo:
        qs = qs.filter(tipo=tipo)
    if ativo in ('0', '1'):
        qs = qs.filter(ativo=(ativo == '1'))
    
    qs = qs[:1000]

    data = []
    for p in qs:
        data.append({
            'id':p.id,
            'nome':p.nome,
            'descricao':p.descricao,
            'endereco':p.endereco,
            'lat':float(p.latitude),
            'lng':float(p.longitude),
            'tipo':p.tipo,
        })
    return JsonResponse({'results':data})

def feed_view(request):
    posts = Post.objects.select_related('autor').all()
    return render(request, 'secundarios/feed.html', {'posts': posts})

def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    respostas = post.respostas.select_related('autor').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('secundarios:login')
        conteudo = request.POST.get('conteudo')
        if conteudo:
            Resposta.objects.create(post=post, autor=request.user, conteudo=conteudo)
            return redirect('secundarios:post', post_id=post.id)
    return render(request, 'secundarios/post.html', {'post': post, 'respostas': respostas})

@login_required
def novo_post_view(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        if titulo and conteudo:
            Post.objects.create(autor=request.user, titulo=titulo, conteudo=conteudo)
            return redirect('secundarios:feed')
    return render(request, 'secundarios/novo_post.html')  "Ainda não existe novo_post.html"
=======
def post_view(request):
    return render(request, 'secundarios/post.html')
>>>>>>> 6c7c68a4d1cce974ea0930d3106830beec5f032e
