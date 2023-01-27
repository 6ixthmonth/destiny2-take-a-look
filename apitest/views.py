from django.shortcuts import render
from django.http import JsonResponse

import requests
import json

def conntest(request):
    # data = json.loads(request.body)

    return JsonResponse({'itemName': 'hello'})
