from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
def index(request):
    return HttpResponse('HOME_PAGE')
def about(request):
    return HttpResponse("contact")
def contact(request):
    return JsonResponse({'name':'ali'})

