from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Place
#,Post, Resposta, SearchLog

# Views de cada página secundária
def criaConta_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('secundarios:home_conta')
    else:
        form = SignUpForm()
    return render(request, 'secundarios/criaConta.html', {'form': form})

def feed_view(request):
    posts = Post.objects.select_related('autor').all()
    return render(request, 'secundarios/feed.html', {'posts': posts})

def home_conta_view(request):
    return render(request, 'secundarios/home_conta.html')

def login_view(request):
    return render(request, 'secundarios/login.html')

def mapa_view(request):
    return render(request, 'secundarios/mapa.html')

def post_view(request):
    return render(request, 'secundarios/post.html')

# def perfil_view(request):
#     return render(request, 'secundarios/perfil.html')

def chats_view(request):
    return render(request, 'secundarios/chats.html')

@login_required(login_url='/secundarios/login/')
def busca_view(request):
    return render(request, 'secundarios/busca.html')

#@login_required
def perfil_view(request):
    user = request.user

    tipos_distintos = SearchLog.objects.filter(usuario=user).exclude(tipo='').values_list('tipo', flat=True).distinct()
    tipos_count = tipos_distintos.count()

    buscas_totais = SearchLog.objects.filter(usuario=user).count()

    posts_count = Post.objects.filter(autor=user).count()

    respostas_count = Resposta.objects.filter(autor=user).count()
    
    META_TIPOS = 10
    META_POSTS = 5
    META_RESPOSTAS = 20

    def pct(count, meta):
        if meta <= 0:
            return 0
        value = int((count / meta) * 100)
        return 100 if value > 100 else value
    
    context = {
        'tipos_count': tipos_count,
        'buscas_totais': buscas_totais,
        'posts_count': posts_count,
        'respostas_count': respostas_count,
        'pct_tipos': pct(tipos_count, META_TIPOS),
        'pct_posts': pct(posts_count, META_POSTS),
        'pct_respostas': pct(respostas_count, META_RESPOSTAS),
        'META_TIPOS': META_TIPOS,
        'META_POSTS': META_POSTS,
        'META_RESPOSTAS': META_RESPOSTAS,
    }
    
    return render(request, 'secundarios/perfil.html', context)



# post_view não estava funcionando, então comentei por enquanto
# def post_view(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     respostas = post.respostas.select_related('autor').all()

#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return redirect('secundarios:login')
#         conteudo = request.POST.get('conteudo')
#         if conteudo:
#             Resposta.objects.create(post=post, autor=request.user, conteudo=conteudo)
#             return redirect('secundarios:post', post_id=post.id)
#     return render(request, 'secundarios/post.html', {'post': post, 'respostas': respostas})

# def novo_post_view(request):
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return redirect('secundarios:login')
#         titulo = request.POST.get('titulo')
#         conteudo = request.POST.get('conteudo')

#         if titulo and conteudo:
#             post = Post.objects.create(autor=request.user, titulo=titulo, conteudo=conteudo)
#             return redirect('secundarios:post', post_id=post.id)
#     return render(request, 'secundarios/novo_post.html')

def places_api(request):
    qs = Place.objects.filter(ativo=True)
    q = request.GET.get('q')
    tipo = request.GET.get('tipo')
    ativo = request.GET.get('ativo')

    if q or tipo:
        if request.user.is_authenticated:
            SearchLog.objects.create(usuario=request.user, termo=q or '', tipo=tipo or '')
    if ativo in ('0', '1'):
        qs = qs.filter(ativo=(ativo == '1'))
    
    qs = qs[:1000]

    data = []
    for p in qs:
        data.append({
            'id': p.id,
            'nome': p.nome,
            'descricao': p.descricao,
            'endereco': p.endereco,
            'lat': float(p.latitude),
            'lng': float(p.longitude),
            'tipo': p.tipo,
        })
    return JsonResponse({'results': data})
