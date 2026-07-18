from django.shortcuts import render,redirect
import requests
from .models import Team, Player, Match, Member, PointsTable,Result
from .models import Match
from .forms import PlayerForm
from .models import Announcement, Sponsor , Auction
from .models import Player, Registration
from .forms import RegistrationForm
from django.contrib import messages
from .models import GallerySeason, GalleryImage
from .models import Notice
from .models import Registration, RegistrationSettings


def home(request):
    return render(request, 'index.html')

def members(request):

    all_members = Member.objects.all()

    context = {
        'members': all_members
    }

    return render(request, 'members.html', context)

def gallery(request):

    seasons = GallerySeason.objects.all()

    return render(request, 'gallery.html', {
        'seasons': seasons
    })


def season_gallery(request, season_id):

    season = GallerySeason.objects.get(id=season_id)

    images = GalleryImage.objects.filter(season=season)

    return render(request, 'season_gallery.html', {
        'season': season,
        'images': images
    })
def contact(request):
    return render(request, 'contact.html')


def registration(request):

    settings = RegistrationSettings.objects.first()

    if settings is None:
        settings = RegistrationSettings.objects.create()

    if not settings.registration_open:
        return render(request, "registration_closed.html")

    print("Registration view called")

    if request.method == "POST":
        print("POST request received")

        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            print("Form is valid")

            reg = form.save()

            Player.objects.create(
                name=reg.player_name,
                age=reg.age,
                phone=reg.phone,
                role=reg.role,
                address=reg.address,
                photo=reg.photo,
                payment_screenshot=reg.payment_screenshot,
            )
            data = {
                "name": reg.player_name,
                "phone": reg.phone_number,
                "email": reg.email,
                "address": reg.address,
                "role": reg.role,
                "photo": str(reg.photo.url) if reg.photo else "",
                "aadhar": str(reg.aadhar.url) if reg.aadhar else "",
                "payment": str(reg.payment_screenshot.url) if reg.payment_screenshot else "",
            }

            GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw6uDQiv2bS7VeoU3m7a3bPxg5RrjuhNtHNyU1ErKuMKXV53ei8eVrtiBs4CT5q7o8H/exec"

            requests.post(GOOGLE_SCRIPT_URL, json=data)

            print("Player created successfully")

            messages.success(request, "Registration Successful!")
            return redirect("registration")

        else:
            print("FORM ERRORS:")
            print(form.errors)

    else:
        print("GET request")

        form = RegistrationForm()

    return render(request, "registration.html", {"form": form})


def matches(request):

    matches = Match.objects.all()

    return render(request, 'matches.html', {'matches': matches})
def players(request):
    players = Registration.objects.filter(status="Approved").order_by("player_name")

    return render(
        request,
        "players.html",
        {
            "players": players
        }
    )
def teams(request):

    all_teams = Team.objects.all()

    context = {
        'teams': all_teams
    }

    return render(request, 'teams.html', context)

def points_table(request):

    table = PointsTable.objects.all().order_by('-points')

    return render(request, 'points_table.html', {
        'table': table
    })

def auction(request):

    players = Auction.objects.all()

    context = {
        'players': players
    }

    return render(request, 'auction.html', context)

def results(request):
    results = Result.objects.all()

    return render(request, 'results.html', {
        'results': results
    })

def index(request):

    announcements = Announcement.objects.all()
    sponsors = Sponsor.objects.all()
    
    

    context = {
        'announcements': announcements,
        'sponsors': sponsors,
        
        
    }

    return render(request, 'index.html', context)

def gspl(request):
    return render(request, 'gspl/index.html')

def notice(request):

    notices = Notice.objects.all().order_by('-uploaded_at')

    return render(request, 'notice.html', {'notices': notices})