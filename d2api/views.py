import json
import pprint

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session, TokenUpdated


API_KEY = settings.API_KEY
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

TITAN_ID = settings.TITAN_ID
HUNTER_ID = settings.HUNTER_ID
WARLOCK_ID = settings.WARLOCK_ID
DESTINY_MEMBERSHIP_ID = settings.DESTINY_MEMBERSHIP_ID
MEMBERSHIP_TYPE = settings.MEMBERSHIP_TYPE

REDIRECT_URI = "https://127.0.0.1:8000/"
AUTHORIZATION_URL = "https://www.bungie.net/en/oauth/authorize"
TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"
BASE_PATH = "https://www.bungie.net/Platform"


def get_auth(request):
    oauth = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url(url=AUTHORIZATION_URL)
    request.session['oauth_state'] = state

    return JsonResponse({'authorization_url': authorization_url})


def fetch_token(request):
    data = json.loads(request.body)

    oauth = OAuth2Session(client_id=CLIENT_ID, state=request.session['oauth_state'])
    token = oauth.fetch_token(token_url=TOKEN_URL, authorization_response=REDIRECT_URI+data['auth_res'], client_secret=CLIENT_SECRET)

    request.session['oauth_token'] = token

    return JsonResponse(token)


def refresh_token(request):
    return JsonResponse({'key': 'value'})


def request_data(request):
    characterId = TITAN_ID
    destinyMembershipId = DESTINY_MEMBERSHIP_ID
    membershipType = MEMBERSHIP_TYPE
    # vendorHash = 69482069  # Commander Zavala
    # vendorHash = 248695599  # The Drifter
    # vendorHash = 3603221665  # Lord Shaxx
    vendor_hash_list = [69482069, 248695599, 3603221665]
    components = "402,304"  # ItemStats

    extra = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    headers = {"X-API-Key": API_KEY}
    endpoint_url = f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/?components={components}"
    try:
        oauth = OAuth2Session(client_id=CLIENT_ID, token=request.session['oauth_token'], auto_refresh_url=TOKEN_URL, auto_refresh_kwargs=extra)
        response = oauth.get(url=endpoint_url, headers=headers)
    except TokenUpdated as e:
        print("====================Updated====================")
        request.session['oauth_token'] = e.token
        response = oauth.get(url=endpoint_url, headers=headers)

    print(response.status_code)
    result = response.json()['Response']['itemComponents']

    for vendor_hash in vendor_hash_list:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(result[str(vendor_hash)]['stats']['data'])

    return JsonResponse(result)
