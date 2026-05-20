from django.contrib import admin
from .models import Team, Player, Match, Member, PointsTable,Result,Announcement
from .models import Sponsor
from .models import Auction
from django.http import HttpResponse
import csv
from .models import Registration
from .models import GallerySeason, GalleryImage
from .models import Notice


admin.site.register(GallerySeason)
admin.site.register(GalleryImage)
admin.site.register(Sponsor)
admin.site.register(Auction)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Member)
admin.site.register(PointsTable)
admin.site.register(Result)
admin.site.register(Announcement)
admin.site.register(Notice)




@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'player_name',
        'age',
        'phone',
        'role'
    )

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=registrations.csv'

        writer = csv.writer(response)

        writer.writerow([
            'Player Name',
            'Age',
            'Phone',
            'Role',
            'Address',
            'Player Photo',
            'Aadhar Card',
            'Payment Screenshot'
        ])

        for player in queryset:

            writer.writerow([
                player.player_name,
                player.age,
                player.phone,
                player.role,
                player.address,
                player.photo.url if player.photo else '',
                player.aadhar_card.url if player.aadhar_card else '',
                player.payment_screenshot.url if player.payment_screenshot else '',
            ])

        return response

    export_as_csv.short_description = "Download Selected Registrations as CSV"