import json
import os
from datetime import timedelta

import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from requests_oauthlib import OAuth2Session, TokenUpdated

from d2api.models import Item, SalesItem, Vendor

HEADERS = {'X-API-Key': settings.API_KEY}
EXTRA = {'client_id': settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET}

CHARACTER_ID_LIST = [settings.TITAN_ID, settings.HUNTER_ID, settings.WARLOCK_ID]
DESTINY_MEMBERSHIP_ID = settings.DESTINY_MEMBERSHIP_ID
MEMBERSHIP_TYPE = settings.MEMBERSHIP_TYPE

REDIRECT_URI = settings.REDIRECT_URI
BASE_URL = "https://www.bungie.net"
MANIFEST_URL = "/Platform/Destiny2/Manifest/"
AUTHORIZATION_URL = "/en/oauth/authorize"
TOKEN_URL = "/platform/app/oauth/token/"
COMPONENTS = "304,402"  # ItemStats, VendorSales

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
        # [177, 178, 179, 180, 181],
        # [147, 148, 149, 150, 151],
        # [102, 103, 104, 105, 106],
        [117, 118, 119, 120, 121],
        [6, 7, 8, 9, 10],
        [6, 7, 8, 9, 10],
    ],  # Titan
    [
        # [172, 173, 174, 175, 176],
        # [142, 143, 144, 145, 146],
        # [97, 98, 99, 100, 101],
        [112, 113, 114, 115, 116],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
    ],  # Hunter
    [
        # [182, 183, 184, 185, 186],
        # [152, 153, 154, 155, 156],
        # [107, 108, 109, 110, 111],
        [122, 123, 124, 125, 126],
        [11, 12, 13, 14, 15],
        [11, 12, 13, 14, 15],
    ],  # Warlock
]
LIMITED_TIME_VENDOR_ITEM_INDEX_LIST = [
    [
        # [238, 239, 240, 241, 242],
        # [448, 449, 450, 451, 452],
        # [208, 209, 210, 211, 212],
        [283, 284, 285, 286, 287],
    ],  # Titan
    [
        # [233, 234, 235, 236, 237],
        # [443, 444, 445, 446, 447],
        # [203, 204, 205, 206, 207],
        [278, 279, 280, 281, 282],
    ],  # Hunter
    [
        # [243, 244, 245, 246, 247],
        # [453, 454, 455, 456, 457],
        # [213, 214, 215, 216, 217],
        [288, 289, 290, 291, 292],
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

def get_manifest(request):
    if not os.path.exists('manifest.json'):
        print("Manifest file not exists.")
        response = requests.get(url=BASE_URL+MANIFEST_URL, headers=HEADERS)
        with open('manifest.json','w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print("Manifest file already exists.")
    return JsonResponse({})

def get_definition(request):
    body = json.loads(request.body)
    param = body['param']
    definition_name = 'Destiny' + "".join(word.capitalize() for word in param.split()) + 'Definition'
    file_name = definition_name + '.json'
    print(f"{definition_name=}, {file_name=}")
    if not os.path.exists(file_name):
        print(f"{definition_name} file not exists.")
        manifest = json.load(open('manifest.json'))
        url = BASE_URL + manifest['Response']['jsonWorldComponentContentPaths']['en'][definition_name]
        response = requests.get(url=url)
        with open(file_name, 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        print(f"{definition_name} file already exists.")
    return JsonResponse({})

def get_auth(request):
    oauth = OAuth2Session(client_id=EXTRA['client_id'], redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url(url=BASE_URL+AUTHORIZATION_URL)
    request.session['oauth_state'] = state
    return JsonResponse({'authorization_url': authorization_url})

def fetch_token(request):
    body = json.loads(request.body)
    oauth = OAuth2Session(client_id=EXTRA['client_id'], state=request.session['oauth_state'])
    token = oauth.fetch_token(token_url=BASE_URL+TOKEN_URL, authorization_response=REDIRECT_URI+body['auth_res'], client_secret=EXTRA['client_secret'])
    request.session['oauth_token'] = token
    return JsonResponse(token)


def get_vendor_data(request):
    membership_type = MEMBERSHIP_TYPE
    destiny_membership_id = DESTINY_MEMBERSHIP_ID
    components = COMPONENTS

    # repeat for the number of characters
    for i in range(len(CHARACTER_ID_LIST)):
        character_id = CHARACTER_ID_LIST[i]
        print(f"{character_id=}")

        # repeat for the number of vendors
        for j in range(len(VENDOR_HASH_LIST)):
            vendor_hash = VENDOR_HASH_LIST[j]
            print(f"\t{vendor_hash=}")

            # request data from api
            url = BASE_URL + f"/Platform/Destiny2/{membership_type}/Profile/{destiny_membership_id}/Character/{character_id}/Vendors/{vendor_hash}/?components={components}"
            headers = HEADERS
            try:
                oauth = OAuth2Session(client_id=EXTRA['client_id'], auto_refresh_url=BASE_URL+TOKEN_URL, auto_refresh_kwargs=EXTRA, token=request.session['oauth_token'])
                response = oauth.get(url=url, headers=headers)
            except TokenUpdated as e:
                print("==========Token has been updated==========")
                print(e.token)
                print("==========New token will be saved==========")
                request.session['oauth_token'] = e.token
                response = oauth.get(url=url, headers=headers)
            response = response.json()['Response']
            sales_data = response['sales']['data']
            stats_data = response['itemComponents']['stats']['data']

            for vendor_item_index in VENDOR_ITEM_INDEX_LIST[i][j]:
                item_hash = sales_data[str(vendor_item_index)]['itemHash']
                print(f"\t\t{item_hash=}")

                if not Item.objects.filter(item_hash=item_hash).exists():
                    destiny_inventory_item_definition = json.load(open('DestinyInventoryItemDefinition.json'))
                    item_name = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']
                    item_type = destiny_inventory_item_definition[str(item_hash)]['itemTypeDisplayName']
                    class_type = destiny_inventory_item_definition[str(item_hash)]['classType']
                    icon_url = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['icon']
                    Item.objects.create(item_hash=item_hash, item_name=item_name, item_type=item_type, class_type=class_type, icon_url=icon_url)

                if not Vendor.objects.filter(vendor_hash=vendor_hash).exists():
                    destiny_vendor_definition = json.load(open('DestinyVendorDefinition.json'))
                    vendor_name = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['name']
                    icon_url = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['largeIcon']
                    Vendor.objects.create(vendor_hash=vendor_hash, vendor_name=vendor_name, icon_url=icon_url)

                new_sales_item = SalesItem.objects.create(item_hash_id=sales_data[str(vendor_item_index)]['itemHash'], vendor_hash_id=vendor_hash)

                # setting stats
                stats = stats_data[str(vendor_item_index)]['stats']
                for stat_hash in STAT_HASH_LIST:
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
    return JsonResponse({})


def get_limited_time_vendor_data(request):
    membership_type = MEMBERSHIP_TYPE
    destiny_membership_id = DESTINY_MEMBERSHIP_ID
    components = COMPONENTS

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
            headers = HEADERS
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
                print(f"\t\t{item_hash=}")

                if not Item.objects.filter(item_hash=item_hash).exists():
                    destiny_inventory_item_definition = json.load(open('destinyInventoryItemDefinition.json'))
                    item_name = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']
                    item_type = destiny_inventory_item_definition[str(item_hash)]['itemTypeDisplayName']
                    class_type = destiny_inventory_item_definition[str(item_hash)]['classType']
                    icon_url = destiny_inventory_item_definition[str(item_hash)]['displayProperties']['icon']
                    Item.objects.create(item_hash=item_hash, item_name=item_name, item_type=item_type, class_type=class_type, icon_url=icon_url)

                if not Vendor.objects.filter(vendor_hash=vendor_hash).exists():
                    destiny_vendor_definition = json.load(open('DestinyVendorDefinition.json'))
                    vendor_name = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['name']
                    icon_url = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['largeIcon']
                    Vendor.objects.create(vendor_hash=vendor_hash, vendor_name=vendor_name, icon_url=icon_url)

                new_sales_item = SalesItem.objects.create(item_hash_id=sales_data[str(vendor_item_index)]['itemHash'], vendor_hash_id=vendor_hash)

                # setting stats
                stats = stats_data[str(vendor_item_index)]['stats']
                for stat_hash in STAT_HASH_LIST:
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
    return JsonResponse({})
