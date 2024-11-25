# models.py

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import uuid

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = RichTextUploadingField(null=True, blank=True, default="")
    image_portada = models.ImageField(null=True, blank=True, default="image_default.jpg")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Añadir el campo de fecha de creación
    favorites = models.ManyToManyField(User, related_name='favorite_posts', blank=True)  # Campo para los favoritos

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
