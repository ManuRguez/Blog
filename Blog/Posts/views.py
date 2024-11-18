from django.shortcuts import render, redirect,get_object_or_404
from .models import Favorite, Post
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def home(request):
    posts = Post.objects.all()  # Obtener todos los posts para mostrar
    favorites = Post.objects.filter(favorite__user=request.user)  # Filtrar los posts favoritos del usuario
    paginator = Paginator(posts, 6)  # Paginación: Mostrar 6 posts por página
    page_number = request.GET.get('page')  # Obtener el número de la página de la URL
    page_obj = paginator.get_page(page_number)  # Obtenemos la página solicitada

    # Pasar los posts paginados a la plantilla
    context = {'page_obj': page_obj, 'favorites': favorites}
    return render(request, 'Posts/posts_page.html', context)



@login_required
# Vista para ver un post específico
def post(request, pk):
    # Obtener el post, si no existe, devolver un 404
    post = get_object_or_404(Post, id=pk)
    
    # Verificar si el usuario autenticado es el autor del post
    is_author = post.author == request.user
    
    # Contexto con el post y si el usuario es el autor
    context = {
        'post': post,
        'is_author': is_author,
    }
    
    return render(request, 'Posts/post.html', context)

@login_required
# Vista para el formulario de nuevo post
def formulario(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)  # Pasamos el usuario al formulario
        if form.is_valid():
            form.save()  # Aquí el campo 'author' ya se asigna automáticamente
            return redirect('home')
    else:
        form = PostForm(user=request.user)  # También pasamos el usuario cuando el formulario se carga

    context = {'form': form}
    return render(request, 'posts/addPost.html', context)

@login_required
# Vista para eliminar un post
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    context = {'post': post}
    return render(request, 'posts/deletePost.html', context)

@login_required
# Vista para actualizar un post
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        form.save()
        return redirect('home')
    context = {"form": form, "update": True}
    return render(request, 'posts/addPost.html', context)

# Vista para el registro de usuarios
def register(request):
    if request.method == 'GET':
        return render(request, 'posts/register.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
                r
            except IntegrityError:
                return render(request, 'posts/register.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
        return render(request, 'posts/register.html', {
            'form': UserCreationForm,
            "error": 'Passwords do not match'
        })

@login_required
# Vista para cerrar sesión
def signout(request):
    logout(request)
    return redirect('/')  # Redirige al login después de cerrar sesión

# Vista para iniciar sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'Posts/login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'Posts/login.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')  # Redirige a la página principal después de iniciar sesión

@login_required
def my_posts(request):
    # Filtra los posts del usuario autenticado
    posts = Post.objects.filter(author=request.user)  

    # Configuración de la paginación
    paginator = Paginator(posts, 6)  # 6 posts por página (ajustalo según lo que necesites)
    page_number = request.GET.get('page')  # Obtiene el número de la página actual desde la query string
    page_obj = paginator.get_page(page_number)  # Obtiene el objeto de la página actual

    return render(request, 'Posts/my_posts.html', {'page_obj': page_obj})  # Pasa el objeto page_obj a la plantilla


@login_required
def add_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Usa 'pk' que será un UUID
    # Verificar si ya es favorito
    if not Favorite.objects.filter(user=request.user, post=post).exists():
        Favorite.objects.create(user=request.user, post=post)
    return redirect('home')

@login_required
def remove_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Usa 'pk' que será un UUID
    # Eliminar el post de favoritos
    Favorite.objects.filter(user=request.user, post=post).delete()
    return redirect('home')

from django.core.paginator import Paginator

@login_required
def favorites(request):
    # Filtrar los posts favoritos del usuario
    favorite_posts = Post.objects.filter(favorite__user=request.user)

    # Configuración de la paginación
    paginator = Paginator(favorite_posts, 6)  # 6 posts por página
    page_number = request.GET.get('page')  # Obtiene el número de la página actual
    page_obj = paginator.get_page(page_number)  # Obtiene el objeto de la página actual

    return render(request, 'Posts/favorites.html', {'page_obj': page_obj})  # Pasa el objeto de la página a la plantilla




@login_required
def post_search(request):
    query = request.GET.get('query', '')

    if query:
        # Filtramos los posts que contienen la consulta en el título o subtítulo
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(subtitle__icontains=query)
        )
    else:
        # Si no hay búsqueda, mostramos todos los posts
        posts = Post.objects.all()

    print(f'Posts encontrados: {posts.count()}')  # Esto debe mostrar la cantidad de posts encontrados

    # Paginación: Mostrar 6 posts por página
    paginator = Paginator(posts, 6)  # 6 posts por página
    page_number = request.GET.get('page')  # Obtener el número de la página de la URL
    page_obj = paginator.get_page(page_number)  # Obtenemos la página solicitada

    print(f'Página actual: {page_obj.number}, Total de páginas: {page_obj.paginator.num_pages}')  # Para ver qué página se está mostrando

    # Obtener los favoritos del usuario
    favorites = Post.objects.filter(favorite__user=request.user)

    return render(request, 'Posts/posts_page.html', {
        'page_obj': page_obj,  # Pasamos los posts paginados a la plantilla
        'favorites': favorites
    })
