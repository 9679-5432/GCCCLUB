from django.shortcuts import render
from mainapp.models import Team, Match

def gspl_home(request):
    teams = Team.objects.all()
    return render(request, 'gspl/index.html', {'teams': teams})

def teams(request):
    teams = Team.objects.all()
    return render(request, 'gspl/teams.html', {'teams': teams})

def matches(request):
    matches = Match.objects.all()
    return render(request, 'gspl/matches.html', {'matches': matches})