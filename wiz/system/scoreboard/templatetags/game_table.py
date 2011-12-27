from django.template import Library
from system.scoreboard.models import PlayedInGame

register = Library()

def game_table(game):
    players = game.players.all()
    player_rows = []
    rating_changes = game.get_rating_changes()
    for player in players:
        row = {}
        pig = PlayedInGame.objects.get(player=player, game=game) #@UndefinedVariable
        row['rank'] = pig.rank
        row['player'] = player
        row['points'] = pig.total_points_manual
        rat_delta = rating_changes[pig.player]
        #row['expected'] = rating_changes[pig.player][1]
        #row['actual'] = rating_changes[pig.player][2]
        rat_text = str(round(rat_delta, 1))
        if rat_delta > 0:
            rat_text = "+" + rat_text
        row['rating_change'] = rat_text
        # Not relevant without a star
        #if pig.called_and_won:
        #    row['star'] = '*'
        #else:
        #    row['star'] = ''
            
        player_rows.append(row)
    
    player_rows.sort(rank_sorter)
    
    return {'players':player_rows}

def rank_sorter(x,y):
    return x['rank'] - y['rank']

register.inclusion_tag('scoreboard/game.html')(game_table)
