from django.shortcuts import render, redirect
from django.http import JsonResponse

from .logic import main
context = {}

main.trainGenAlgo()

def home(requests) :
    graphData = main.getData()
    context = {
        # xDataPoints = x
        # yDataPoints = y
        'zDataPoints' : graphData['Z'],
        'firstZ' : graphData['Z'][0],
        'totalChanges' : len(graphData['Z'])-1
    }
    return render(requests, 'home.html', context)

def prediction(requests):
    return {}

def geneticAlgo(requests):
    return {}