from django.shortcuts import render
from ipl.models import Matches, Deliveries
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.db import transaction
from django.db.models.functions import Cast
from django.db.models import FloatField


def index(request):
    return render(request, 'index.html')

# def matchesperyearhc(request):

#     output = Matches.objects.values(
#         'season').annotate(totalplayed=Count('season'))
#     return render(request, 'matchesperyear.html', {'output': output})


# def matcheswonperyearhc(request):
#     output = Matches.objects.values('season', 'winner').annotate(
#         win=Count('winner')).order_by('season')
#     print(output)
#     return render(request, 'matcheswonperyear.html', {'output': output})


# def extrarunshc(request):
#     output = Deliveries.objects.filter(match_id__season=2016).values(
#         'battingteam').annotate(extraruns=Sum('extra_runs'))
#     print(output)
#     return render(request, 'extraruns.html', {'output': output})


# def economicbowlerhc(request):

#     output = Deliveries.objects.filter(match_id__season=2015).values('bowler').annotate(
#         economy=Sum('total_runs')*6/Count('total_runs')).order_by('economy')[:10]
#     return render(request, 'economicalbowlers.html', {'output': output})

@transaction.atomic
def matchesperyearhc(request):
    output = matchesperyear(request)
    return render(request, 'matchesperyear.html', {'output': output})


@transaction.atomic
def matcheswonperyearhc(request):
    output = matcheswonperyear(request)
    return render(request, 'matcheswonperyear.html', {'output': output})


@transaction.atomic
def extrarunshc(request):
    output = extrarunsperteam(request)
    return render(request, 'extraruns.html', {'output': output})


@transaction.atomic
def economicbowlerhc(request):

    output = economicbowler(request)
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
