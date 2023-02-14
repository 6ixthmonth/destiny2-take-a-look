import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session


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
GET_VENDORS_URL = r"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/"
GET_VENDOR_URL = r"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/"


def get_auth(request):
    auth_session = OAuth2Session(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI
    )
    auth_response = auth_session.authorization_url(AUTHORIZATION_URL)
    # print(f"auth response URL: {auth_response[0]}")
    # print(f"auth response state: {auth_response[1]}")

    return JsonResponse({'auth_response_url': auth_response[0]})


def refresh_token(request):
    return JsonResponse({'key': 'value'})


def request_data(request):
    data = json.loads(request.body)
    print(data)

    print(REDIRECT_URI + data['auth_res'])

    characterId = TITAN_ID
    destinyMembershipId = DESTINY_MEMBERSHIP_ID
    membershipType = MEMBERSHIP_TYPE
    vendorHash = 69482069  # <Vendor "Commander Zavala">
    components = "400"

    # getVendors
    # endpoint_url = f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/?components={components}"
    # getVendor
    endpoint_url = f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/?components={components}"

    auth_session = OAuth2Session(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI
    )
    auth_session.fetch_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                             token_url=TOKEN_URL, authorization_response=REDIRECT_URI+data['auth_res'])

    headers = {"X-API-Key": API_KEY}
    response = auth_session.get(url=endpoint_url, headers=headers)

    print(response.status_code)
    # print(response.text)
    # print(response.content)
    print(json.loads(response.content))

    return JsonResponse({'key': 'value'})
