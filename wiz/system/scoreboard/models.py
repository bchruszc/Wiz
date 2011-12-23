from django.db import models
from django.forms.models import ModelForm
from datetime import timedelta
import random

class RatingManager:
    def get_daily_ratings(self, s_date, e_date):
        graphs  = {}
        
        end_date = e_date + timedelta(days=7-e_date.weekday())
        start_date = s_date + timedelta(days=0-s_date.weekday())
        date = start_date
        players = Player.objects.all()

        add_date = 0
        labels = []
        normal_values = []
        mer_rating = 1200
        mer = Player.objects.get(id=12)
        for p in players:
            graphs[p] = [] 
        while date <= end_date:
            if date.weekday() >= 5:  # Skip weekends
                date = date + timedelta(days=2)
                continue

            # Default is "None" for this date
            ratings_this_date = {}
            for p in players:
                ratings_this_date[p] = None
            
            # If there are pigs for this date, get the rating
            pigs = PlayedInGame.objects.filter(game__date=date)
            for pig in pigs:
                ratings_this_date[pig.player] = pig.rating
            
            if pigs.count() > 0:
                randint = random.randint(1, 7)
                if randint == 1:
                    ratings_this_date[mer] = mer_rating + random.randint(16, 22)
                elif randint == 2:
                    ratings_this_date[mer] = None
                else:
                    ratings_this_date[mer] = mer_rating - random.randint(-1, 8)
                
                if ratings_this_date[mer]:
                    mer_rating = ratings_this_date[mer]
            
            # Append to the graphs
            for p in players:
                graphs[p].append(ratings_this_date[p])     

            # Label the Mondays
            if add_date % 5 == 0:
            #if date.weekday() == 1:
                labels.append(date.strftime("%d/%m"))
            else:
                labels.append(None)
    
            add_date = add_date + 1
            date = date + timedelta(days=1)
            normal_values.append(None)
        
        normal_values[0] = 1200.0
        normal_values[-1] = 1200.0
        return graphs, labels, normal_values
    
    def win_func(self, value):
        # Currently inverse log
        return 10.0 ** (value / 600.0)
    
    def calculate_ratings(self):
#        if players > 0:
#            games = Game.objects.order_by('date').filter(num_players=players)
#        else:
#            games = Game.objects.order_by('date')
#        if date_end:
#            games = games.filter(date__lte=date_end)
        
        games = Game.objects.order_by('date')
        
        rat = {}
        exp = {}
        exp[3] = [0.79, 0.21, 0.0]
        exp[4] = [0.68, 0.24, 0.08, 0.0]
        exp[5] = [0.6, 0.25, 0.11, 0.04, 0.0]
        exp[6] = [0.55, 0.24, 0.12, 0.06, 0.03, 0.0]
        exp[7] = [0.51, 0.23, 0.13, 0.07, 0.04, 0.02, 0.0]
        
        for p in Player.objects.all():
            rat[p] = 1200.0
            
        for g in games:
            bot = 0
            pigs = g.get_records() # pigs
            
            default_weights = {}
            rank_weights = {}

            for r in range(0, g.num_players):
                default_weights[r+1] = exp[g.num_players][r]
            
            min = 999.9
            tot = 0.0
  
            for r in range(1, 9):
                pigs_at_rank = []
                for pig in pigs:
                    if pig.rank == r:
                        pigs_at_rank.append(pig)
                count = len(pigs_at_rank)
                if count == 0:
                    continue
                
                tot_weight = 0.0
                
                for r2 in range(r, r+count):
                    tot_weight = tot_weight + default_weights[r2]
                    
                avg_weight = tot_weight / (count * 1.0)
                rank_weights[r] = avg_weight
                if avg_weight < min:
                    min = avg_weight
                tot = tot + (avg_weight * count)
                
            tot = tot - (min * pigs.count())
                
            for pig in pigs:
                bot = bot + RatingManager.win_func(self, rat[pig.player])
            
            K = pigs.count() * 10
                            
            for pig in pigs:
                top = RatingManager.win_func(self, rat[pig.player])
                expected = top / bot
                actual = (rank_weights[pig.rank] - min)/tot
                #actual = 0.0
                #if pig.rank == 1:
                #    actual = 1.0

                new_rating = rat[pig.player] + (K * (actual - expected))

                pig.rating_change = new_rating - rat[pig.player]
                pig.rating = new_rating
                pig.save()
                
                rat[pig.player] = new_rating

                #rat[pig.player] = get_rating    return rat
            

