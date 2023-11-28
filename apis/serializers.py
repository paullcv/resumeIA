from rest_framework import serializers
from .models import Postulante

class PostulanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulante
        fields = ('id', 'nombre', 'email','resumecv','puntuacioncv', 'created_at')
        read_only_fields = ('created_at',)