import json
from django.shortcuts import render
from django.http import JsonResponse
from Crawling.Crawl import Crawl
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def crawl(request):
        req = ((request.body).decode('utf-8'))
        return_json_str = json.loads(req)
        mid = return_json_str['mid']

        obj = Crawl()

        return JsonResponse({
                'type' : 'buttons',
                'buttons' : ['1','2']
                })

