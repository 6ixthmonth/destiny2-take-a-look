import json
import os
from datetime import timedelta

import pandas as pd
import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from keras.models import load_model
from requests_oauthlib import OAuth2Session, TokenUpdated

from dbapp.models import Item, SalesItem, Vendor

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
STAT_HASH_LIST = [
    2996146975,  # Mobility
    392767087,  # Resilience
    1943323491,  # Recovery
    1735777505,  # Discipline
    144602215,  # Intellect
    4244567218,  # Strength
]

def get_events(request):
    result = []
    for salesitem in SalesItem.objects.values('vendor_hash__vendor_name', 'sales_date').distinct():
        result.append({
            'title': salesitem['vendor_hash__vendor_name'],
            'start': salesitem['sales_date'].strftime("%Y-%m-%dT%H:%M:%SZ"),
            'end': (salesitem['sales_date'] + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ") if salesitem['vendor_hash__vendor_name'] == 'Xûr' else (salesitem['sales_date'] + timedelta(days=6)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
    return JsonResponse({
        'result': result
    })

def get_manifest(request):
    file_name = 'manifest/manifest.json'
    if not os.path.exists(file_name):
        response = requests.get(url=BASE_URL+MANIFEST_URL, headers=HEADERS)
        with open(file_name, 'w') as f:
            json.dump(response.json(), f, indent=4)
        print("Manifest file has been saved.")
    else:
        print("Manifest file already exists.")
    return JsonResponse({})

def get_definition(request):
    # check manifest file whether exists or not.
    if not os.path.exists('manifest/manifest.json'):
        print("Download manifest file first.")
        return JsonResponse({})
    else:
        manifest = json.load(open('manifest/manifest.json'))
    
    body = json.loads(request.body)
    param = body['param']
    definition_name = 'Destiny' + "".join(word.capitalize() for word in param.split()) + 'Definition'
    file_name = 'manifest/' + definition_name + '.json'
    
    if not os.path.exists(file_name):
        response = requests.get(url=BASE_URL+manifest['Response']['jsonWorldComponentContentPaths']['en'][definition_name])
        with open(file_name, 'w') as f:
            json.dump(response.json(), f, indent=4)
        print(f"{definition_name} file has been saved.")
    else:
        print(f"{definition_name} file already exists.")
    return JsonResponse({})

def get_auth(request):
    oauth = OAuth2Session(client_id=EXTRA['client_id'], redirect_uri=REDIRECT_URI)
    auth_url, state = oauth.authorization_url(url=BASE_URL+AUTHORIZATION_URL)
    request.session['state'] = state
    return JsonResponse({'auth_url': auth_url})

def fetch_token(request):
    body = json.loads(request.body)
    oauth = OAuth2Session(client_id=EXTRA['client_id'], state=request.session['state'])
    token = oauth.fetch_token(token_url=BASE_URL+TOKEN_URL, authorization_response=REDIRECT_URI+body['authRes'], client_secret=EXTRA['client_secret'])
    request.session['token'] = token
    return JsonResponse(token)

def calculate_sales_date():
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
    sales_date = sales_date.replace(hour=17, minute=0, second=0, microsecond=0)
    return sales_date

def get_vendor_data(request):
    # check whether sales item exists or not.
    sales_date = calculate_sales_date()
    if SalesItem.objects.filter(sales_date=sales_date).exists():
        print("data already exists.")
        return JsonResponse({})

    membership_type = MEMBERSHIP_TYPE
    destiny_membership_id = DESTINY_MEMBERSHIP_ID
    components = COMPONENTS

    destiny_inventory_item_definition = json.load(open('manifest/DestinyInventoryItemDefinition.json'))

    # repeat for the number of characters
    for i in range(len(CHARACTER_ID_LIST)):
        character_id = CHARACTER_ID_LIST[i]
        print(f"{character_id=}")

        # repeat for the number of vendors
        for j in range(len(VENDOR_HASH_LIST)):
            vendor_hash = VENDOR_HASH_LIST[j]
            if not Vendor.objects.filter(vendor_hash=vendor_hash).exists():
                destiny_vendor_definition = json.load(open('manifest/DestinyVendorDefinition.json'))
                vendor_name = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['name']
                icon_url = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['largeIcon']
                Vendor.objects.create(vendor_hash=vendor_hash, vendor_name=vendor_name, icon_url=icon_url)
            print(f"\t{vendor_hash=}")

            # request data from api
            url = BASE_URL + f"/Platform/Destiny2/{membership_type}/Profile/{destiny_membership_id}/Character/{character_id}/Vendors/{vendor_hash}/?components={components}"
            headers = HEADERS
            try:
                oauth = OAuth2Session(client_id=EXTRA['client_id'], auto_refresh_url=BASE_URL+TOKEN_URL, auto_refresh_kwargs=EXTRA, token=request.session['token'])
                response = oauth.get(url=url, headers=headers)
            except TokenUpdated as e:
                print("==========Token has been updated==========")
                request.session['token'] = e.token
                print("==========New token has been saved==========")
                response = oauth.get(url=url, headers=headers)
            response = response.json()['Response']
            sales_data = response['sales']['data']

            # repeat for the number of sales items.
            for item_index in sales_data:
                # check whether item hash exists in definition or not.
                item_hash = sales_data[item_index].get('itemHash')
                if item_hash is None or str(item_hash) not in destiny_inventory_item_definition:
                    continue
                # check whether item type is armor or not.
                item_type = destiny_inventory_item_definition[str(item_hash)].get('itemType')
                if item_type is None or item_type != 2:
                    continue
                print(f"\t\t{item_hash=}")

                # Create new Item data if not exists in DB.
                if not Item.objects.filter(item_hash=item_hash).exists():
                    item = destiny_inventory_item_definition[str(item_hash)]
                    item_name = item['displayProperties']['name']
                    item_type = item['itemTypeDisplayName']
                    class_type = item['classType']
                    icon_url = item['displayProperties']['icon']
                    Item.objects.create(item_hash=item_hash, item_name=item_name, item_type=item_type, class_type=class_type, icon_url=icon_url)

                # Create new SalesItem data to insert into DB.
                new_sales_item = SalesItem.objects.create(item_hash_id=item_hash, vendor_hash_id=vendor_hash)

                # set stats.
                stats = response['itemComponents']['stats']['data'][item_index]['stats']
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
                
                # set sales date.
                new_sales_item.sales_date = sales_date

                # Insert into DB.
                new_sales_item.save()
    return JsonResponse({})

def calculate_limited_time_sales_date():
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
    return sales_date

def get_limited_time_vendor_data(request):
    # check whether sales item exists or not.
    sales_date = calculate_limited_time_sales_date()
    if SalesItem.objects.filter(sales_date=sales_date).exists():
        print("data already exists.")
        return JsonResponse({})

    membership_type = MEMBERSHIP_TYPE
    destiny_membership_id = DESTINY_MEMBERSHIP_ID
    components = COMPONENTS

    destiny_inventory_item_definition = json.load(open('manifest/DestinyInventoryItemDefinition.json'))

    # repeat for the number of characters
    for i in range(len(CHARACTER_ID_LIST)):
        character_id = CHARACTER_ID_LIST[i]
        print(f"{character_id=}")

        # repeat for the number of vendors
        for j in range(len(LIMITED_TIME_VENDOR_HASH_LIST)):
            vendor_hash = LIMITED_TIME_VENDOR_HASH_LIST[j]
            if not Vendor.objects.filter(vendor_hash=vendor_hash).exists():
                destiny_vendor_definition = json.load(open('manifest/DestinyVendorDefinition.json'))
                vendor_name = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['name']
                icon_url = destiny_vendor_definition[str(vendor_hash)]['displayProperties']['largeIcon']
                Vendor.objects.create(vendor_hash=vendor_hash, vendor_name=vendor_name, icon_url=icon_url)
            print(f"\t{vendor_hash=}")

            # request data from api
            url = BASE_URL + f"/Platform/Destiny2/{membership_type}/Profile/{destiny_membership_id}/Character/{character_id}/Vendors/{vendor_hash}/?components={components}"
            headers = HEADERS
            try:
                oauth = OAuth2Session(client_id=EXTRA['client_id'], auto_refresh_url=BASE_URL+TOKEN_URL, auto_refresh_kwargs=EXTRA, token=request.session['token'])
                response = oauth.get(url=url, headers=headers)
            except TokenUpdated as e:
                print("==========Token has been updated==========")
                request.session['token'] = e.token
                print("==========New token has been saved==========")
                response = oauth.get(url=url, headers=headers)
            response = response.json()['Response']
            sales_data = response['sales']['data']

            # repeat for the number of sales items.
            for item_index in sales_data:
                # check whether item hash exists in definition or not.
                item_hash = sales_data[item_index].get('itemHash')
                if item_hash is None or str(item_hash) not in destiny_inventory_item_definition:
                    continue
                # check whether item type is armor or not.
                item_type = destiny_inventory_item_definition[str(item_hash)].get('itemType')
                if item_type is None or item_type != 2:
                    continue
                if SalesItem.objects.filter(item_hash_id=item_hash, sales_date=sales_date):
                    print(f"\t\skip => {destiny_inventory_item_definition[str(item_hash)]['displayProperties']['name']}")
                    continue
                print(f"\t\t{item_hash=}")

                if not Item.objects.filter(item_hash=item_hash).exists():
                    item = destiny_inventory_item_definition[str(item_hash)]
                    item_name = item['displayProperties']['name']
                    item_type = item['itemTypeDisplayName']
                    class_type = item['classType']
                    icon_url = item['displayProperties']['icon']
                    Item.objects.create(item_hash=item_hash, item_name=item_name, item_type=item_type, class_type=class_type, icon_url=icon_url)

                new_sales_item = SalesItem.objects.create(item_hash_id=item_hash, vendor_hash_id=vendor_hash)

                # setting stats.
                stats = response['itemComponents']['stats']['data'][item_index]['stats']
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
                
                # setting sales date.
                new_sales_item.sales_date = sales_date

                new_sales_item.save()
    return JsonResponse({})

def update_item(request):
    body = json.loads(request.body)
    class_type = body['classType']

def predict_item(request):
    body = json.loads(request.body)
    class_type = body['classType']
    match class_type:
        case 0:
            class_model = load_model("weights/titan.h5")
        case 1:
            class_model = load_model("weights/hunter.h5")
        case 2:
            class_model = load_model("weights/warlock.h5")
    common_model = load_model("weights/common.h5")

    item_list = SalesItem.objects.filter(item_hash__item_type__in=['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor'], item_hash__class_type=class_type, pve_recommendation=0, pvp_recommendation=0)
    for item in item_list:
        x_test1 = pd.DataFrame([[item.mobility, item.resilience, item.recovery]])
        x_test1 = (x_test1 - 2) / 28
        result1 = class_model.predict(x_test1)
        x_test2 = pd.DataFrame([[item.discipline, item.intellect, item.strength]])
        x_test2 = (x_test2 - 2) / 28
        result2 = common_model.predict(x_test2)
        item.pve_recommendation = round((result1[0][0] + result2[0][0]) / 2, 6)
        item.pvp_recommendation = round((result1[0][1] + result2[0][1]) / 2, 6)
        item.save()

    return JsonResponse({})
