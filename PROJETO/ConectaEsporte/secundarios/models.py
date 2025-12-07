from django.db import models
#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Place(models.Model):

    SPORT_CHOICES = [
        ('futebol', 'Futebol'),
        ('basquete', 'Basquete'),
        ('volei', 'Vôlei'),
        ('tenis', 'Tênis'),
        ('corrida', 'Corrida'),
        ('natação', 'Natação'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    tipo = models.CharField(max_length=30, choices=SPORT_CHOICES, default='outro')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, blank=True)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} ({self.autor})"


















# class Resposta(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='respostas')
#     autor = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
#     conteudo = models.TextField()
#     criado_em = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['criado_em']
    
#     def __str__(self):
#         return f"Resposta de {self.autor.email} em {self.post}"

# class SearchLog(models.Model):
#     " Registra as buscas feitas pelos usuários no mapa, pra ser aplicado na barra de progreso"
#     usuario = models.ForeignKey(Pessoa, null=True, blank=True, on_delete=models.CASCADE, related_name='search_logs')
#     termo = models.CharField(max_length=200, blank=True)
#     tipo = models.CharField(max_length=100, blank=True)
#     criado_em = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-criado_em']
   
#     def __str__(self):
#         return f"{self.usuario or 'anon'} - {self.tipo or self.termo or 'busca'}"