###############################################################################
#
#  PLAYER
#
###############################################################################

class Player(models.Model):
    first_name = models.CharField("First Name", max_length=50)
    last_name =  models.CharField("Last Name", max_length=50, blank=True)
    initials =   models.CharField("Initials", max_length=5)
    graph_colour = models.CharField("Graph Colour", max_length=6)
    
    def pigs(self):
        return PlayedInGame.objects.filter(player=self)
    
    def __str__(self):
        return self.first_name
    
    def games_played(self, num_players=0):
        if num_players == 0:
            return self.pigs().count()
        return self.pigs().filter(game__num_players=num_players).count()
    
    # Fi most recent PlayedInGame, and get the rating.
    def get_rating(self, players=0, date_end=None):
        pigs = PlayedInGame.objects.filter(player=self).order_by('-game__date')
        if date_end:
            pigs.filter(date__lte=date_end)
        
        if pigs.count() == 0:
            return 1200
        return pigs[0].get_rating()
#        if self.rating == 0:
#            RatingManager().calculate_ratings(date_end=date_end)
#        
#        return self.rating

    
    def wins(self, num_players):
        return long(self.times_ranked(1, num_players))
    
    # Get the number of times that this player has finished in the given rank
    def times_ranked(self, rank, num_players=0):
        if rank == 0:
            # Treat this as 'all ranks', or games played
            return self.games_played(num_players)
       
        if num_players == 0:  # All number of players
            return self.pigs().filter(rank=rank).count()
        
        return self.pigs().filter(rank=rank, game__num_players=num_players).count()
    
    def high_score(self, num_players=0):
        if num_players == 0:
            if self.pigs().count() == 0:
                return '-'
            return self.pigs().order_by('-total_points_manual')[0].total_points_manual
        if self.pigs().filter(game__num_players=num_players).count() == 0:
            return '-'
        return self.pigs().filter(game__num_players=num_players).order_by('-total_points_manual')[0].total_points_manual
    
    def low_score(self, num_players=0):
        if num_players == 0:
            if self.pigs().filter(game__num_players=num_players).count() == 0:
                return '-'
            return self.pigs().order_by('total_points_manual')[0].total_points_manual
        if self.pigs().filter(game__num_players=num_players).count() == 0:
                return '-'
        return self.pigs().filter(game__num_players=num_players).order_by('total_points_manual')[0].total_points_manual
    
class Game(models.Model):
    date =    models.DateField("Game Date")
    players = models.ManyToManyField(Player, through='PlayedInGame')
    num_players = models.SmallIntegerField("Number of Players")

    #player_records = models.ManyToManyField(PlayedInGame, related_name='played In Game')
    use_manual_points = models.BooleanField("Use Manual Point Total", default=True)

    #driver_gained = models.ForeignKey(Player, related_name='gained_in_trade', verbose_name="Driver_Gained")
    def get_records(self):
        return PlayedInGame.objects.filter(game=self.id).order_by('rank')
    
    def players_with_total_points(self):
        players_and_points = []
        
        # If it's manually entered, use that.
        if self.use_manual_points == True:
            for record in self.get_records():
                players_and_points[record.player] = record.total_points_manual
        else:
            for record in self.player_records:
                # No manual entry...  calculate
                # This doesn't work yet.  In the future!
                players_and_points[record.player] = 0
    
    # Get the ratings/changes of all of the players in this game, after this game
    def get_ratings(self):
        ratings = {}
        pigs = self.get_records()
        # Check if the ratings are saved.  If so, we don't need to calculate
        for pig in pigs:
            if pig.rating == 0:
                RatingManager().calculate_ratings()
                break
            
        for pig in pigs:
            ratings[pig.player] = pig.rating
            
        return ratings

    def get_rating_changes(self):
        deltas = {}
        for pig in self.get_records():
            deltas[pig.player] = pig.rating_change
        return deltas
    
