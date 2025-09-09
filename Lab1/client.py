import socket

def start_client(host='127.0.0.1', port=5001):
    client = "Client of Utkarsh"  
    clientNo = int(input("Enter an integer between 1 and 100: "))

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((host, port))

    socket.send(f"{client},{clientNo}".encode())

    data = socket.recv(1024).decode()
    server, serverNo = data.split(',')
    serverNo = int(serverNo)

    
    print(f"Client Name: {client}")
    print(f"Client Number: {clientNo}")
    print(f"Server Name: {server}")
    print(f"Server Number: {serverNo}")
    print(f"Sum: {clientNo + serverNo}")
    
    socket.close()

if __name__ == "__main__":
    start_client()
