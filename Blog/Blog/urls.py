from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('Posts.urls')),  # Incluye las URLs de la aplicación `Posts`
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name='signout'),  # Cambiado de 'logout' a 'signout'
    path('', views.signin, name='signin'),
    path('my-posts/', views.my_posts, name='myPosts'),
]

# Rutas estáticas para archivos media y static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
