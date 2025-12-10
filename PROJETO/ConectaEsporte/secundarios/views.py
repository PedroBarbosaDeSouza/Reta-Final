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

    posts = posts.order_by('-criado_em')[:100]  # limitar a 100 resultados por segurança
    return render(request, 'secundarios/feed.html', {'posts': posts, 'q': q})





def searchf(request):
    if request.method == 'GET':
        return render(request, 'feed.html')
    else:
        search_query = request.POST.get('search')
        # Aqui você pode adicionar a lógica para filtrar os carros com base na pesquisa
        post = secundarios.objects.filter(name__icontains=search_query)
        # contexto é uma variável do tipo dicionário 
        # que armazena os dados a serem enviados para o template.
        # No template, você pode acessar esses dados usando as chaves do dicionário.
        contexto = {
            'search_query': search_query,   # o texto pesquisado
            'posts': post                # os resultados da pesquisa
        }
        # No meu caso, eu mostro a mesma página,
        # mas você pode usar outro template para mostrar uma página diferente.
        # Basta trocar o nome do arquivo HTML no parâmetro da função render a seguir.
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

def post_view(request):
    return render(request, 'secundarios/post.html')


def chats_view(request):
    return render(request, 'secundarios/chats.html')

@login_required
def busca_view(request):
    return render(request, 'secundarios/busca.html')

@login_required
def perfil_view(request):
     return render(request, 'secundarios/perfil.html')


# def perfil_view(request):
#     user = request.user

#     tipos_distintos = SearchLog.objects.filter(usuario=user).exclude(tipo='').values_list('tipo', flat=True).distinct()
#     tipos_count = tipos_distintos.count()

#     buscas_totais = SearchLog.objects.filter(usuario=user).count()

#     posts_count = Post.objects.filter(autor=user).count()

#     respostas_count = Resposta.objects.filter(autor=user).count()
    
#     META_TIPOS = 10
#     META_POSTS = 5
#     META_RESPOSTAS = 20

#     def pct(count, meta):
#         if meta <= 0:
#             return 0
#         value = int((count / meta) * 100)
#         return 100 if value > 100 else value
    
#     context = {
#         'tipos_count': tipos_count,
#         'buscas_totais': buscas_totais,
#         'posts_count': posts_count,
#         'respostas_count': respostas_count,
#         'pct_tipos': pct(tipos_count, META_TIPOS),
#         'pct_posts': pct(posts_count, META_POSTS),
#         'pct_respostas': pct(respostas_count, META_RESPOSTAS),
#         'META_TIPOS': META_TIPOS,
#         'META_POSTS': META_POSTS,
#         'META_RESPOSTAS': META_RESPOSTAS,
#     }
    
#     return render(request, 'secundarios/perfil.html', context)



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
