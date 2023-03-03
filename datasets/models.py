from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class SchemaModel(models.Model):
    title = models.CharField(max_length=64)
    separator = models.CharField(max_length=5, null=True)
    quotechar = models.CharField(max_length=5, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    src = models.FileField(upload_to='media/csv/')
    author = models.ForeignKey(to=USER, on_delete=models.CASCADE)

    def __str__(self):
        return f'Title: {self.title}, author: {self.author}'