#        rat1 = Playerget_ratingings(None, date_end=self.date - datetime.timedelta(days=1))
#        rat2 = Player().ratings(None, date_end=self.date)
#        deltas = {}
#        for pig in self.get_records():
#            p = pig.player
#            deltas[p] = [0,0,0] 
#            deltas[p][0] = rat2[p][0] - rat1[p][0]
#            deltas[p][1] = rat2[p][1]
#            deltas[p][2] = rat2[p][2]
#        return deltas
        
        
    def __str__(self):
        return str(self.date)

class PlayedInGame(models.Model):
    player = models.ForeignKey(Player, verbose_name="Player") # related_name='played_in_games', 
    game =   models.ForeignKey(Game, verbose_name="Game") # related_name='played_in_games', 
    table_position = models.SmallIntegerField("Position")
    total_points_manual = models.IntegerField("Total Points")
    rank = models.SmallIntegerField("Rank")
    called_and_won = models.BooleanField("Called and Won")
    rating = models.FloatField("Final Rating")
    rating_change = models.FloatField("Rating Change")

    def get_rating(self):
        if self.rating == 0:
            RatingManager().calculate_ratings()
        return self.rating
    
    def __str__(self):
        return str(self.player) + ' played in ' + str(self.game)
    
class PlayedInGameForm(ModelForm):
    #game_date=forms.DateField()
    class Meta:
        model = PlayedInGame
        exclude=('game','table_position','rank','rating', 'rating_change')
        
class GameForm(ModelForm):
    #game_date=forms.DateField()
    class Meta:
        model = Game
        fields=('date',)

class Award:
    def __init__(self, name, decimals=0):
        self.name = name
        self.values = []
        self.decimals = decimals
        self.evaluator = None
    
    def sort(self, custom_sort=None):
        if custom_sort:
            self.values.sort(custom_sort)
        else:
            self.values.sort()
    
    def add_player(self, player, value, game=None):
        self.values.append([player, value, game])
        
    def is_streak(self):
        return isinstance(self, StreakAward)

class StreakAward(Award):
    def __init__(self, name, evaluator, good_name, bad_name, decimals=0):
        self.name = name
        self.values = []
        self.decimals = decimals
        self.evaluator = evaluator
        self.good_name = good_name
        self.bad_name = bad_name
        
    def get_sub_awards(self):
        subs = []
        subs.append(self.get_streak_award(self.good_name + " Streak", False, False))
        subs.append(self.get_streak_award("Current " + self.good_name + " Streak", True, False))
        subs.append(self.get_streak_award(self.bad_name + " Streak", False, True))
        subs.append(self.get_streak_award("Current " + self.bad_name + " Streak", True, True))
        return subs
    
    def get_streak_award(self, award_name, current, opposite):
        a = Award(award_name,)

        for p in Player.objects.all():
            streak = 0
            max_streak = 0
            pigs = PlayedInGame.objects.filter(player=p).order_by('-game__date')
            for pig in pigs:
                match = self.evaluator(pig)
                if match != opposite:
                    streak = streak + 1
                    if streak > max_streak:
                        max_streak = streak
                elif current:  # Not what we're looking for, since it's "current", we're done
                    break
                else:
                    streak = 0
            if current:
                a.add_player(p, streak)
            else:
                a.add_player(p, max_streak)
        a.sort(award_sort_descending)
        return a

