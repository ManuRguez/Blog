# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Favorite
from django.core.paginator import Paginator
from django.utils.text import slugify
import uuid


class HomeViewTestCase(TestCase):
    def setUp(self):
        # Crear un usuario para autenticar
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Crear otro usuario
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')

        # Crear algunos posts
        for i in range(10):  # Crear 10 posts
            Post.objects.create(
                title=f'Post {i+1}',
                subtitle=f'Subtitle {i+1}',
                description=f'Description of Post {i+1}',
                author=self.user
            )

        # Crear un favorito
        favorite_post = Post.objects.first()
        Favorite.objects.create(user=self.user, post=favorite_post)

        # URL de la vista home
        self.url = reverse('home')  # Asegúrate de que 'home' es el nombre de la vista en urls.py

    def test_login_required(self):
        # Intentar acceder a la vista sin autenticarse
        response = self.client.get(self.url)
        # La respuesta debe redirigir al login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)  # Asegúrate de que coincide con tu configuración

    def test_home_view_authenticated(self):
        # Autenticar al usuario
        self.client.login(username='testuser', password='testpass')

        # Hacer la solicitud GET a la vista home
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # La vista debe cargar correctamente

        # Verificar que los posts están en el contexto
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj']), 6)  # La paginación debe limitar a 6 posts

        # Verificar que los favoritos están en el contexto
        self.assertIn('favorites', response.context)
        self.assertEqual(response.context['favorites'].count(), 1)  # Solo 1 post es favorito

    def test_pagination(self):
        # Autenticar al usuario
        self.client.login(username='testuser', password='testpass')

        # Solicitar la segunda página de los posts
        response = self.client.get(self.url, {'page': 2})
        self.assertEqual(response.status_code, 200)

        # Verificar que hay 4 posts en la segunda página (10 totales, 6 en la primera página)
        self.assertEqual(len(response.context['page_obj']), 4)

def test_favorites_for_logged_in_user(self):
    # Autenticar al usuario
    self.client.login(username='testuser', password='testpass')

    # Crear un post como favorito
    favorite_post = Post.objects.first()  # Tomar el primer post creado
    Favorite.objects.create(user=self.user, post=favorite_post)

    # Hacer la solicitud GET a la vista home
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)

    # Verificar que el usuario solo ve sus favoritos
    favorite_titles = [post.title for post in response.context['favorites']]
    self.assertIn('Post 1', favorite_titles)  # Ahora debería encontrarse "Post 1" en los favoritos


class PostViewTestCase(TestCase):
    def setUp(self):
        # Crear usuarios
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')

        # Crear un post
        self.post = Post.objects.create(
            title="Post de prueba",
            subtitle="Subtítulo del post",
            description="Descripción del post de prueba",
            author=self.user
        )
        
        # URL de la vista post, asumiendo que el nombre de la URL es 'post' y se pasa un 'pk' (id del post)
        self.url = reverse('post', kwargs={'pk': self.post.id})

    def test_login_required(self):
        """ Verificar que la vista de post requiere estar autenticado """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Debería redirigir al login
        self.assertIn('/accounts/login/', response.url)  # Verificar que redirige a login

    def test_view_post_authenticated(self):
        """ Verificar que un usuario autenticado puede ver el post """
        self.client.login(username='testuser', password='testpass')  # Iniciar sesión
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Debería devolver un 200 OK
        self.assertContains(response, 'Post de prueba')  # Verificar que el título del post está en la respuesta

    def test_view_post_as_author(self):
        """ Verificar que un usuario autenticado puede ver un post y que es el autor """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post de prueba')
        self.assertTrue(response.context['is_author'])  # Verificar que el usuario es el autor del post

    def test_view_post_as_non_author(self):
        """ Verificar que un usuario autenticado que no es autor no tiene privilegios especiales """
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post de prueba')
        self.assertFalse(response.context['is_author'])  # Verificar que el usuario no es el autor



class PostViewTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user2 = User.objects.create_user(username="otheruser", password="password456")
        # Crear un post de prueba
        self.post = Post.objects.create(
            id=uuid.uuid4(),
            title="Test Post",
            subtitle="Test Subtitle",
            description="This is a test description",
            author=self.user
        )

    def test_delete_post_authenticated(self):
        """Verifica que un usuario autenticado pueda eliminar un post"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("deletePost", args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 302)  # Redirección tras eliminar el post
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())  # El post debe eliminarse

    def test_delete_post_unauthenticated(self):
        """Verifica que un usuario no autenticado no pueda eliminar un post"""
        response = self.client.post(reverse("deletePost", args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 302)  # Debe redirigir al login
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())  # El post debe seguir existiendo

    def test_update_post_authenticated(self):
        """Verifica que un usuario autenticado pueda actualizar un post"""
        self.client.login(username="testuser", password="password123")
        new_data = {
            "title": "Updated Title",
            "subtitle": "Updated Subtitle",
            "description": "Updated description"
        }
        response = self.client.post(reverse("updatePost", args=[str(self.post.id)]), new_data)
        self.assertEqual(response.status_code, 302)  # Redirección tras actualizar
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_add_favorite_authenticated(self):
        """Verifica que un usuario autenticado pueda añadir un post a favoritos"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("add_favorite", args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 302)  # Redirección tras añadir a favoritos
        self.assertTrue(Favorite.objects.filter(user=self.user, post=self.post).exists())  # Relación creada

    def test_remove_favorite_authenticated(self):
        """Verifica que un usuario autenticado pueda eliminar un post de favoritos"""
        # Agregar el post a favoritos primero
        Favorite.objects.create(user=self.user, post=self.post)
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("remove_favorite", args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 302)  # Redirección tras eliminar de favoritos
        self.assertFalse(Favorite.objects.filter(user=self.user, post=self.post).exists())  # Relación eliminada

    def test_favorites_authenticated(self):
        """Verifica que los posts favoritos de un usuario se muestren correctamente"""
        # Agregar el post a favoritos
        Favorite.objects.create(user=self.user, post=self.post)
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)  # Página cargada exitosamente
        self.assertContains(response, self.post.title)  # El título del post debe estar en la respuesta

    def test_post_search(self):
        """Verifica que la búsqueda de posts funcione correctamente"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("post_search"), {"query": "Test"})
        self.assertEqual(response.status_code, 200)  # Página cargada exitosamente
        self.assertContains(response, self.post.title)  # El título del post debe estar en la respuesta

class FormularioPostViewTestCase(TestCase):
    def setUp(self):
        # Crear usuarios
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # URL de la vista formulario (corrige 'formulario' a 'formPost')
        self.url = reverse('formPost')  # Cambiado a 'formPost' según urls.py

    def test_login_required(self):
        """ Verificar que el formulario requiere estar autenticado """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirige al login si no está autenticado
        self.assertIn('/accounts/login/', response.url)  # Verifica que redirige al login

    def test_create_post_authenticated(self):
        """ Verificar que un usuario autenticado puede crear un post """
        self.client.login(username='testuser', password='testpass')
        
        data = {
            'title': 'Nuevo Post',
            'subtitle': 'Subtítulo del post',
            'description': 'Contenido del post',
            # Omite 'image_portada' si no estás probando con una imagen
        }
        response = self.client.post(self.url, data)

        # Verificar que se redirige a la página de inicio después de guardar el post
        self.assertRedirects(response, reverse('home'))

        # Verificar que el post se ha creado en la base de datos
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'Nuevo Post')





