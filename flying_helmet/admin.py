from django.contrib import admin
from .models import Review, Recipe, Cuisine, Ingredient, Ingredient_quantities

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Cuisine)
admin.site.register(Review)
admin.site.register(Ingredient_quantities)
