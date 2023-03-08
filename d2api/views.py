import json
import os
from datetime import timedelta

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView
from requests_oauthlib import OAuth2Session, TokenUpdated

from d2api.models import Item, SalesItem, Vendor

API_KEY = settings.API_KEY
EXTRA = {'client_id': settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET}

CHARACTER_ID_LIST = [settings.TITAN_ID, settings.HUNTER_ID, settings.WARLOCK_ID]
DESTINY_MEMBERSHIP_ID = settings.DESTINY_MEMBERSHIP_ID
MEMBERSHIP_TYPE = settings.MEMBERSHIP_TYPE

REDIRECT_URI = "https://127.0.0.1:8000/d2api/"
AUTHORIZATION_URL = "https://www.bungie.net/en/oauth/authorize"
TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"

VENDOR_HASH_LIST = [
    350061650,  # Ada-1
    396892126,  # Devrim Kay
    1576276905,  # Failsafe
]
LIMITED_TIME_VENDOR_HASH_LIST = [
    2190858386,  # Xûr
]
VENDOR_ITEM_INDEX_LIST = [
    [
        [177, 178, 179, 180, 181],
        [6, 7, 8, 9, 10],
        [6, 7, 8, 9, 10],
    ],  # Titan
    [
        [172, 173, 174, 175, 176],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
    ],  # Hunter
    [
        [182, 183, 184, 185, 186],
        [11, 12, 13, 14, 15],
        [11, 12, 13, 14, 15],
    ],  # Warlock
]
LIMITED_TIME_VENDOR_ITEM_INDEX_LIST = [
    [
        [238, 239, 240, 241, 242],
    ],  # Titan
    [
        [233, 234, 235, 236, 237],
    ],  # Hunter
    [
        [243, 244, 245, 246, 247],
    ],  # Warlock
]
STAT_HASH_LIST = [
    2996146975,  # Mobility
    392767087,  # Resilience
    1943323491,  # Recovery
    1735777505,  # Discipline
    144602215,  # Intellect
    4244567218,  # Strength
]
COMPONENTS = "304,402"  # ItemStats, VendorSales


