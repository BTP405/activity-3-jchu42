import socket
import pickle
import threading
import time


closeChatroom = False
server_socket = None
allClientSockets = []
socketsLock = threading.Lock()

def handle_client(client_socket, client_address):
    global closeChatroom

    with socketsLock:
        allClientSockets.append(client_socket)

    try:
        print("Connection to:", client_address)
        while not closeChatroom:
            msg = pickle.loads(client_socket.recv(1024))
            print ("broadcasting message:", msg)
            with socketsLock:
                for skt in allClientSockets:
                    if skt is not client_socket:
                        skt.send(msg.encode()) # regular message
            if (msg == "exit"):
                print ("exiting")
                closeChatroom = True
                server_socket.close() # ??
    except pickle.PickleError:
        print ("unpicklable")
    except EOFError:
        print ("error receiving")
    except TimeoutError:
        print ("connection timed out")
    except OSError:
        print ("networking or file error")
    finally:
        client_socket.close()
    with socketsLock:
        allClientSockets.remove(client_socket)

def run_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(50) # max number of clients
    threads = []
    try:
        while not closeChatroom: 
            print ("Waiting for connection")
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread (target=handle_client, args=(client_socket, client_address))            
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    except OSError:
        print ("probably server has been closed with 'exit' command")
    except Exception:
        server_socket.close()

if __name__ == "__main__":
    run_server()