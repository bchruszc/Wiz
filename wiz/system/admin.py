from django.contrib import admin
from system.scoreboard.models import Player

class PlayerAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question']

admin.site.register(Player, PlayerAdmin)
