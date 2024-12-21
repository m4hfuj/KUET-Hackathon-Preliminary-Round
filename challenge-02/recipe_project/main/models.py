from django.db import models

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('pieces', 'Pieces'),
        ('grams', 'Grams'),
        ('kilograms', 'Kilograms'),
        ('liters', 'Liters'),
        ('cups', 'Cups'),
        ('tablespoons', 'Tablespoons'),
        ('teaspoons', 'Teaspoons'),
    ]

    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES,blank= True, null =True)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=2000, blank= True, null = True)
    

    def __str__(self):
        return self.name
