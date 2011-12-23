from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from system.scoreboard.models import Chart
from django.http import HttpResponse
from datetime import datetime
from datetime import date
from datetime import timedelta
from system.scoreboard.models import Player
from system.scoreboard.models import RatingManager

def graph(request, data_type="rating", start_date=(datetime.now() - timedelta(days=28)).strftime("%Y%m%d"), 
end_date=(datetime.now() + timedelta(days=4)).strftime("%Y%m%d")):
    return render_to_response('scoreboard/graph.html', RequestContext(request, {
        'menu_group':"graph",
        'graph_type':data_type,
        'start_date':start_date,
        'end_date':end_date,
    }))
    
def graph_data(request, data_type, start_date, end_date):
    s_date = date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
    e_date = date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))
    
    if data_type == "rating":
        return graph_rating(request, s_date, e_date)

#    return render_to_response('scoreboard/graph.html', RequestContext(request, {
#        'menu_group':"graph",
#        'graph_type':graph_type,
#        'player_id':player_id,
#        'players':Player.objects.all(), #@UndefinedVariable
#    }))

def graph_rating(request, start_date, end_date):
    gd = Chart("line_dot", "Ratings")
    
    # Meridith hack in get_dail_ratings
    values, labels, normal_values = RatingManager().get_daily_ratings(start_date, end_date)

    gd.set_x_axis_labels(labels)
    
    for p in Player.objects.all(): #@UndefinedVariable
        gd.add_values(values[p], str(p), "#" + p.graph_colour)
    
    gd.add_values_background(normal_values, "Average")
#    gd.set_y_range(1120, 1310)
    gd_serialized = simplejson.dumps(gd.get_js())
    
    return HttpResponse(gd_serialized, "text/plain")

#def graph_points(request, player_id):
#    gd = Chart("bar", "Points")
#    
#    player = Player.objects.get(id=player_id) #@UndefinedVariable
#    pigs = PlayedInGame.objects.filter(player=player) #@UndefinedVariable
#    value_dict = {}
#    for p in pigs:
#        value_dict[p.game.date.strftime("%d%m%Y")] = p.total_points_manual
#
#    values, labels = RatingManager().get_daily_ratings()
#    min = min - 10
#    max = max + 10
#
#    normal_values = []
#
#    for v in values:
#        normal_values.append(None)
#    normal_values[0] = 0
#    normal_values[-1] = 0
#    
#    gd.set_x_axis_labels(labels)
#    gd.add_values(values, str(player))
#    gd.add_values_background(normal_values, "Zero")
#
#    gd.set_y_range(min, max)
#    gd_serialized = simplejson.dumps(gd.get_js())
#    
#    return HttpResponse(gd_serialized, "text/plain")

    
