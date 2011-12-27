from django.shortcuts import render_to_response
from django.template import RequestContext
from system.scoreboard.models import AwardFactory

def awards(request):
    award_list = []
    af = AwardFactory()
    
    award_list.append(af.get_highest_point_award())
    award_list.append(af.get_highest_rating_award())

    award_list.append(af.get_highest_average_award())
    award_list.append(af.get_lowest_win_award())
    #award_list.append(af.get_points_ahead_of_winner())  - Not relevant without a star

#    award_list.append(af.get_longest_winning_streak_award())
#    award_list.append(af.get_longest_winless_streak_award())
#    award_list.append(af.get_longest_winless_streak_current_award())
    award_list.append(af.get_win_streak())
    award_list.append(af.get_loser_streak())
   # award_list.append(af.get_star_streak())  - Not relevant without a star

#    sa = af.get_win_streak()
#    for award in sa.get_sub_awards():
#        award_list.append(award)

    return render_to_response('scoreboard/awards.html', RequestContext(request, {
       'menu_group':"awards",
       'awards':award_list,
    }))
