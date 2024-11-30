import re
from ppadb.client import Client as AdbClient
from ssh_launch import remote_command

# ADB Server configurations
host = "127.0.0.1"
port = 5037

device_list = []

client = AdbClient(host=host, port=port)
devices = client.devices()

for device in devices: 
    try: 
        device_ip_address = re.findall('src.(\d+.\d+.\d+.\d+)',device.shell("ip route"))
        device_product_model = device.shell("getprop ro.product.model")
        device_list.append({"model":device_product_model, "ip_address": device_ip_address[0], "device_object":device})
        print('Next device!')
    except Exception as e:
        print(f"Error: {e}")

for device in device_list:
    try:
        print("Connecting to:  ", device["ip_address"])
        check_process = remote_command(device["ip_address"], 2022, "chance", "chance", "pidof ccminer")
    except:
        print("Connection did not went well!")
        check_process = [""]

    if check_process[0] != "":
        print("Miner software is running! Nothing to do here!")
    else:
        print("Service has to be started!")
        try:
            check_process = remote_command(device["ip_address"], 2022, "chance", "chance", "/home/chance/ccminer/start.sh")
            print("Service started!")
        except:
            print("Did not manage to launch Miner!")