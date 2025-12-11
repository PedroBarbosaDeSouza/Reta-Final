from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Place, Post


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
    """
    Feed com busca por query string 'q'.
    Exemplo: /feed/?q=futebol
    Pesquisa em titulo, conteudo e autor (case-insensitive).
    """
    q = request.GET.get('q', '').strip()
    posts = Post.objects.all()

    if q:
        posts = posts.filter(
            Q(titulo__icontains=q) |
            Q(tag__icontains=q) |
            Q(autor__icontains=q)
        )

        # opcional: registrar busca se existir SearchLog (arquivo modelo pode não ter)
        if request.user.is_authenticated and q:
            try:
                from .models import SearchLog
                SearchLog.objects.create(usuario=request.user, termo=q or '', tipo='')
            except Exception:
                # se SearchLog não existir, apenas ignore
                pass

    posts = posts.order_by('-criado_em')[:30]  # limitar a 30 resultados por segurança
    return render(request, 'secundarios/feed.html', {'posts': posts, 'q': q})


def feedLog_view(request):
    """
    Feed com busca por query string 'q'.
    Exemplo: /feed/?q=futebol
    Pesquisa em titulo, conteudo e autor (case-insensitive).
    """
    q = request.GET.get('q', '').strip()
    posts = Post.objects.all()

    if q:
        posts = posts.filter(
            Q(titulo__icontains=q) |
            Q(tag__icontains=q) |
            Q(autor__icontains=q)
        )

        # opcional: registrar busca se existir SearchLog (arquivo modelo pode não ter)
        if request.user.is_authenticated and q:
            try:
                from .models import SearchLog
                SearchLog.objects.create(usuario=request.user, termo=q or '', tipo='')
            except Exception:
                # se SearchLog não existir, apenas ignore
                pass

    posts = posts.order_by('-criado_em')[:30]  # limitar a 30 resultados por segurança
    return render(request, 'secundarios/feedLog.html', {'posts': posts, 'q': q})


def searchf(request):
    if request.method == 'GET':
        if user.is_authenticated:
            return render(request, 'feedLog.html')
        else:
            return render(request, 'feed.html')
    else:
        search_query = request.POST.get('search')
    
        post = secundarios.objects.filter(name__icontains=search_query)
 
        contexto = {
            'search_query': search_query,   # o texto pesquisado
            'posts': post                # os resultados da pesquisa
        }
        if user.is_authenticated:
            return render(request, 'secundarios/feedLog.html', contexto)
        else:
            return render(request, 'secundarios/feed.html', contexto)




@login_required
def home_conta_view(request):
    # Mostrar as postagens recentes também na página principal do usuário
    q = request.GET.get('q', '').strip()
    posts = Post.objects.all()
    if q:
        from django.db.models import Q as _Q
        posts = posts.filter(
            _Q(titulo__icontains=q) |
            _Q(tag__icontains=q) |
            _Q(autor__icontains=q)
        )
    posts = posts.order_by('-criado_em')[:6]
    return render(request, 'secundarios/home_conta.html', {'posts': posts, 'q': q})


def mapa_view(request):
    return render(request, 'secundarios/mapa.html')

def mapaLog_view(request):
    return render(request, 'secundarios/mapa.html')

@login_required
def post_view(request):
    """
    Exibe uma única postagem. Espera receber o id via query string: /post/?id=123
    Se o id não for fornecido redireciona para o feed.
    """
    post_id = request.GET.get('id')
    if not post_id:
        return redirect('secundarios:feed')

    post = get_object_or_404(Post, id=post_id)

    # respostas e manipulação de comentários estão comentadas no modelo,
    # então por enquanto apenas renderizamos a postagem.
    return render(request, 'secundarios/post.html', {'post': post})

@login_required
def chats_view(request):
    return render(request, 'secundarios/chats.html')

@login_required
def busca_view(request):
    return render(request, 'secundarios/busca.html')

@login_required
def perfil_view(request):
     return render(request, 'secundarios/perfil.html')


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
