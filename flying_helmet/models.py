from django.db import models

# Create your models here.

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
   
    def __str__(self):
        return f'{self.name} {self.id}' 
        

class Recipe(models.Model):
    name = models.CharField(max_length=300)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, default='')
    poster_username = models.CharField(max_length=150)
   # dietery_restriction = models.CharField(max_length=)
    portions = models.IntegerField(default=1)
    method = models.CharField(max_length=1000)
    prep_time = models.IntegerField(default=10)
    image = models.ImageField(null=True, blank=True, upload_to='recipe_images/')
    
    def __str__(self):
        return f'{self.name} {self.id}' 
        
    

class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    recipes = models.ManyToManyField(Recipe, through='Ingredient_quantities')

    def __str__(self):
        return f'{self.name} {self.id}' 


class Review(models.Model):
    review_text = models.CharField(max_length=600)
    reviewer = models.CharField(max_length=150)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

class Ingredient_quantities(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.recipe.name} {self.ingredient.name} {self.quantity}'