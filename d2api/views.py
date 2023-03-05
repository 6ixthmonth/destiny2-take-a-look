import json
from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from requests_oauthlib import OAuth2Session, TokenUpdated

from d2api.models import Item, SalesItem, Vendor

API_KEY = settings.API_KEY
EXTRA = {'client_id': settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET}

CHARACTER_ID_LIST = [settings.TITAN_ID, settings.HUNTER_ID, settings.WARLOCK_ID]
DESTINY_MEMBERSHIP_ID = settings.DESTINY_MEMBERSHIP_ID
MEMBERSHIP_TYPE = settings.MEMBERSHIP_TYPE

REDIRECT_URI = "https://127.0.0.1:8000/"
AUTHORIZATION_URL = "https://www.bungie.net/en/oauth/authorize"
TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"
BASE_PATH = "https://www.bungie.net/Platform"

VENDOR_HASH_LIST = [
    # 350061650,  # Ada-1
    # 396892126,  # Devrim Kay
    # 1576276905,  # Failsafe
    # 2190858386,  # Xûr
]
VENDOR_ITEM_INDEX_LIST = [
    [
        [110, 111, 112, 113, 114],
    ],  # Titan
    [
        [105, 106, 107, 108, 109],
    ],  # Hunter
    [
        [115, 116, 117, 118, 119],
    ],  # Warlock
]
ITEM_INDEX_TO_ITEM_HASH = {
    '110': 212971972,
    '111': 2999584444,
    '112': 456484913,
    '113': 1537128821,
    '114': 2143618030,
    '105': 619556600,
    '106': 469333264,
    '107': 3691455821,
    '108': 4076604385,
    '109': 2949791538,
    '115': 671664021,
    '116': 1080431755,
    '117': 4156676002,
    '118': 3611754012,
    '119': 2713820407,
}
STAT_HASH_LIST = [
    2996146975,  # Mobility
    392767087,  # Resilience
    1943323491,  # Recovery
    1735777505,  # Discipline
    144602215,  # Intellect
    4244567218,  # Strength
]
COMPONENTS = "304,402"  # ItemStats, VendorSales


def home(request):
    context = {}
    return render(request, 'd2api/index.html', context)


def admin(request):
    return render(request, 'd2api/admin.html')


def get_auth(request):
    oauth = OAuth2Session(client_id=EXTRA['client_id'], redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url(url=AUTHORIZATION_URL)
    request.session['oauth_state'] = state

    return JsonResponse({'authorization_url': authorization_url})


def fetch_token(request):
    data = json.loads(request.body)

    oauth = OAuth2Session(client_id=EXTRA['client_id'], state=request.session['oauth_state'])
    token = oauth.fetch_token(token_url=TOKEN_URL, authorization_response=REDIRECT_URI+data['auth_res'], client_secret=EXTRA['client_secret'])
    request.session['oauth_token'] = token

    return JsonResponse(token)


def request_data(request):
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
                print(f"\t{vendor_item_index=}")
                new_sales_item = SalesItem.objects.create(item_hash_id=sales_data[str(vendor_item_index)]['itemHash'], vendor_hash_id=vendor_hash)
                stats = stats_data[str(vendor_item_index)]['stats']
                for stat_hash in STAT_HASH_LIST:
                    print(f"\t\t{stat_hash=}, value={stats[str(stat_hash)]['value']}")
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
                print(new_sales_item)

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
                    sales_date = today
                sales_date = sales_date.replace(hour=17, minute=0, second=0, microsecond=0)  # pst 9 = utc 17 = kst 26
                new_sales_item.sales_date = sales_date

                new_sales_item.save()

    return JsonResponse(stats_data)
