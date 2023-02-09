from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# import json
import requests

def req(request):
    # data = json.loads(request.body)

    HEADERS = {"X-API-Key": settings.API_KEY}
    membershipType = 0
    destinyMembershipId = 0
    characterId = 0
    vendorHash = 0
    components = "0"
    # response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/?components={components}", headers=HEADERS)
    response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/?components={components}", headers=HEADERS)
    print(response.json())

    return JsonResponse({'key': 'value'})
