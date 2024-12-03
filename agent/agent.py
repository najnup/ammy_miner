import re
import time
import json
import logging
from time import sleep
from monitoring import miner_monitoring
from ppadb.client import Client as AdbClient
from ssh_launch import remote_command

# Logging definition
logging.basicConfig(filename='/home/pi/ammy_miner/agent/myminer.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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
                device_product_model = device.shell("getprop ro.product.model").strip()
                device_build_release = device.shell("getprop ro.build.version.release")
                device_ip_address = re.findall('src.(\d+.\d+.\d+.\d+)',device.shell("ip route"))
                device_battery_level = re.findall('level: (\d+)', device.shell("dumpsys battery"))
                device_list.append({"model":device_product_model, "release_version":device_build_release, "ip_address": device_ip_address[0], "battery_level": device_battery_level[0], "device_object":device})
                logging.info('Next device!')
            except Exception as e:
                logging.error(e)

        for device in device_list:
            logging.info(device["model"], device["ip_address"], device["battery_level"])
            
            # Stopping the miner
            if int(device["battery_level"]) < 20:
                logging.info("Battery below 20%")
                miner = miner_monitoring(device["ip_address"], 4068)
                miner.send_command('quit')
                logging.info("Miner Stopped!")
            
            # Starting miner
            elif int(device["battery_level"]) > 80:
                logging.info("Battery above 80%")
                try:
                    check_process = remote_command(device["ip_address"], 2022, "chance", "chance", "pidof ccminer")
                except:
                    logging.warning("Connection did not went well!")
                    check_process = [""]

                if check_process[0] != "":
                    logging.info("Miner software is running! Nothing to do here!")
                else:
                    logging.info("Service has to be started!")
                    try:
                        check_process = remote_command(device["ip_address"], 2022, "chance", "chance", "/home/chance/ccminer/start.sh")
                        logging.info("Service started!")
                    except:
                        logging.warning("Something went off with starting Miner software.")
            else:
                logging.info("No need to stop anything!")

        # Starting of the service

        # Wait for the next round
        sleep(300)
