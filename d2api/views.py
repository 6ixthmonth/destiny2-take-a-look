import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from requests_oauthlib import OAuth2Session


def req(request):
    # data = json.loads(request.body)

    base_auth_url = "https://www.bungie.net/en/OAuth/Authorize"
    redirect_url = "https://127.0.0.1:8000/"
    token_url = "https://www.bungie.net/Platform/App/OAuth/token/"
    endpoint_url = "https://www.bungie.net/Platform/"

    # HEADERS = {"X-API-Key": settings.API_KEY}
    # membershipType = 0
    # destinyMembershipId = 0
    # characterId = 0
    # vendorHash = 0
    # components = "0"
    # response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/?components={components}", headers=HEADERS)
    # response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/?components={components}", headers=HEADERS)
    # response = requests.get(f"https://www.bungie.net/Platform/Destiny2/Vendors/?components=402", headers=HEADERS)
    # print(response.json())

    return JsonResponse({'key': 'value'})
