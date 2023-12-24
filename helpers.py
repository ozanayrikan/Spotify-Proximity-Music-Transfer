import random
import string
import requests
import json


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def authorize(client_id, redirect_uri, client_secret, code):
    token_url = 'https://accounts.spotify.com/api/token'

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        print('Authorize Successful! Token found.')
        token_data = response.json()
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        return access_token, refresh_token
    else:
        print('Authorize Error Code:', response.status_code)
        print('Authorize Error message:', response.text)
        return None, None


def get_devices(base_url, access_token):
    token_url = base_url + 'me/player/devices'
    header = {
        'Authorization': 'Bearer ' + access_token,
    }
    response = requests.get(token_url, headers=header)

    if response.status_code == 200:
        response = response.json()
        return response['devices']

    else:
        print('Get Devices Error Code:', response.status_code)
        print('Get Devices Error message:', response.text)


CURRENT_ID = None


def playback_transfer_to(base_url, access_token, id):
    global CURRENT_ID
    if CURRENT_ID == id:
        return False

    token_url = base_url + 'me/player'
    header = {
        'Authorization': 'Bearer ' + access_token,
    }
    payload = json.dumps({
        'device_ids': [id],
        'play': True
    })
    response = requests.put(token_url, data=payload, headers=header)

    if response.status_code == 204 or response.status_code == 404:
        CURRENT_ID = id
