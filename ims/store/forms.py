from django.forms import ModelForm
from .models import Material, Purchase, Recipe

class add_material_form(ModelForm):
    class Meta:
        model = Material
        fields = ['name']

class add_purchase_form(ModelForm):
    class Meta:
        model = Purchase
        fields = ['type', 'price', 'measure', 'notes', 'date_of_purchase']

class recipe_form(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']