from django.shortcuts import render, redirect
from django.http import JsonResponse

from .logic import main
context = {}

main.trainGenAlgo()

def home(request) :
    context = {
        'activeTab' : "dashboard",
    }
    return render(request, 'dashboard.html', context)

def prediction(request):
    price = -1
    if 'area' in request.GET :
        print("true")
        price = main.predictPrice(int(request.GET['area']), int(request.GET['rooms']))

    context = {
        'activeTab' : "prediction",
        'price' : price,
    }
    return render(request, 'prediction.html', context)

def geneticAlgo(request):
    graphData = main.getData()
    context = {
        'activeTab' : "geneticAlgo",
        'zDataPoints' : graphData['Z'],
        'firstZ' : graphData['Z'][0],
        'totalChanges' : len(graphData['Z'])-1
    }

    return render(request, 'geneticAlgo.html', context)