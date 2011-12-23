from django.contrib import admin
from system.scoreboard.models import Player
from system.scoreboard.models import Game
from system.scoreboard.models import PlayedInGame

#
#  PLAYER
#

#class PlayerAdmin(admin.ModelAdmin):
#    fields = ['first_name', 'last_name', 'initials']
#    list_display = ('first_name', 'initials')
    
admin.site.register(Player)

#
#  GAME
#

#class GameAdmin(admin.ModelAdmin):
#    fields = ['date', 'use_manual_points']
#    list_display = ('date')
    
admin.site.register(Game)
admin.site.register(PlayedInGame)
