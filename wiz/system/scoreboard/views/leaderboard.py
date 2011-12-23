from django.shortcuts import render_to_response
from django.template import RequestContext
from system.scoreboard.models import PlayedInGame
from system.scoreboard.models import Player
from system.scoreboard.models import Game

def leaderboard(request): 
    player_infos = []
    player_infos.append(['All Players', 'All', get_leaders()])
    player_infos.append(['3 Players', '3', get_leaders(3)])
    player_infos.append(['4 Players', '4', get_leaders(4)])
    player_infos.append(['5 Players', '5', get_leaders(5)])
    player_infos.append(['6 Players', '6', get_leaders(6)])
    #player_infos.append(['7 Players', '7', get_leaders(7)])
    
    recent_winners = []
    for game in Game.objects.order_by('-date')[:10]: #@UndefinedVariable
        recent_winner={}
        recent_winner['game'] = game
        winner = PlayedInGame.objects.filter(game=game,rank=1)[0] #@UndefinedVariable
        recent_winner['winner'] = winner.player
        recent_winner['points'] = winner.total_points_manual
        recent_winners.append(recent_winner)

    return render_to_response('scoreboard/leaderboard.html', RequestContext(request, {
           'menu_group':"leaderboard",
           'player_infos':player_infos,
           'recent_winners':recent_winners,
        }))

def get_leaders(num_players=0):
    players = Player.objects.all() #@UndefinedVariable
    player_info = []
    
    for p in players:
        wins = p.wins(num_players)
        games = p.games_played(num_players)
        if games == 0:
            continue
        rating = p.get_rating(num_players)
        win_per = 0.0
        if games > 0:
            win_per = (100.0 * wins) / games
        
        info = {}
        info['games'] = games
        info['player'] = p
        info['wins'] = wins
        info['rating'] = rating
        info['win_percentage'] = win_per
        player_info.append(info)
#    info - 7 == 5
    
    player_info.sort(leader_sort)
    return player_info

def leader_sort(x, y):
    if x['rating'] != y['rating']:
        return int(y['rating']) - int(x['rating'])
    if x['win_percentage'] != y['win_percentage']:
        return int(y['win_percentage'] - x['win_percentage'])
    if x['wins'] != y['wins']:
        return int(y['wins'] - x['wins'])
    return x['player'].initials > y['player'].initials
