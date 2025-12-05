from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('O usuário precisa ter um email válido')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    

# class Pessoa(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField('email', unique=True)
#     first_name = models.CharField('nome', max_length=150, blank=True)
#     last_name = models.CharField('sobrenome', max_length=150, blank=True)
#     is_active = models.BooleanField('ativo', default=True)
#     is_staff = models.BooleanField('membro da equipe', default=False)
#     date_joined = models.DateTimeField('data de entrada', auto_now_add=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

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

# class Post(models.Model):
#     autor = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='posts')
#     titulo = models.CharField(max_length=200)
#     conteudo = models.TextField()
#     criado_em = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-criado_em']
    
#     def __str__(self):
#         return self.titulo

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


class Local(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome