from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class MealTime(models.Model):
    diff_meals = [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snack', 'Snack'), ('dinner', 'Dinner')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type=models.CharField(max_length=20, choices=diff_meals)
    name = models.CharField(max_length=200)
    date=models.DateField(default= timezone.now)
    protein = models.FloatField()
    energy = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    sugar = models.FloatField()
    fiber = models.FloatField()
    calcium= models.FloatField()
    iron = models.FloatField()
    magnesium = models.FloatField()
