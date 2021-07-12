from django.shortcuts import render

from .models import SuperHero
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        alter_ego = request.POST.get('alter ego')
        primary_ability = request.POST.get('primary ability')
        secondary_ability = request.POST.get('secondary ability')
        catch_phrase = request.POST.get('catch phrase')
        new_superhero = SuperHero(name=name, alter_ego=alter_ego, primary_ability=primary_ability,
                                  secondary_ability=secondary_ability, catch_phrase=catch_phrase
                                  )
        new_superhero.save()
        return HttpResponseRedirect(reverse('superheroes:index', ))
    else:
        return render(request, 'superheroes/create.html')


def index(request):
    all_superheroes = SuperHero.objects.all()
    context = {
        'all_superheroes': all_superheroes
    }
    return render(request, 'superheroes/index.html', context)


def superhero_detail(request, superhero_id):
    singular_superhero = SuperHero.objects.get(pk=superhero_id)
    context = {
        'singular_superhero': singular_superhero
    }
    return render(request, "superheroes/detail.html", context, )


def delete_hero(request, superhero_id):
    singular_superhero = SuperHero.objects.get(pk=superhero_id)
    if request.method == 'POST':
        singular_superhero.delete()
    context = {
        'singular_superhero': singular_superhero
    }
    return render(request, "superheroes/deleteview.html", context)
