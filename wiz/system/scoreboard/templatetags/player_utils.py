from django.template import Library

register = Library()

def times_ranked(player, rank=0, num_players=0):
    if rank > num_players and num_players != 0: return '-'
    return str(player.times_ranked(rank, num_players))

def high_score(player, num_players=0):
    return str(player.high_score(num_players))

def low_score(player, num_players=0):
    return str(player.low_score(num_players))

register.simple_tag(times_ranked)
register.simple_tag(high_score)
register.simple_tag(low_score)