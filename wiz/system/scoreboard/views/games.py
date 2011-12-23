from django.shortcuts import render_to_response
from django.template.context import RequestContext
from system.scoreboard.models import Game
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import InvalidPage

def game(request, game_id):
    game = get_object_or_404(Game, id=game_id) #@UndefinedVariable
    return render_to_response('scoreboard/game_details.html', RequestContext(request, {
        'menu_group':"games",
        'game':game
    }))
    
def games(request, page=1):
    all_games = Game.objects.order_by('-date') #@UndefinedVariable
    paginator = Paginator(all_games, 5)

    try:
        games = paginator.page(page)
    except (EmptyPage, InvalidPage):
        games = paginator.page(paginator.num_pages)

    return render_to_response('scoreboard/games.html', RequestContext(request, {
        'menu_group':"games",
        'games':games
    }))