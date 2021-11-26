from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materials/', views.material, name='materials'),
    path('purchases/', views.purchase, name='purchases'),
    path('recipes/', views.recipe, name='recipes'),
]
