from django.shortcuts import render
from django.http import JsonResponse

def crawl(request):

        return JsonResponse({
                'type' : 'buttons',
                'buttons' : ['1','2']
                })

