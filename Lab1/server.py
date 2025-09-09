import socket

def start_server(host='0.0.0.0', port=5001):
    server = "Server for Utkarsh"  
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(1)
    print(f"Server started at {host}:{port}")

    while True:
        conn, addr = socket.accept()
        print(f"Connection from {addr}")

        data = conn.recv(1024).decode()
        if not data:
            break
        
        client, clientNo = data.split(',')
        clientNo = int(clientNo)
        
        print(f"Client Name: {client}")
        print(f"Client Number: {clientNo}")
      
        if clientNo < 1 or clientNo > 100:
            print("Number out of range. Closing server.")
            conn.close()
            break
        
        serverNo = 42  
        total_sum = clientNo + serverNo
        
        print(f"Server Name: {server}")
        print(f"Server Number: {serverNo}")
        print(f"Sum: {total_sum}")
        conn.send(f"{server},{serverNo}".encode())
        conn.close()

    socket.close()

if __name__ == "__main__":
    start_server()
