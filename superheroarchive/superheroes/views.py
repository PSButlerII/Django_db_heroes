from django.shortcuts import render
from .models import SuperHero


# Create your views here.

def index(request):
    all_superheroes = SuperHero.objects.all()
    context = {
        'all_superheroes': all_superheroes
    }
    return render(request, 'superheroes/index.html', context)


def detail(request, superhero_id):
    singular_superhero = SuperHero.objects.filter(pk=superhero_id).get()
    context = {
        'singular_superhero': singular_superhero
    }
    return render(request, 'superheroes/detail.html', context)