class AwardFactory:
    def get_highest_point_award(self):
        from django.db import connection
        a = Award("Most Points in a Single Game")
    
        # First query ends up giving us the sort
        cursor = connection.cursor() #@UndefinedVariable
        cursor.execute("""
            SELECT player_id, MAX(total_points_manual)
            FROM scoreboard_playedingame
            GROUP BY player_id
            ORDER BY 2 DESC
            """)
        for row in cursor.fetchall():
            pig = PlayedInGame.objects.get(player=row[0], total_points_manual=row[1])
            a.add_player(pig.player, pig.total_points_manual, pig.game)
        return a

    def get_highest_rating_award(self):
        from django.db import connection
        a = Award("Peak Rating")

        # First query ends up giving us the sort
        cursor = connection.cursor() #@UndefinedVariable
        cursor.execute("""
            SELECT player_id, MAX(rating)
            FROM scoreboard_playedingame
            GROUP BY player_id
            ORDER BY 2 DESC
            """)
        for row in cursor.fetchall():
            pig = PlayedInGame.objects.get(player=row[0], rating=row[1])
            a.add_player(pig.player, pig.rating, pig.game)
        return a
    
    def get_points_ahead_of_winner(self):
        a = Award("Points Ahead of the Winner")
    
        record_pigs = {} # 0 = pts, 1 = pig

        for g in Game.objects.all():
            pigs = g.get_records()
            high_score = -9999
            for pig in pigs:
                if pig.total_points_manual > high_score and pig.called_and_won:
                    high_score = pig.total_points_manual

            for pig in pigs:
                if pig.rank != 1 and pig.called_and_won == False and pig.total_points_manual >= high_score:
                    pts_ahead = pig.total_points_manual - high_score
                    old_record = 0
                    if record_pigs.has_key(pig.player):
                        old_record = record_pigs[pig.player][0]
                    if pts_ahead >= old_record:
                        record_pigs[pig.player] = [int(pts_ahead), pig]

        for r in record_pigs.values():
            a.add_player(r[1].player, r[0], r[1].game)
        a.sort(award_sort_descending)
        return a
    
    def get_lowest_win_award(self):
        a = Award("Lowest Winning Score")
                
        # First query ends up giving us the sort

        lowest_wins = {}
        
        for game in Game.objects.all():
            for pig in game.get_records():
                if pig.rank == 1:
                    pl = pig.player
                    if pl in lowest_wins.keys():
                        if pig.total_points_manual < lowest_wins[pl].total_points_manual:
                            lowest_wins[pl] = pig
                    else:
                        lowest_wins[pl] = pig
        for p in lowest_wins.keys():
             pig = lowest_wins[p]
             a.add_player(pig.player, int(pig.total_points_manual), pig.game)

        a.sort(award_sort_ascending)
        return a
