import urllib.parse
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import RedirectResponse
from bleak_bluetooth import scan_for_devices
from helpers import generate_random_string, authorize, get_devices, playback_transfer_to
import asyncio
from dotenv import load_dotenv
import os
import time

app = FastAPI()

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
base_url = os.getenv('BASE_URL')

current_devices = {
    'Smartphone': None,
    'Laptop': None
}
tokens = {
    'access_token': None,
    'refresh_token': None
}


@app.get('/')
async def login():
    scope = 'user-read-private user-read-email user-modify-playback-state user-read-playback-state app-remote-control' \
            ' streaming user-read-currently-playing'
    state = generate_random_string(16)

    payload = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }

    spotify_auth_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(payload)
    return RedirectResponse(url=spotify_auth_url)


@app.get('/callback')
async def callback(code: str, state: str):
    tokens['access_token'], tokens['refresh_token'] = authorize(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        code=code
    )
    while not current_devices['Smartphone'] and not current_devices['Laptop']:
        devices = get_devices(base_url=base_url, access_token=tokens['access_token'])
        print('Waiting for Laptop and Smartphone to connect to Spotify.')
        for device in devices:
            id = device.get('id')
            type = device.get('type')

            if type == 'Laptop':
                current_devices['Laptop'] = id
            elif type == 'Smartphone':
                current_devices['Smartphone'] = id
        time.sleep(5)

    return RedirectResponse(url='/home')


RSSI_VALUES = []

consecutive_fail_count = 1
max_fails_before_action = 2


async def update():
    global consecutive_fail_count
    global max_fails_before_action

    rssi = await scan_for_devices()

    if not rssi:
        consecutive_fail_count += 1
        if len(RSSI_VALUES) > 0 and consecutive_fail_count >= max_fails_before_action:
            playback_transfer_to(base_url=base_url, access_token=tokens['access_token'],
                                 id=current_devices['Smartphone'])
            consecutive_fail_count = 0
            print('RSSI has gone too far, being transmitted to the phone.')
        else:
            playback_transfer_to(base_url=base_url, access_token=tokens['access_token'], id=current_devices['Laptop'])
            consecutive_fail_count = 0
            print('RSSI never happened, it is transferred to the laptop.')
        return True

    RSSI_VALUES.append(int(rssi))

    if len(RSSI_VALUES) >= 2:
        last_four_rssi = RSSI_VALUES[-2:]
        print(last_four_rssi)
        if all(last_four_rssi[i] < -80 for i in range(1)):
            playback_transfer_to(base_url=base_url, access_token=tokens['access_token'],
                                 id=current_devices['Smartphone'])
            print('The last four RSSIs transferred to the phone:', last_four_rssi)
        else:
            playback_transfer_to(base_url=base_url, access_token=tokens['access_token'], id=current_devices['Laptop'])
            print('Transferred to laptop, last four RSSI:', last_four_rssi)

    else:
        print('Not enough RSSI values, total:', len(RSSI_VALUES))

    return True


async def run_infinite_loop():
    while True:
        await update()
        await asyncio.sleep(1)  # Non-blocking wait


@app.get("/home")
async def home(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_infinite_loop)
    return 'Success!'
