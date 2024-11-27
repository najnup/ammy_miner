import socket

# Define the server address and port
server_address = '192.168.8.30'
server_port = 4068

class miner_monitoring():
    def __init__(self, ip_address, port):
        self.port = port
        self.ip_address = ip_address
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect the socket to the server
            self.sock.connect((self.ip_address, self.port))
            print(f"Connected to the server at {self.ip_address}:{self.port}")
        except socket.error as e:
            print(f"Failed to create socket: {e}")
    
    def __del__(self):
        # Close the socket
        self.sock.close()
    
    def send_command(self, command):
        # Send Command to miner
        # Commands: summary, threads, pool, histo, hwinfo, meminfo, scanlog, seturl, switchpool, quit
        try:
            # Sending command
            self.sock.sendall(command.encode('utf-8')) 
            response = self.sock.recv(1024).decode('utf-8')
            return response
        except: 
            print("Something went wrong!")

if __name__ == "__main__":
    monitor = miner_monitoring(server_address, server_port)
    response = monitor.send_command('quit')
    print(response)