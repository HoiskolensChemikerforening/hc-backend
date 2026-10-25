from django.contrib import admin

from .models import CandidatePref, PositionPref, ElectionPref, TicketPref, CandidateRank

admin.site.site_title = "Valg"


@admin.register(ElectionPref)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["date", "is_open"]


@admin.register(CandidatePref)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["user", "get_position", "gender"]

    def get_position(self, obj):
        return obj.candidate_position.first().position_name

#TODO: Legg til alt av stuff models gir. Fix models først.
@admin.register(PositionPref)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_name",
        "spots",
        "total_votes",
        "blank_votes",
        "number_of_prevote_tickets",
        "is_active",
        "is_done",
        "get_candidates_votes",
        "important_gender",
    ]

    def get_candidates_votes(self, obj):
        return "\n".join(
            [
                f"{candidate.user.get_full_name()}: {candidate.get_candidate_votes()},"
                for candidate in obj.candidates.all()
            ]
        )

    def blank_votes(self, obj):
        return str(obj.get_blank_votes())

    def total_votes(self, obj):
        return str(obj.get_total_votes())

@admin.register(TicketPref)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "position", "get_candidates"]

    def get_candidates(self, obj):
        return "\n".join(
            [
                f"{candidate.user.get_full_name()},"
                for candidate in obj.candidates.all()
            ]
        )

@admin.register(CandidateRank)
class CandidateRankAdmin(admin.ModelAdmin):
    list_display = ["rank", "get_candidates"]

    def get_candidates(self, obj):
        return "\n".join(
            [
                f"{candidate.user.get_full_name()},"
                for candidate in obj.candidates.all()
            ]
        )
