import ssh2.session
import socket

# Define server details
hostname = "192.168.8.37"
port = 2022
username = 'chance'
password = 'chance'
command = '/home/chance/ccminer/start.sh'

def remote_command(hostname, port, username, password, command):
    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    # Create a session
    session = ssh2.session.Session()
    session.set_timeout(10000)
    session.handshake(sock)

    # Authenticate with username and password
    session.userauth_password(username, password)

    # Open a channel and execute the command
    channel = session.open_session()
    channel.execute(command)

    # Read and print the command output
    size, data = channel.read()
    output = ""
    while size > 0:
        #print(data.decode())
        output = output + " " + data.decode()
        size, data = channel.read()
    # Close the channel and session
    channel.close()
    session.disconnect()
    sock.close()
    return output, size, data

if __name__ == "__main__":
    output = remote_command(hostname, port, username, password, "pidof ccminer")
    print(output[0].strip())
    print(type(output[0]))