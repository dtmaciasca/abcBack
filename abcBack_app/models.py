from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + ' ' + str(self.id)

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categoria')
    lugar = models.CharField(null=False, max_length=500)
    direccion = models.CharField(null=False, max_length=500)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    es_presencial = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)




