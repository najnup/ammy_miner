import requests
import re
import time
import json
from time import sleep
from monitoring import miner_monitoring
from ppadb.client import Client as AdbClient
from ssh_launch import remote_command

# Default is "127.0.0.1" and 5037

### TODO Launch UserLand automatically 

host = "127.0.0.1"
port = 5037

if __name__ == "__main__":
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host=host, port=port)

    while True:
        device_list = []
        # Listing all concted devices
        devices = client.devices()
        
        # Apend devices data
        for device in devices: 
            try: 
                device_product_model = device.shell("getprop ro.product.model")
                device_build_release = device.shell("getprop ro.build.version.release")
                device_ip_address = re.findall('src.(\d+.\d+.\d+.\d+)',device.shell("ip route"))
                device_battery_level = re.findall('level: (\d+)', device.shell("dumpsys battery"))
                device_list.append({"model":device_product_model, "release_version":device_build_release, "ip_address": device_ip_address[0], "battery_level": device_battery_level[0], "device_object":device})
                print('Next device!')
            except:
                print("Failed to read from device!")

        for device in device_list:
            print(device["model"], device["ip_address"], device["battery_level"])
            
            # Stopping the miner
            if int(device["battery_level"]) < 20:
                miner = miner_monitoring(device["ip_address"], 4068)
                miner.send_command('quit')
                print("Miner Stopped!")
            
            # Starting miner
            elif int(device["battery_level"]) > 80:
                print("Have to start the app")
                try:
                    check_process = remote_command(device["ip_address"], 2022, "chance", "chance", "pidof ccminer")
                except:
                    print("Connection did not went well!")
                #if check_process != null:
                if check_process[0] != "":
                    print("Miner software is running! Nothing to do here!")
                else:
                    print("Service has to be started!")
                    try:
                        check_process = remote_command(device["ip_address"], 2022, "chance", "chance", "/home/chance/ccminer/start.sh")
                        print("Service started!")
                    except:
                        print("Something went off with starting Miner software.")
            else:
                print("No need to stop anything!")

        # Starting of the service

        # Wait for the next round
        sleep(300)
"""
Get info about device
Monitor the level for battery
if it drops below 15 stop CC miner
"""