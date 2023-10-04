# import socket module
from socket import *
import sys  # In order to terminate the program


def webServer(port=80):
    serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a server socket

    serverSocket.bind(('', port))
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print(f'Ready to serve on port {port}...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024)
            filename = message.split()[1]

            with open(filename[1:], 'r') as f:
                outputdata = f.read()
                f.close()
                # Send one HTTP header line into socket
                outputdata = f'HTTP/1.1 200 OK\r\n\r\n{outputdata}'

                # Send the content of the requested file to the client
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
            connectionSocket.close()
        except IOError:
            # Send response message for file not found
            error = 'HTTP/1.1 404 Not Found\r\n\r\n'
            print(f'error: {error}')

            # Close client socket
            for i in range (0, len(error)):
                connectionSocket.send(error[i].encode())
            connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    try:
        port = input("Input desired port or press 'Enter' to initiate the server...")
        if port == '':
            # port 80
            webServer()
        elif 0 <= int(port) <= 65535:
            webServer(port)
        else:
            print("Invalid input. Port must be an integer between 0 and 65535.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
