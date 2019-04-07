from django.contrib import admin

from .models import Candidate, Position, Election, Ticket

admin.site.site_header = "Valg"
admin.site.site_title = "Valg"


admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(Election)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["get_candidates", "is_blank", "position"]

    def get_candidates(self, obj):
        return "\n".join(
            [
                candidate.user.get_full_name() + ","
                for candidate in obj.candidates.all()
            ]
        )
