import asyncio
from bleak import BleakScanner
from dotenv import load_dotenv
import os

load_dotenv()

TARGET_DEVICE_BLUETOOTH_ADDRESS = os.getenv('TARGET_DEVICE_BLUETOOTH_ADDRESS')
SCAN_INTERVAL = os.getenv('SCAN_INTERVAL')


async def scan_for_devices():
    devices = await BleakScanner.discover(timeout=int(SCAN_INTERVAL))
    for d in devices:
        if d.address == TARGET_DEVICE_BLUETOOTH_ADDRESS:
            return d.rssi
    return None
