from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from system.scoreboard.models import Player
from system.scoreboard.models import PlayedInGame

def players(request, player_id): 
    p = get_object_or_404(Player, id=player_id)
    players = Player.objects.order_by('initials') #@UndefinedVariable
    recent_games = PlayedInGame.objects.filter(player=p).order_by('-game__date')[0:10] #@UndefinedVariable

    return render_to_response('scoreboard/player.html', RequestContext(request, {
           'menu_group':"leaderboard",
           'player':p,
           'players':players,
           'recent_games':recent_games,
           'player_range':range(3,8),
           'rank_range':range(1,8),
        }))