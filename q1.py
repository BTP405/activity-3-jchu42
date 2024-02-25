import socket
import pickle

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345) # Replace 'localhost' with your IP address
    server_socket.bind(server_address)
    server_socket.listen(1) # max number of clients

        # Wait for connection
    print ("Waiting for connection")
    client_socket, client_address = server_socket.accept()

    try:
        print("Connection to:", client_address)

        # Receive data from client
        data = client_socket.recv(1024) #size of message to receive; 1024 is maximum
        print ("data received:", data)
        print ("unpickled: ", pickle.loads(data))
        with open(input("specify location to write to: "), "wb") as file:
            pickle.dump (data, file)
            print ("data saved")
    except pickle.PickleError:
        print ("unpicklable")
    except TimeoutError:
        print ("connection timed out")
    except OSError:
        print ("networking or file error")
    finally:
        # Clean up connection
        client_socket.close()


if __name__ == "__main__":
    run_server()