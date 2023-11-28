from django.urls import path
from .views import Test
from .viewstwo import Match

urlpatterns=[
    path('api/postulanteIA/', Test.as_view(), name='resume'),  # Añade una barra al final
    path('api/postulanteIA/<int:pk>/', Test.as_view(), name='get_postulante'),  
    #path('api/matchIA/', Match.as_view(), name='match'),
    path('api/postulanteIA/<int:pk>/delete/', Test.as_view(), name='delete_postulante'),
]