class Home(ListView):
    template_name = "d2api/index.html"

    def get_queryset(self):
        queryset = SalesItem.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def get_manifest(request):
    if not os.path.isfile('manifest.json'):
        print("Manifest file not exists.")
        manifest_url = 'http://www.bungie.net/Platform/Destiny2/Manifest/'
        headers = {"X-API-Key": API_KEY}
        response = requests.get(manifest_url, headers=headers)
        manifest = response.json()
        with open('manifest.json','w') as f:
            json.dump(manifest, f, indent=4)
    else:
        print("Manifest file already exists.")
        manifest = open('manifest.json')
        manifest = json.load(manifest)

    if not os.path.isfile('destiny-inventory-item-definition.json'):
        print("DestinyInventoryItemDefinition file not exists.")
        destiny_inventory_item_definition_url = 'http://www.bungie.net'+manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyInventoryItemDefinition']
        response = requests.get(destiny_inventory_item_definition_url)
        with open('destiny-inventory-item-definition.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print("DestinyInventoryItemDefinition file already exists.")
    
    if not os.path.isfile('destiny-stat-definition.json'):
        print("DestinyStatDefinition file not exists.")
        destiny_stat_definition_url = 'http://www.bungie.net'+manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyStatDefinition']
        response = requests.get(destiny_stat_definition_url)
        with open('destiny-stat-definition.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print("DestinyStatDefinition file already exists.")

    if not os.path.isfile('destiny-vendor-definition.json'):
        print("DestinyVendorDefinition file not exists.")
        destiny_vendor_definition_url = 'http://www.bungie.net'+manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyVendorDefinition']
        response = requests.get(destiny_vendor_definition_url)
        with open('destiny-vendor-definition.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print("DestinyVendorDefinition file already exists.")

    return JsonResponse({})


def get_auth(request):
    oauth = OAuth2Session(client_id=EXTRA['client_id'], redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url(url=AUTHORIZATION_URL)
    request.session['oauth_state'] = state

    return JsonResponse({'authorization_url': authorization_url})


def fetch_token(request):
    body = json.loads(request.body)

    oauth = OAuth2Session(client_id=EXTRA['client_id'], state=request.session['oauth_state'])
    token = oauth.fetch_token(token_url=TOKEN_URL, authorization_response=REDIRECT_URI+body['auth_res'], client_secret=EXTRA['client_secret'])
    request.session['oauth_token'] = token

    return JsonResponse(token)


def get_data(request):
    membership_type = MEMBERSHIP_TYPE
    destiny_membership_id = DESTINY_MEMBERSHIP_ID
    components = COMPONENTS

    destiny_inventory_item_definition = json.load(open('destiny-inventory-item-definition.json'))

    # repeat for the number of characters
    for i in range(len(CHARACTER_ID_LIST)):
        character_id = CHARACTER_ID_LIST[i]
        print(f"{character_id=}")

        # repeat for the number of vendors
        for j in range(len(VENDOR_HASH_LIST)):
            vendor_hash = VENDOR_HASH_LIST[j]
            print(f"\t{vendor_hash=}")

            # request data from api
            endpoint_url = f"https://www.bungie.net/Platform/Destiny2/{membership_type}/Profile/{destiny_membership_id}/Character/{character_id}/Vendors/{vendor_hash}/?components={components}"
            headers = {"X-API-Key": API_KEY}
            try:
                oauth = OAuth2Session(client_id=EXTRA['client_id'], auto_refresh_url=TOKEN_URL, auto_refresh_kwargs=EXTRA, token=request.session['oauth_token'])
                response = oauth.get(url=endpoint_url, headers=headers)
            except TokenUpdated as e:
                print("==========Token has been updated==========")
                print(e.token)
                print("==========New token will be saved==========")
                request.session['oauth_token'] = e.token
                response = oauth.get(url=endpoint_url, headers=headers)
            response = response.json()['Response']
            sales_data = response['sales']['data']
            stats_data = response['itemComponents']['stats']['data']

            for vendor_item_index in VENDOR_ITEM_INDEX_LIST[i][j]:
                item_hash = sales_data[str(vendor_item_index)]['itemHash']
                print(f"\t\t{vendor_item_index=}, {item_hash=}, name={destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']}")

                if not Item.objects.filter(item_hash=item_hash).exists():
                    item_name = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']
                    item_type = destiny_inventory_item_definition[str(item_hash)]['itemTypeDisplayName']
                    class_type = destiny_inventory_item_definition[str(item_hash)]['classType']
                    icon_url = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['icon']
                    Item.objects.create(item_hash=item_hash, item_name=item_name, item_type=item_type, class_type=class_type, icon_url=icon_url)

                if not Vendor.objects.filter(vendor_hash=vendor_hash).exists():
                    Vendor.objects.create(vendor_hash=vendor_hash, vendor_name="", icon_url="")

                new_sales_item = SalesItem.objects.create(item_hash_id=sales_data[str(vendor_item_index)]['itemHash'], vendor_hash_id=vendor_hash)
                stats = stats_data[str(vendor_item_index)]['stats']
                for stat_hash in STAT_HASH_LIST:
                    print(f"\t\t\t{stat_hash=}, value={stats[str(stat_hash)]['value']}")
                    match(STAT_HASH_LIST.index(stat_hash)):
                        case 0:
                            new_sales_item.mobility = stats[str(stat_hash)]['value']
                        case 1:
                            new_sales_item.resilience = stats[str(stat_hash)]['value']
                        case 2:
                            new_sales_item.recovery = stats[str(stat_hash)]['value']
                        case 3:
                            new_sales_item.discipline = stats[str(stat_hash)]['value']
                        case 4:
                            new_sales_item.intellect = stats[str(stat_hash)]['value']
                        case 5:
                            new_sales_item.strength = stats[str(stat_hash)]['value']
                        case _:
                            pass
                
                # calculate sales date
                today = timezone.now()
                weekday = today.weekday()
                if weekday > 1:
                    # 2 ~ 6 = wed ~ sun
                    sales_date = today - timedelta(days=weekday-1)
                elif weekday < 1:
                    # 0 = mon
                    sales_date = today - timedelta(days=weekday+6)
                else:
                    # 1 = tue
                    if today.hour < 17:
                        sales_date = today - timedelta(days=7)
                    else:
                        sales_date = today
                sales_date = sales_date.replace(hour=17, minute=0, second=0, microsecond=0)  # pst 9 = utc 17 = kst 26
                new_sales_item.sales_date = sales_date

                new_sales_item.save()
    return JsonResponse(stats_data)


def get_limited_time_vendor_data(request):
    membership_type = MEMBERSHIP_TYPE
    destiny_membership_id = DESTINY_MEMBERSHIP_ID
    components = COMPONENTS

    destiny_inventory_item_definition = json.load(open('destiny-inventory-item-definition.json'))

    # repeat for the number of characters
    for i in range(len(CHARACTER_ID_LIST)):
        character_id = CHARACTER_ID_LIST[i]
        print(f"{character_id=}")

        # repeat for the number of vendors
        for j in range(len(LIMITED_TIME_VENDOR_HASH_LIST)):
            vendor_hash = LIMITED_TIME_VENDOR_HASH_LIST[j]
            print(f"\t{vendor_hash=}")

            # request data from api
            endpoint_url = f"https://www.bungie.net/Platform/Destiny2/{membership_type}/Profile/{destiny_membership_id}/Character/{character_id}/Vendors/{vendor_hash}/?components={components}"
            headers = {"X-API-Key": API_KEY}
            try:
                oauth = OAuth2Session(client_id=EXTRA['client_id'], auto_refresh_url=TOKEN_URL, auto_refresh_kwargs=EXTRA, token=request.session['oauth_token'])
                response = oauth.get(url=endpoint_url, headers=headers)
            except TokenUpdated as e:
                print("==========Token has been updated==========")
                print(e.token)
                print("==========New token will be saved==========")
                request.session['oauth_token'] = e.token
                response = oauth.get(url=endpoint_url, headers=headers)
            response = response.json()['Response']
            sales_data = response['sales']['data']
            stats_data = response['itemComponents']['stats']['data']

            for vendor_item_index in LIMITED_TIME_VENDOR_ITEM_INDEX_LIST[i][j]:
                item_hash = sales_data[str(vendor_item_index)]['itemHash']
                print(f"\t\t{vendor_item_index=}, {item_hash=}, name={destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']}")

                if not Item.objects.filter(item_hash=item_hash).exists():
                    item_name = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']
                    item_type = destiny_inventory_item_definition[str(item_hash)]['itemTypeDisplayName']
                    class_type = destiny_inventory_item_definition[str(item_hash)]['classType']
                    icon_url = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['icon']
                    Item.objects.create(item_hash=item_hash, item_name=item_name, item_type=item_type, class_type=class_type, icon_url=icon_url)

                if not Vendor.objects.filter(vendor_hash=vendor_hash).exists():
                    Vendor.objects.create(vendor_hash=vendor_hash, vendor_name="", icon_url="")

                new_sales_item = SalesItem.objects.create(item_hash_id=sales_data[str(vendor_item_index)]['itemHash'], vendor_hash_id=vendor_hash)
                stats = stats_data[str(vendor_item_index)]['stats']
                for stat_hash in STAT_HASH_LIST:
                    print(f"\t\t\t{stat_hash=}, value={stats[str(stat_hash)]['value']}")
                    match(STAT_HASH_LIST.index(stat_hash)):
                        case 0:
                            new_sales_item.mobility = stats[str(stat_hash)]['value']
                        case 1:
                            new_sales_item.resilience = stats[str(stat_hash)]['value']
                        case 2:
                            new_sales_item.recovery = stats[str(stat_hash)]['value']
                        case 3:
                            new_sales_item.discipline = stats[str(stat_hash)]['value']
                        case 4:
                            new_sales_item.intellect = stats[str(stat_hash)]['value']
                        case 5:
                            new_sales_item.strength = stats[str(stat_hash)]['value']
                        case _:
                            pass
                
                # calculate sales date
                today = timezone.now()
                weekday = today.weekday()
                if weekday > 4:
                    # 5 ~ 6 = sat ~ sun
                    sales_date = today - timedelta(days=weekday-4)
                elif weekday < 4:
                    # 0 ~ 3 = mon ~ thu
                    sales_date = today - timedelta(days=weekday+3)
                else:
                    # 4 = fri
                    if today.hour < 17:
                        sales_date = today - timedelta(days=7)
                    else:
                        sales_date = today
                sales_date = sales_date.replace(hour=17, minute=0, second=0, microsecond=0)  # pst 9 = utc 17 = kst 26
                new_sales_item.sales_date = sales_date

                new_sales_item.save()
    return JsonResponse(stats_data)
