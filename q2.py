
# just make the worker things as functions?

import socket
import pickle
import threading
import marshal
import types
import time
import multiprocessing


def run_worker():
    print ("connecting")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12345) 
        client_socket.connect(server_address)
        work, args = marshal.loads(client_socket.recv(1024))
        workFunction = types.FunctionType(work, globals(), "function")
        #args = marshal.loads(client_socket.recv(1024))
        res = workFunction (*args)
        client_socket.send(pickle.dumps(res))
    except FileNotFoundError:
        print ("file not found")
    except OSError:
        print ("networking or file reading error")
    finally:
        # Clean up connection
        client_socket.close()

if __name__ == "__main__":
    processes = []
    for i in range(10): # number of workers
        process = multiprocessing.Process(target=run_worker)
        process.start()
        processes.append(process)
        time.sleep(1)
    for process in processes:
        process.join()