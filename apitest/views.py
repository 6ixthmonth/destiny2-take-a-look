from django.shortcuts import render
from django.http import JsonResponse

import requests
import json

def conntest(request):
    # data = json.loads(request.body)
    
    #dictionary to hold extra headers
    HEADERS = {"X-API-Key":''}

    #make request for Gjallarhorn
    r = requests.get("https://www.bungie.net/platform/Destiny/Manifest/InventoryItem/1274330687/", headers=HEADERS);

    #convert the json object we received into a Python dictionary object
    #and print the name of the item
    inventoryItem = r.json()
    # print(inventoryItem)
    # print(inventoryItem['Response']['data']['inventoryItem']['itemName'])
    itemName = inventoryItem['Response']['data']['inventoryItem']['itemName']

    #Gjallarhorn

    return JsonResponse({'itemName': itemName})
