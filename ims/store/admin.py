from django.contrib import admin
from .models import Material, Purchase, Recipe, Ingredient


class MaterialAdmin(admin.ModelAdmin):
    pass


class PurchaseAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    pass



admin.site.register(Material, MaterialAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
