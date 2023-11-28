from django.db import models

# Create your models here.
class Postulante(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    resumecv = models.TextField()
    puntuacioncv = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    