#        cursor = connection.cursor() #@UndefinedVariable
#        cursor.execute("""
#            SELECT player_id, MIN(total_points_manual)
#            FROM scoreboard_playedingame
#            WHERE rank=1
#            GROUP BY player_id
#            ORDER BY 2 ASC
#            """)
#        for row in cursor.fetchall():
#            pig = PlayedInGame.objects.get(player=row[0], total_points_manual=row[1])
#            a.add_player(pig.player, pig.total_points_manual, pig.game)
#        return a
    
    def get_highest_average_award(self):
        from django.db import connection
        a = Award("Highest Average Score", 1)

        # First query ends up giving us the sort
        cursor = connection.cursor() #@UndefinedVariable
        cursor.execute("""
            SELECT player_id, AVG(total_points_manual)
            FROM scoreboard_playedingame
            GROUP BY player_id
            ORDER BY 2 DESC
            """)
        for row in cursor.fetchall():
            a.add_player(Player.objects.get(id=row[0]), row[1])
        return a
    
    def get_longest_winning_streak_award(self):
        a = Award("Longest Winning Streak",)

        for p in Player.objects.all():
            streak = 0
            max_streak = 0
            pigs = PlayedInGame.objects.filter(player=p).order_by('game__date')
            for pig in pigs:
                if pig.rank == 1:
                    streak = streak + 1
                    if streak > max_streak:
                        max_streak = streak
                else:
                    streak = 0
            a.add_player(p, max_streak)
        a.sort(award_sort_descending)
        return a
    
    def get_longest_winless_streak_award(self):
        a = Award("Longest Winless Streak",)

        for p in Player.objects.all():
            streak = 0
            max_streak = 0
            pigs = PlayedInGame.objects.filter(player=p).order_by('game__date')
            for pig in pigs:
                if pig.rank != 1:
                    streak = streak + 1
                    if streak > max_streak:
                        max_streak = streak
                else:
                    streak = 0
            a.add_player(p, max_streak)
        a.sort(award_sort_descending)
        return a
    
    def get_longest_winless_streak_current_award(self):
        a = Award("Longest Current Winless Streak",)

        for p in Player.objects.all():
            streak = 0
            pigs = PlayedInGame.objects.filter(player=p).order_by('-game__date')
            for pig in pigs:
                if pig.rank != 1:
                    streak = streak + 1
                else:
                    break
            a.add_player(p, streak)
        a.sort(award_sort_descending)
        return a
    
    def has_star(self, pig):
        return pig.called_and_won
    
    def get_star_streak(self):
        a = StreakAward("Star Streaks", self.has_star, "Star", "Starless")
        return a
    
    def first_place(self, pig):
        return pig.rank == 1
    
    def last_place(self, pig):
        return pig.rank == pig.game.num_players

    def get_win_streak(self):
        a = StreakAward("Win Streaks", self.first_place, "Winning", "Winless")
        return a

    def get_loser_streak(self):
        a = StreakAward("Futility Streaks", self.last_place, "Futile", "Lastless")
        return a    

def award_sort_descending(x, y):
    # [0] = player, [1] = value, [2] = game
    if x[1] != y[1]:
        return y[1] - x[1]
    return x[0] > y[0]

def award_sort_ascending(x, y):
    # [0] = player, [1] = value, [2] = game
    if x[1] != y[1]:
        return x[1] - y[1]
    return x[0] > y[0]


#
#
#  CHARTS
#
#

#xhtml_template = """
#<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
#"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
#<html xmlns="http://www.w3.org/1999/xhtml">
#    <script type="text/javascript" src="/static/swfobject.js"></script>
#    <script type="text/javascript">
#        $js
#    </script>
#<head>
#
#<title>$title</title>
#
#</head>
#
#<body>
#    $body
#</body>
#
#</html>
#"""

