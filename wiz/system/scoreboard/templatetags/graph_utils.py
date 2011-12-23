from django.template import Library
from datetime import date
from datetime import timedelta
from system.scoreboard.models import Game

register = Library()

def start_dates():
    dates = []
    all_games = Game.objects.order_by("date") #@UndefinedVariable
    first_date = all_games[0].date
    last_date = all_games[len(all_games) - 1].date
    week_delta = timedelta(weeks=1)
    cur_date = first_date - timedelta(days=(1 - first_date.weekday()))
    
    while cur_date < last_date:
        dates.append(wrap_date_with_option_text(cur_date))
        cur_date = cur_date + week_delta
    return dates

def end_dates():
    return start_dates()

def wrap_date_with_option_text(date):
    return '<option value="' + date.isoformat() + '">' + date.isoformat() + '</option>'

register.simple_tag(start_dates)
register.simple_tag(end_dates)