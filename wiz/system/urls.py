from django.conf.urls.defaults import patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #'django.contrib.auth.views.login',
    (r'^$', 'system.scoreboard.views.leaderboard'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^leaderboard/$', 'system.scoreboard.views.leaderboard'),
    (r'^leaderboard/(?P<player_id>\d+)/$', 'system.scoreboard.views.players'),
    (r'^entry/$', 'system.scoreboard.views.entry'),
    (r'^games/$', 'system.scoreboard.views.games'),
    (r'^game/(?P<game_id>\d+)/$', 'system.scoreboard.views.game'),
    (r'^games/(?P<page>\d+)/$', 'system.scoreboard.views.games'),
    (r'^games/recent/$', 'system.scoreboard.views.games'),
    (r'^awards/$', 'system.scoreboard.views.awards'),
    (r'^graph/$', 'system.scoreboard.views.graph'),
    (r'^graph/(?P<data_type>\w+)/(?P<start_date>\w+)/(?P<end_date>\w+)/$', 'system.scoreboard.views.graph'),
    (r'^graph/data/(?P<data_type>\w+)/(?P<start_date>\w+)/(?P<end_date>\w+)/$', 'system.scoreboard.views.graph_data'),
)
