from ppadb.client import Client as AdbClient

# Default ADB server is "127.0.0.1" and 5037
host = "127.0.0.1"
port = 5037



client = AdbClient(host=host, port=port)
devices = client.devices()



if __name__ == "__main__":
    pass