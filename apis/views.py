from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Postulante
from .serializers import PostulanteSerializer
from .ia import *

@method_decorator(csrf_exempt, name='dispatch')
class Test(View):
    
    def get(self, request, pk=None):  # Hacer 'pk' opcional
        if pk is not None:
            # Se proporcionó 'pk', obtener un registro específico
            try:
                postulante = Postulante.objects.get(pk=pk)
                serializer = PostulanteSerializer(postulante)
                return JsonResponse(serializer.data)
            except Postulante.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            # No se proporcionó 'pk', obtener todos los registros
            postulantes = Postulante.objects.all()
            serializer = PostulanteSerializer(postulantes, many=True)
            return JsonResponse(serializer.data, safe=False)
    

    def post(self, request):
        data = JSONParser().parse(request)
        resumen = str(process_resume(data.get('resumecv')))
        #print(resumen)
        job = str((data.get('job')))
        match = calculate_similarity(data.get('resumecv'),data.get('job'))
        print(match)
        
        # Modificar el valor de 'resumecv' en el diccionario 'data'
        data['resumecv'] = resumen
        data['puntuacioncv'] = match

        serializer = PostulanteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            postulante = Postulante.objects.get(pk=pk)
        except Postulante.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        data = JSONParser().parse(request)
        serializer = PostulanteSerializer(postulante, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            postulante = Postulante.objects.get(pk=pk)
        except Postulante.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        postulante.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