#jstpl = Template('swfobject.embedSWF("/static/open-flash-chart.swf","$title", "$width", "$height", "$flash_ver", "expressInstall.swf", {"data-file": "$data_src"});\n')
#dvtpl = Template('<h1>$title</h1><div id="$title"></div><br/>\n')
#
class Chart:
    type = ''
    title = ''
    
    

    width=400
    height=200
    flash_ver='9.0.0'

    data_src = None

    chart = None

    def index(self):
        return self.chart.encode()
    index.exposed = True

    def __init__(self, type, name):
        self.title = name
        self.data_src='/'+name
        self.elements = []
        self.x_axis_labels = []
        self.type = type
        self.y_interval=25
        
    def set_x_axis_labels(self, labels):
        self.x_axis_labels = labels

    def set_y_range(self, low, high):
        self.y_range_low = low
        self.y_range_high = high
        
    def add_values(self, values, label, colour):
        e1 = {}
        e1["type"] = self.type
        e1["alpha"] = 0.5
        e1["colour"] = colour
        e1["text"] = label
        e1["font-size"] = 10
        e1["values"] = values
        e1["dot-size"] = 2
        e1["halo-size"] = 0
        e1["tip"] = label + ": #val#"
        #"tip": "#x_label#:#val#"
        self.elements.append(e1)
        
    def add_values_background(self, values, label):
        e1 = {}
        e1["type"] = "line"
        e1["alpha"] = 0.1
        e1["colour"] = "#666666"
        e1["text"] = label
        e1["font-size"] = 10
        e1["values"] = values
        #"line-style": { "style": "dash", "on": 4, "off": 3 }
        line_style = {}
        line_style["style"] = "dash"
        line_style["on"] = "2"
        line_style["off"] = "6"

        e1["style"] = line_style
        self.elements.append(e1)
    
    def init_y_axis(self):
        # Loop through all of the values, finding the min and the max
        # We'll assume that the difference between the max and the min is around
        # 400-500
        min = 9999
        max = -9999
        for line in self.elements:
            for val in line["values"]:
                if val:
                    if val < min:
                        min = val
                    if val > max:
                        max = val
                    
        # Round up or down to the nearest 50
        
        min = (int(min) / self.y_interval) * self.y_interval
        max = ((int(max) / self.y_interval) * self.y_interval) + self.y_interval
        
        self.y_range_low = min
        self.y_range_high = max
        self.y_steps = self.y_interval  # Number of steps, not size

    def get_js(self):
        self.init_y_axis()
        gd = {}
        gd["title"] = {}
        gd["title"]["text"] = self.title
        gd["title"]["style"] = "{font-size: 20px; color:#0000ff; font-family: Verdana; text-align: center;}"
        
        gd["y_legend"] = {}

        gd["y_legend"]["text"] = self.title
        gd["y_legend"]["style"] = "{color: #736AFF; font-size: 12px;}"


        gd["elements"] = self.elements
        
        x_axis = {}
        x_axis["steps"] = 5
        x_axis["stroke"] = 1
        x_axis["tick_height"] = 10
        x_axis["colour"] = "#d000d0"
        x_axis["grid_colour"] = "#00ff00"
        x_axis["labels"] = {}
        x_axis["labels"]["labels"] = self.x_axis_labels

        gd["x_axis"] = x_axis
        
        y_axis = {}
        y_axis["steps"] = self.y_steps
        y_axis["stroke"] = 1
        y_axis["tick_length"] = 3
        y_axis["colour"] = "#d000d0"
        y_axis["grid_colour"] = "#00ff00"
        y_axis["offset"] = 0
        y_axis["min"] = self.y_range_low
        y_axis["max"] = self.y_range_high
        gd["y_axis"] = y_axis
        
        return gd

#
#class BarChart(Chart):
#    def __init__(self, type, name):
#        Chart.__init__(self, type, name)
#
#        # create the bar element and set its values
#        element = Bar(values=[9,8,7,6,5,4,3,2,1])
#
#        # create the chart and set its title
#        self.chart = ofc2.open_flash_chart(title=str(datetime.datetime.now()))
#        self.chart.add_element(element)
#
#class BarStackChart(Chart):
#    def __init__(self, type, name):
#        Chart.__init__(self, type, name)
#
#        # create the bar element and set its values
#        element = BarStack(values=[ [ 2.5, 5 ], [ 7.5 ], [ 5, { 'val': 5, 'colour': '#ff0000' } ], [ 2, 2, 2, 2, { "val": 2, 'colour': '#ff00ff' } ] ])
#
#        # create the chart and set its title
#        self.chart = ofc2.open_flash_chart(title=str(datetime.datetime.now()))
#        self.chart.set_y_axis(min=0, max=14, steps=7)
#        self.chart.set_x_axis(labels=['a', 'b', 'c', 'd'])
#        self.chart.add_element(element)
#
#class LineChart(Chart):
#    def __init__(self, type, name):
#        Chart.__init__(self, type, name)
#
#        # create the bar element and set its values
#        element = Line(values=[9,8,7,6,5,4,3,2,1])
#
#        # create the chart and set its title
#        self.chart = ofc2.open_flash_chart(title=str(datetime.datetime.now()))
#        self.chart.add_element(element)
