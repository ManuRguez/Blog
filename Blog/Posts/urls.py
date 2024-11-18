from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('post/<str:pk>', views.post, name="post"),
    path('form_post/', views.formulario, name="formPost"),
    path('delete_post/<str:pk>/', views.deletePost, name="deletePost"),
    path('update_post/<str:pk>/', views.updatePost, name="updatePost"),
    path('add_favorite/<uuid:pk>/', views.add_favorite, name='add_favorite'),  # Cambio de int a uuid
    path('remove_favorite/<uuid:pk>/', views.remove_favorite, name='remove_favorite'),  # Cambio de int a uuid
    path('favorites/', views.favorites, name="favorites"),
    path('search/', views.post_search, name='post_search'),
]
