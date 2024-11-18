from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'favorites']  # Excluimos 'author' del formulario, no se mostrará

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extraemos 'user' de kwargs
        super(PostForm, self).__init__(*args, **kwargs)

        # Si el usuario está disponible, asignamos el autor automáticamente
        if user:
            self.instance.author = user

        # Agregamos la clase 'form-control' a los campos de texto
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['subtitle'].widget.attrs.update({'class': 'form-control'})
        self.fields['image_portada'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget = CKEditorUploadingWidget(attrs={'class': 'form-control'})

