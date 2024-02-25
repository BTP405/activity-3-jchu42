import socket
import pickle
import threading
import time
import marshal

connectedLock = threading.Lock()
connected = 0
finishedLock = threading.Lock()
finished = 0

workersRequired = 10

def work(num):
    time.sleep(1)
    print (num) # printed at worker side
    time.sleep(1)
    return num**5 # large value is returned to client where it is then printed

def handle_worker():
    global finished
    global connected
    cnt = connected + finished
    with connectedLock:
        connected += 1
    print ("Waiting for connection")
    worker_socket, worker_address = server_socket.accept()

    try:
        print("Connection to:", worker_address)

        worker_socket.send(marshal.dumps((work.__code__, (cnt,))))
        #worker_socket.send(marshal.dumps((connected,))) # tuple
        print ("data sent to", worker_address)
        res = worker_socket.recv(1024)
        #print (res)
        res = pickle.loads(res)
        print (res)
        with finishedLock:
            finished += 1
    #except pickle.PickleError:
    #    print ("unpicklable")
    except ValueError:
        print ("couldn't marshal object/function")
    except EOFError:
        print ("error receiving")
    except TimeoutError:
        print ("connection timed out")
    except OSError:
        print ("networking or file error")
    finally:
        worker_socket.close()
    with connectedLock:
        connected -= 1

def run_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(workersRequired) # max number of clients
    threads = []
    while finished != workersRequired: # wait for completion
        if (connected + finished < workersRequired): # constant check for dropped connections
            thread = threading.Thread (target=handle_worker)            
            thread.start()
            threads.append(thread)
        time.sleep(1)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run_server()