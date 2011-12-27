from datetime import datetime
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from system.scoreboard.models import Game, GameForm, PlayedInGame, \
    PlayedInGameForm

def entry(request):
    PIG_formset = formset_factory(PlayedInGameForm, extra=8, max_num=8)

    if request.method == 'POST':
        pig_fs = PIG_formset(request.POST, request.FILES)
        game_form = GameForm(request.POST)
        if pig_fs.is_valid() and game_form.is_valid():
            # We have a valid submission.
            if not 'date' in game_form.cleaned_data:
                return entry_failure(pig_fs, game_form, request, ['You must enter a game date'])
            
            game = Game(date=game_form.cleaned_data['date'], use_manual_points=True)

            pigs = []
            pig_points = []
            position=0
            for form in pig_fs.forms:
                position = position + 1
                if not 'player' in form.cleaned_data:
                    continue
                player = form.cleaned_data['player']
                pts = form.cleaned_data['total_points_manual']
                star = form.cleaned_data['called_and_won']
                pig_points.append(pts)
                pigs.append(PlayedInGame(player=player, 
                                         table_position=position, 
                                         total_points_manual=pts, 
                                         called_and_won=star,
                                         rating=0,
                                         rating_change=0
                                         ))
            
            if(len(pigs) < 3):
                return entry_failure(pig_fs, game_form, request, ['At least three players are required in a game'])

            
            ranks = {} # Map pts -> rank
            last_pts = 99999
            rank = 1
            pig_points.sort(reverse=True)

            for pts in pig_points:
                if pts != last_pts:
                    ranks[pts] = rank
                last_pts = pts
                rank = rank + 1
            
            game.num_players = len(pigs)
            game.save()
            
            pigs.sort(pig_sorter)
            
            rank = 1
            last_rank = 0
            last_points = 99999
            for pig in pigs:
                if pig.total_points_manual != last_points:
                    last_rank = rank
                    last_points = pig.total_points_manual
                pig.game = game
                pig.rank = last_rank
                pig.save()
                rank = rank + 1
                
            # Success!
            return HttpResponseRedirect('/game/' + str(game.id) + '/')
        else:
            return entry_failure(pig_fs, game_form, request, ['Please correct the invalid fields below'])

    else:
        pig_fs = PIG_formset(initial=None)
        game_form = GameForm({'date':datetime.now().strftime("%Y-%m-%d")})
        return render_to_response('scoreboard/entry.html', RequestContext(request, {
                'menu_group':"entry",
                'pig_formset':pig_fs,
                'game_form':game_form,
                'csrf_token':csrf(request),
            }))

def pig_sorter(x, y):
    if x.called_and_won != y.called_and_won:
        if x.called_and_won: return -1
        else: return 1
    return y.total_points_manual - x.total_points_manual

def entry_failure(pig_fs, game_form, request, errors=[]):
    return render_to_response('scoreboard/entry.html', RequestContext(request, {
        'menu_group':"entry",
        'errors':errors,
        'pig_formset':pig_fs,
        'game_form':game_form,
        'csrf_token':csrf(request),
    }))
    
