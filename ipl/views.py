from django.shortcuts import render
from ipl.models import Matches, Deliveries
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.db import transaction
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count, F, Value,Q
from django.db import connection
from django.db.models import OuterRef, Subquery


def index(request):
    return render(request, 'index.html')

@transaction.atomic
def matchesperyearhc(request):
    
    urlpatttern=reverse(matchesperyear)
    print(urlpatttern)
    return render(request, 'matchesperyear.html', {'urlpattern': urlpatttern})


@transaction.atomic
def matcheswonperyearhc(request):
    output = reverse(matcheswonperyear)
    return render(request, 'matcheswonperyear.html', {'output': output})


@transaction.atomic
def extrarunshc(request):
    output = reverse(extrarunsperteam)
    return render(request, 'extraruns.html', {'output': output})


@transaction.atomic
def economicbowlerhc(request):

    output = reverse(economicbowler)
    print(output)
    return render(request, 'economicalbowlers.html', {'output': output})


@transaction.atomic
def matchesperyear(request):

    output = Matches.objects.values(
        'season').annotate(totalplayed=Count('season'))
    
    return JsonResponse(list(output), safe=False)


@transaction.atomic
def matcheswonperyear(request):
    output = Matches.objects.values('season', 'winner').annotate(
        win=Count('winner')).order_by('season')
    print(output)
    return JsonResponse(list(output), safe=False)


@transaction.atomic
def extrarunsperteam(request):
    output = Deliveries.objects.filter(match_id__season=2016).values(
        'battingteam').annotate(extraruns=Sum('extra_runs'))
    print(output)
    return JsonResponse(list(output), safe=False)


@transaction.atomic
def economicbowler(request):

    output = Deliveries.objects.filter(match_id__season=2015).values('bowler').annotate(
        economy=Cast((Sum('total_runs')*6.0) / Count('total_runs'), FloatField())).order_by('economy')[:10]
    return JsonResponse(list(output), safe=False)

@transaction.atomic
def runsperteam(request):
    output = Deliveries.objects.values('battingteam').annotate(Teamruns=Sum('total_runs')).order_by('Teamruns')
    return JsonResponse(list(output), safe=False)

@transaction.atomic
def toprcbbatsmen(request):
    output = Deliveries.objects.values('batsman').filter(battingteam='Royal Challengers Bangalore').annotate(batsmenruns=Sum('batsman_runs')).order_by('-batsmenruns')[:10]
    return JsonResponse(list(output), safe=False)

def matchesperteam(request):
    # intial_output=Matches.objects.values('team1')
  
    
    
    output_in_team1 = Matches.objects.all().annotate(teamname=F('team1')).values('season','teamname').distinct().annotate(teamcount= Count('teamname'))
    output_in_team2= Matches.objects.all().annotate(teamname=F('team2')).values('season','teamname').distinct().annotate(teamcount= Count('teamname'))
    combined_query = output_in_team1|output_in_team2.values('season','teamname').aggregate(total=Sum('teamcount')).order_by('season','teamname')
    print(combined_query)
                                                             
    # return JsonResponse(list(output), safe=False)
