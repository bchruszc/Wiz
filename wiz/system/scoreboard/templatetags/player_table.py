from django.template import Library

register = Library()

def game_table(player):
    
    return '%d' % d.get_team_points(t.id)
    
    return '%d' % d.get_team_points(t.id, race_id)
    
driver_get_team_points = register.simple_tag(driver_get_team_points)