from django.shortcuts import render
from .models import SuperHero
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.


def index(request):
    all_superheroes = SuperHero.objects.all()
    context = {
        'all_superheroes': all_superheroes
    }
    return render(request, 'superheroes/index.html', context)


def superhero_detail(request, superhero_id):
    singular_superhero = SuperHero(pk=superhero_id)
    context = {
        'singular_superhero': singular_superhero
    }
    return render(request, "superheroes/detail.html", context)


def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        alter_ego = request.POST.get('primary ability')
        primary_power = request.POST.get('secondary ability')
        secondary_power = request.POST.get('catch_phrase')
        catch_phrase = request.POST.get('catch phrase')
        new_superhero = SuperHero(name=name, alter_ego=alter_ego, primary_power=primary_power,
                                  secondary_power=secondary_power, catch_phrase=catch_phrase
                                  )
        new_superhero.save()
        return HttpResponseRedirect(reverse('superheroes:index'))
    else:
        return render(request, 'superheroes/create.html')
