from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matchesplayedhighcharts', views.matchesperyearhc, name="matchesplayedhc"),
    path('matcheswonperyearhighcharts',
         views.matcheswonperyearhc, name='matcheswonperyearhc'),
    path('extrarunshighcharts', views.extrarunshc, name='extrarunshc'),
    path('economicbowlerhighcharts',
         views.economicbowlerhc, name='economicbowlerhc'),

    path('matchesplayed', views.matchesperyear, name="matchesplayed"),
    path('matcheswon', views.matcheswonperyear, name='matcheswonperyear'),
    path('extrarunsperteam', views.extrarunsperteam, name='extrarunsperteam'),
    path('economicbowler', views.economicbowler, name='economicbowler'),

]
