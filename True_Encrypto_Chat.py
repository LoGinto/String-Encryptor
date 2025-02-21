import socket
import threading
import rsa

# Generate RSA keys
public_key, private_key = rsa.newkeys(512)
peer_public_key = None

# Get local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unknown"

local_ip = get_local_ip()
# Function to handle incoming connections
def server_mode(port):
    global peer_public_key

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    print(f"Waiting for connection on port {port}...")

    while True:
        conn, addr = server.accept()
        print(f"\nIncoming connection request from {addr[0]}")

        accept = input("Accept connection? (y/n): ").strip().lower()
        if accept != "y":
            conn.close()
            continue

        print(" Exchanging public keys...")
        conn.send(public_key.save_pkcs1())  # Send own public key
        peer_public_key = rsa.PublicKey.load_pkcs1(conn.recv(1024))  # Receive peer's public key

        print("Secure connection established! You can now chat.")

        # Start listening for messages
        threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

# Function to receive messages
def receive_messages(conn):
    global private_key
    while True:
        try:
            encrypted_message = conn.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
            print(f"\n Message: {decrypted_message}")
        except Exception:
            print("Connection closed by peer.")
            break
    conn.close()

# Function to connect to a peer
def client_mode(target_ip, target_port):
    global peer_public_key

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_ip, target_port))

    print(" Exchanging public keys...")
    peer_public_key = rsa.PublicKey.load_pkcs1(client.recv(1024))  # Receive peer's public key
    client.send(public_key.save_pkcs1())  # Send own public key

    print(" Secure connection established! You can now chat.")

    # Start listening for messages
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break
        encrypted_message = rsa.encrypt(message.encode(), peer_public_key)
        client.send(encrypted_message)

    client.close()

# Start server mode in the background
port = int(input("Enter your listening port: "))
threading.Thread(target=server_mode, args=(port,), daemon=True).start()

# Ask user if they want to connect to someone
while True:
    choice = input("\nDo you want to connect to someone? (y/n): ").strip().lower()
    if choice == "y":
        target_ip = input("Enter peer's IP: ")
        target_port = int(input("Enter peer's port: "))
        client_mode(target_ip, target_port)
    elif choice == "n":
        print("Waiting for incoming connections...")
    else:
        print("Invalid choice. Enter 'y' or 'n'.")
