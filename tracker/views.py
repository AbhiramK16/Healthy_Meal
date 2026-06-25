from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from .models import MealTime
from django.utils import timezone
import os

def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('searching')
    value = int(request.GET.get('portion') or 100)
    request.session['last_query'] = query

    findings = []
    nutrient_values = {}
    if query:
        food = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', 
                            params = {
                                'query' : query,
                                'api_key' : os.getenv('USDA_API_KEY')
                            })
        
        findings = food.json().get('foods', [])
        check = query.lower().strip()
        for finding in findings:
            if check == finding['description'].lower().strip(): 
                break
            else:
                message = "Please type a valid food"
                return render(request, 'search.html', {'message': message})
        new_nutrient_names = {'Protein' : 'Protein', "Energy" : "Energy", "Total lipid (fat)" : "Fat", "Carbohydrate, by difference" : "Carbs", "Total Sugars" : "Sugars", "Fiber, total dietary": "Fibers", "Calcium, Ca" : "Calcium",  "Magnesium, Mg" : "Magnesium", "Iron, Fe" : "Iron"}
        nutrient_values = {"Protein": [], "Energy": [], "Fat" : [], "Carbs" : [], "Sugars" : [], "Fibers" : [], "Calcium" : [], "Iron" : [], "Magnesium" : []}
        for nutrient in findings[0]['foodNutrients']:
            if nutrient['nutrientName'] in new_nutrient_names:
                nutrient_values[new_nutrient_names[nutrient['nutrientName']]].append(round((value/100) * int(nutrient['value']), ndigits=3))
                nutrient_values[new_nutrient_names[nutrient['nutrientName']]].append(nutrient['unitName'].lower())
  

    return render(request, 'search.html', {'nutrients' : nutrient_values, 'query' : query})

@login_required(login_url='login')
def addFood(request):
    if request.method == "POST":
        
        today = timezone.now().date()
        MealTime.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            date=today,
            meal_type=request.POST.get('meal_type'),
            protein=request.POST.get('protein') or 0,
            energy=request.POST.get('energy') or 0,
            calcium=request.POST.get('calcium') or 0,
            iron=request.POST.get('iron') or 0,
            carbs=request.POST.get('carbs') or 0,
            magnesium=request.POST.get('magnesium') or 0,
            fat=request.POST.get('fat') or 0,
            sugar=request.POST.get('sugar') or 0,
            fiber=request.POST.get('fiber') or 0
        )
    return render(request, 'myplan.html')

@login_required(login_url='login')
def myplan(request):    
    today = timezone.now().date()
    meal_choice = request.GET.get('mealtime')

    if meal_choice != 'all' and meal_choice != None:
        meals = MealTime.objects.filter(user=request.user, meal_type=meal_choice, date=today)
    else:
        meals = MealTime.objects.filter(user=request.user, date=today)
    times = ['breakfast', 'lunch', 'snack', 'dinner']
    return render(request, 'myplan.html', {'meal_choice' : meal_choice, 'meals' : meals, 'times' : times})

