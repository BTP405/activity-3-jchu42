import socket
import pickle

    


def run_client():
        # Send message to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12345) # Replace 'localhost' with your server's IP address
        client_socket.connect(server_address)
        #file = open(input("specify source file: "), "rb")
        with open(input("specify source file: "), "rb") as file:
            client_socket.send(file.read())
            print ("file sent.")
    except FileNotFoundError:
        print ("file not found")
    except OSError:
        print ("networking or file reading error")
    finally:
        # Clean up connection
        client_socket.close()

if __name__ == "__main__":
    a = {'hello': 'world'}
    # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict-or-any-other-python-object
    with open("file.pkl", "wb") as file:
        pickle.dump(a, file)
    run_client()