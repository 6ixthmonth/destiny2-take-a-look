from django.shortcuts import render
from django.http import JsonResponse

# import json
import requests

def conntest(request):
    # data = json.loads(request.body)
    
    HEADERS = {"X-API-Key":''}
    response = requests.get("https://www.bungie.net/platform/Destiny/Manifest/InventoryItem/1274330687/", headers=HEADERS);
    inventoryItem = response.json()
    # print(inventoryItem)
    # print(inventoryItem['Response']['data']['inventoryItem']['itemName'])
    itemName = inventoryItem['Response']['data']['inventoryItem']['itemName']

    return JsonResponse({'itemName': itemName})
