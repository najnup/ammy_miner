import requests
import time
import json
from ppadb.client import Client as AdbClient

"""
TODO Start and stop miner application on the phones
TODO Have Battery checks for all connected phones
"""

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)

# Listing all connected devices
devices = client.devices()

