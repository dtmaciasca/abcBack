from .models import Evento, Categoria
from rest_framework import serializers

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categoria
        fields=('id','nombre')

class EventoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    class Meta:
        model = Evento
        fields = ('id','nombre', 'categoria', 'lugar', 'direccion', 'fecha_inicio',
                  'fecha_fin', 'es_presencial')