
# just make the worker things as functions?

import socket
import pickle
import sys
import threading
import marshal
import types
import time


def senderLoop(client_socket, connected):
    try:
        while connected[0]:
            print ("Enter message:", end='')
            msg = input()
            client_socket.send(pickle.dumps(msg)) # ezpz
            if (msg == "exit"):
                connected[0] = False
                client_socket.close()
    except OSError:
        print ("socket was closed")

def run_client():
    print ("connecting")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12345) 
        client_socket.connect(server_address)

        connected = [True]
        thread = threading.Thread(target=senderLoop, args=(client_socket, connected))
        thread.start()

        while connected[0]:
            msg = client_socket.recv(1024).decode()
            #print ("\033[A                             \033[A") # delete last line? https://stackoverflow.com/questions/44565704/how-to-clear-only-last-one-line-in-python-output-console
            
            #sys.stdout.write("\033[F\033[K")
            print ("\r                                                  ", end='')
            print ("\r" + msg)
            if (msg == "exit"):
                connected[0] = False
                client_socket.close()
            print ("Enter message:", end='')
            sys.stdout.flush() # https://stackoverflow.com/questions/35230959/printfoo-end-not-working-in-terminal
    except FileNotFoundError:
        print ("file not found")
    except OSError:
        print ("networking or file reading error")
    finally:
        # Clean up connection
        client_socket.close()
    if (thread):
        thread.join()

if __name__ == "__main__":
    run_client()