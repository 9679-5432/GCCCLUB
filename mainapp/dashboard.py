from django.shortcuts import render, get_object_or_404, redirect
from .models import Registration
from django.db.models import Q
from .forms import RegistrationForm
from django.http import HttpResponse
from openpyxl import Workbook

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.units import inch
from django.conf import settings
from datetime import datetime
import os
from .models import RegistrationSettings


def open_registration(request):
    settings = RegistrationSettings.objects.first()

    if settings is None:
        settings = RegistrationSettings.objects.create()

    settings.registration_open = True
    settings.save()

    return redirect("dashboard_home")


def close_registration(request):
    settings = RegistrationSettings.objects.first()

    if settings is None:
        settings = RegistrationSettings.objects.create()

    settings.registration_open = False
    settings.save()

    return redirect("dashboard_home")

# Dashboard Home
# Dashboard Home
def dashboard_home(request):

    total = Registration.objects.count()

    approved = Registration.objects.filter(
        status="Approved"
    ).count()

    pending = Registration.objects.filter(
        status="Pending"
    ).count()

    rejected = Registration.objects.filter(
        status="Rejected"
    ).count()

    recent_registrations = Registration.objects.all().order_by("-id")[:5]

    settings = RegistrationSettings.objects.first()

    if settings is None:
        settings = RegistrationSettings.objects.create()

    return render(
        request,
        "dashboard/dashboard_home.html",
        {
            "total": total,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "recent_registrations": recent_registrations,
            "registration_open": settings.registration_open,
        },
    )


# Registration List
def registration_list(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")

    registrations = Registration.objects.all().order_by("id")

    # Search by player name or phone
    if search:
        registrations = registrations.filter(
            Q(player_name__icontains=search) |
            Q(phone__icontains=search)
        )

    # Filter by status
    if status:
        registrations = registrations.filter(status=status)

    return render(
        request,
        "dashboard/registration_list.html",
        {
            "registrations": registrations,
            "search": search,
            "status": status,
        },
    )


# Registration Details
def registration_detail(request, id):
    player = get_object_or_404(Registration, id=id)

    return render(
        request,
        "dashboard/registration_detail.html",
        {
            "player": player
        }
    )


# Approve Registration
def approve_registration(request, id):
    player = get_object_or_404(Registration, id=id)
    player.status = "Approved"
    player.save()

    return redirect("registration_detail", id=id)


# Reject Registration
def reject_registration(request, id):
    player = get_object_or_404(Registration, id=id)
    player.status = "Rejected"
    player.save()

    return redirect("registration_detail", id=id)


# Players
def players(request):
    search = request.GET.get("search", "")

    players = Registration.objects.filter(status="Approved")

    if search:
        players = players.filter(
            Q(player_name__icontains=search) |
            Q(phone__icontains=search)
        )

    players = players.order_by("id")

    return render(
        request,
        "dashboard/players.html",
        {
            "players": players,
            "search": search,
        }
    )

def edit_player(request, id):
    player = get_object_or_404(Registration, id=id)

    if request.method == "POST":
        form = RegistrationForm(
            request.POST,
            request.FILES,
            instance=player
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard_players")

    else:
        form = RegistrationForm(instance=player)

    return render(
        request,
        "dashboard/edit_player.html",
        {
            "form": form,
            "player": player,
        },
    )

def delete_player(request, id):
    player = get_object_or_404(Registration, id=id)

    if request.method == "POST":
        player.delete()
        return redirect("dashboard_players")

    return render(
        request,
        "dashboard/delete_player.html",
        {
            "player": player
        }
    )

def export_players_excel(request):
    players = Registration.objects.filter(status="Approved").order_by("id")

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Approved Players"

    # Header
    worksheet.append([
        "Sl No",
        "Player Name",
        "Age",
        "Category",
        "Role",
        "Phone",
        "Village"
    ])

    # Data
    for index, player in enumerate(players, start=1):
        worksheet.append([
            index,
            player.player_name,
            player.age,
            player.age_category,
            player.role,
            player.phone,
            player.address,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="GSPL_Approved_Players.xlsx"'
    )

    workbook.save(response)

    return response

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

subtitle_style = styles["Heading2"]
subtitle_style.alignment = TA_CENTER

normal_style = styles["Normal"]
normal_style.alignment = TA_CENTER

def export_players_pdf(request):

    players = Registration.objects.filter(
        status="Approved"
    ).order_by("id")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="GSPL_Approved_Players.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    elements = []

    # ================= Logo =================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "gspl_logo.jpg",
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=80,
            height=80,
        )

        logo.hAlign = "CENTER"

        elements.append(logo)

    elements.append(Spacer(1, 10))

    # ================= Heading =================

    elements.append(
        Paragraph(
            "GHANARAMPUR SUPER PREMIER LEAGUE",
            title_style,
        )
    )

    elements.append(
        Paragraph(
            "GSPL Season 3 - 2026",
            subtitle_style,
        )
    )

    elements.append(
        Paragraph(
            "<b>Approved Players List</b>",
            subtitle_style,
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"Generated On : {datetime.now().strftime('%d %B %Y')}",
            normal_style,
        )
    )

    elements.append(
        Paragraph(
            f"Total Approved Players : {players.count()}",
            normal_style,
        )
    )

    elements.append(Spacer(1, 20))

        # ================= Table =================

    data = []

    data.append([
        "Sl",
        "Photo",
        "Player Name",
        "Age",
        "Role",
        "Category",
        "Phone",
        "Village",
    ])

    for i, player in enumerate(players, start=1):

        photo = ""

        if player.photo:

            photo_path = player.photo.path

            if os.path.exists(photo_path):

                photo = Image(
                    photo_path,
                    width=35,
                    height=35,
                )

        data.append([
            i,
            photo,
            player.player_name,
            player.age,
            player.age_category,
            player.role,
            player.phone,
            player.address,
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),

    ]))

    elements.append(table)

    doc.build(elements)

    return response