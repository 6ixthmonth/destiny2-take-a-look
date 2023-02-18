import json
import pprint

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session, TokenUpdated

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
    69482069,  # Commander Zavala
    # 248695599,  # The Drifter
    # 3603221665,  # Lord Shaxx
]
VENDOR_ITEM_INDEX_LIST = [
    [
        [110, 111, 112, 113, 114],
        # [50, 51, 52, 53],
        # [135, 136, 137, 138],
    ],  # Titan
    [
        [105, 106, 107, 108, 109],
        # [42, 43, 44, 45],
        # [139, 140, 141, 142],
    ],  # Hunter
    [
        [115, 116, 117, 118, 119],
        # [46, 47, 48, 49],
        # [131, 132, 133, 134],
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


def refresh_token(request):
    return JsonResponse({'key': 'value'})


def request_data(request):
    # repeat for the number of characters
    for i in range(len(CHARACTER_ID_LIST)):
        membershipType = MEMBERSHIP_TYPE
        destinyMembershipId = DESTINY_MEMBERSHIP_ID
        characterId = CHARACTER_ID_LIST[i]
        components = COMPONENTS
        print(f"{characterId=}")

        for j in range(len(VENDOR_HASH_LIST)):
            vendorHash = VENDOR_HASH_LIST[j]
            endpoint_url = f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/?components={components}"
            headers = {"X-API-Key": API_KEY}
            try:
                oauth = OAuth2Session(client_id=EXTRA['client_id'], auto_refresh_url=TOKEN_URL, auto_refresh_kwargs=EXTRA, token=request.session['oauth_token'])
                response = oauth.get(url=endpoint_url, headers=headers)
            except TokenUpdated as e:
                print("==========Token has been updated==========")
                print(e.token)
                request.session['oauth_token'] = e.token
                response = oauth.get(url=endpoint_url, headers=headers)
            data = response.json()['Response']['itemComponents']['stats']['data']

            for vendor_item_index in VENDOR_ITEM_INDEX_LIST[i][j]:
                print(f"\t{vendor_item_index=}")
                stats = data[str(vendor_item_index)]['stats']
                for stat_hash in STAT_HASH_LIST:
                    print(f"\t\t{stat_hash=}, value={stats[str(stat_hash)]['value']}")

    return JsonResponse(data)
