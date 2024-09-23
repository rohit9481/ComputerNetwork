import socket
import threading
import pickle

# Sample data for provider login credentials
provider_credentials = {
    "Rohan": "password123",
    "Arjun": "password123",
    "Raju": "password123",
    "Manish": "password123",
    "Kiran": "password123",
    "Suresh": "password123",
    "Rahul": "password123",
    "Amit": "password123",
    "Deepak": "password123",
    "Naveen": "password123",
    "Praveen": "password123",
    "Raj": "password123",
    "Vijay": "password123",
    "Mukesh": "password123",
    "Ramesh": "password123",
    "Ashok": "password123",
    "Harish": "password123",
    "Kumar": "password123",
    "Santosh": "password123",
    "Gopal": "password123",
    "Rajesh": "password123",
    "Vikram": "password123",
    "Anil": "password123",
    "Sanjay": "password123",
    "Shyam": "password123",
    "Nikhil": "password123",
    "Lokesh": "password123",
    "Aravind": "password123",
    "Suraj": "password123",
    "Mahesh": "password123",
    "Siddharth": "password123",
    "Vishal": "password123",
    "Vikas": "password123",
    "Karthik": "password123",
    "Rakesh": "password123",
    "Ajit": "password123",
    "Nitesh": "password123",
    "Ajay": "password123",
    "Sunil": "password123",
    "Karan": "password123",
    "Prakash": "password123",
    "Raghav": "password123",
    "Mohan": "password123",
    "Anil": "password123",
    "Rajesh": "password123",
    "Nilesh": "password123",
    "Vivek": "password123",
    "Anand": "password123",
    "Rahul": "password123",
    "Nitin": "password123"
}

client_requests = {}

def handle_client_connection(client_socket, address):
    print(f"Client {address} connected.")
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            message = pickle.loads(data)
            if message["type"] == "request":
                service_request = message["data"]
                provider = service_request["provider"]
                client_id = service_request["client_id"]
                print(f"Request from Client {client_id} for {provider}: {service_request}")

                if provider not in client_requests:
                    client_requests[provider] = []

                client_requests[provider].append((client_id, service_request))
                response = f"Request sent to provider {provider}."
                client_socket.send(pickle.dumps(response))

            elif message["type"] == "login":
                login_data = message["data"]
                provider_name = login_data["provider"]
                password = login_data["password"]

                if provider_name in provider_credentials and provider_credentials[provider_name] == password:
                    response = {"status": "success", "message": f"Welcome, {provider_name}!"}
                    client_socket.send(pickle.dumps(response))

                    threading.Thread(target=handle_provider_requests, args=(client_socket, provider_name)).start()
                else:
                    response = {"status": "failure", "message": "Invalid credentials."}
                    client_socket.send(pickle.dumps(response))

            elif message["type"] == "response":
                response_data = message["data"]
                request_info = response_data["request_info"]
                status = response_data["status"]
                print(f"Provider response: {status} - {request_info}")
                # Process provider response (e.g., send to client)
                # In a real application, we would locate the client socket and send the response

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        print(f"Client {address} disconnected.")

def handle_provider_requests(provider_socket, provider_name):
    try:
        while True:
            if provider_name in client_requests and client_requests[provider_name]:
                client_id, service_request = client_requests[provider_name].pop(0)
                provider_socket.send(pickle.dumps(service_request))
    except Exception as e:
        print(f"Error handling provider {provider_name}: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server listening on port 12345")

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client_connection, args=(client_socket, address)).start()

if __name__ == "__main__":
    main()
