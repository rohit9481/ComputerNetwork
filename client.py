import tkinter as tk
from tkinter import ttk, messagebox
import socket
import pickle
import threading

# Sample data for services, locations, and providers
professional_groups = {
    "Carpenter": {
        "Vijay Nagar": ["Rohan", "Arjun", "Raju", "Manish", "Kiran"],
        "Electronic City": ["Suresh", "Rahul", "Amit", "Deepak", "Naveen"],
        "Koramangala": ["Praveen", "Raj", "Vijay", "Mukesh", "Ramesh"],
        "Whitefield": ["Ashok", "Harish", "Kumar", "Santosh", "Gopal"]
    },
    "Plumber": {
        "Jayanagar": ["Ravi", "Rajesh", "Vikram", "Anil", "Sanjay"],
        "Rajaji Nagar": ["Shyam", "Nikhil", "Lokesh", "Aravind", "Suraj"],
        "Indiranagar": ["Gopal", "Mahesh", "Siddharth", "Naveen", "Vishal"],
        "Marathahalli": ["Ramesh", "Vikas", "Amit", "Karthik", "Ravi"]
    },
    "Painter": {
        "HSR Layout": ["Manoj", "Rakesh", "Suresh", "Ajit", "Nitesh"],
        "Vijay Nagar": ["Ajay", "Vijay", "Sunil", "Karan", "Prakash"],
        "Bellandur": ["Ravi", "Manish", "Harish", "Kumar", "Ashok"],
        "BTM Layout": ["Santosh", "Deepak", "Raghav", "Mohan", "Ajay"]
    },
    "Driver": {
        "BTM Layout": ["Karthik", "Anil", "Ravi", "Suresh", "Manoj"],
        "Koramangala": ["Deepak", "Ramesh", "Santosh", "Ajay", "Vikram"],
        "MG Road": ["Arjun", "Prakash", "Ravi", "Naveen", "Kiran"],
        "Indiranagar": ["Sunil", "Rajesh", "Karthik", "Vikas", "Nilesh"]
    },
    "Electrician": {
        "Indiranagar": ["Sunil", "Vikram", "Kiran", "Ravi", "Manish"],
        "Marathahalli": ["Vivek", "Anand", "Rajesh", "Ramesh", "Naveen"],
        "Koramangala": ["Ajay", "Karthik", "Suresh", "Rahul", "Deepak"],
        "Whitefield": ["Vikram", "Raj", "Harish", "Prakash", "Nitin"]
    }
}

class ClientProviderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client-Provider App")
        self.geometry("500x600")

        self.role = None  # Client or Provider
        self.service_var = tk.StringVar(self)
        self.location_var = tk.StringVar(self)
        self.provider_var = tk.StringVar(self)

        self.create_role_selection()

    def create_role_selection(self):
        self.clear_widgets()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(pady=50)
        
        tk.Label(frame, text="Select Role:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=10)
        role_combobox = ttk.Combobox(frame, values=["Client", "Provider"], state="readonly", font=("Helvetica", 12))
        role_combobox.grid(row=0, column=1, padx=10, pady=10)
        role_combobox.bind("<<ComboboxSelected>>", self.select_role)

    def select_role(self, event):
        self.role = self.nametowidget(".!frame.!combobox").get()

        if self.role == "Client":
            self.create_client_ui()
        elif self.role == "Provider":
            self.create_login_ui()

    def create_login_ui(self):
        self.clear_widgets()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(pady=50)

        tk.Label(frame, text="Provider Login", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(frame, text="Provider Name:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.provider_name_entry = tk.Entry(frame, font=("Helvetica", 12))
        self.provider_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        login_button = tk.Button(frame, text="Login", command=self.login_provider, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
        login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def login_provider(self):
        provider_name = self.provider_name_entry.get()
        password = self.password_entry.get()

        login_data = {
            "type": "login",
            "data": {
                "provider": provider_name,
                "password": password
            }
        }

        try:
            self.provider_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.provider_socket.connect(('127.0.0.1', 12345))
            self.provider_socket.send(pickle.dumps(login_data))
            response = self.provider_socket.recv(4096)
            response_message = pickle.loads(response)

            if response_message["status"] == "success":
                messagebox.showinfo("Login Successful", response_message["message"])
                self.create_provider_ui()
                threading.Thread(target=self.receive_requests).start()
            else:
                messagebox.showerror("Login Failed", response_message["message"])
        except Exception as e:
            messagebox.showerror("Error", f"Error logging in: {e}")

    def create_client_ui(self):
        self.clear_widgets()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(pady=50)

        tk.Label(frame, text="Select Service:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)
        service_combobox = ttk.Combobox(frame, textvariable=self.service_var, values=list(professional_groups.keys()), font=("Helvetica", 12))
        service_combobox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Select Location:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.location_combobox = ttk.Combobox(frame, textvariable=self.location_var, values=[], font=("Helvetica", 12))
        self.location_combobox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(frame, text="Select Provider:", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10)
        self.provider_combobox = ttk.Combobox(frame, textvariable=self.provider_var, values=[], font=("Helvetica", 12))
        self.provider_combobox.grid(row=3, column=1, padx=10, pady=10)

        request_button = tk.Button(frame, text="Send Request", command=self.send_request, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
        request_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.response_label = tk.Label(frame, text="", font=("Helvetica", 12))
        self.response_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        service_combobox.bind("<<ComboboxSelected>>", self.update_locations)
        self.location_combobox.bind("<<ComboboxSelected>>", self.update_providers)

    def create_provider_ui(self):
        self.clear_widgets()
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(pady=50)

        tk.Label(frame, text="Provider Interface", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.requests_listbox = tk.Listbox(frame, font=("Helvetica", 12))
        self.requests_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        accept_button = tk.Button(frame, text="Accept Request", command=self.accept_request, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
        accept_button.grid(row=2, column=0, padx=10, pady=10)

        reject_button = tk.Button(frame, text="Reject Request", command=self.reject_request, font=("Helvetica", 12, "bold"), bg="#F44336", fg="white")
        reject_button.grid(row=2, column=1, padx=10, pady=10)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update_locations(self, event):
        selected_service = self.service_var.get()
        if selected_service in professional_groups:
            locations = list(professional_groups[selected_service].keys())
            self.location_var.set("")  # Clear previous selection
            self.location_combobox["values"] = locations

    def update_providers(self, event):
        selected_service = self.service_var.get()
        selected_location = self.location_var.get()
        if selected_service in professional_groups and selected_location in professional_groups[selected_service]:
            providers = professional_groups[selected_service][selected_location]
            self.provider_var.set("")  # Clear previous selection
            self.provider_combobox["values"] = providers

    def send_request(self):
        service = self.service_var.get()
        location = self.location_var.get()
        provider = self.provider_var.get()

        if service and location and provider:
            request_data = {
                "type": "request",
                "data": {
                    "service": service,
                    "location": location,
                    "provider": provider,
                    "client_id": id(self)  # Example client ID
                }
            }

            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(('127.0.0.1', 12345))
                self.client_socket.send(pickle.dumps(request_data))
                response = self.client_socket.recv(4096)
                response_message = pickle.loads(response)
                messagebox.showinfo("Request Sent", response_message)
                threading.Thread(target=self.receive_provider_response).start()
            except Exception as e:
                messagebox.showerror("Error", f"Error sending request: {e}")

    def receive_provider_response(self):
        while True:
            try:
                response = self.client_socket.recv(4096)
                if response:
                    response_message = pickle.loads(response)
                    self.response_label.config(text=response_message)
            except Exception as e:
                messagebox.showerror("Error", f"Error receiving response: {e}")
                break

    def receive_requests(self):
        while True:
            try:
                response = self.provider_socket.recv(4096)
                if response:
                    request_message = pickle.loads(response)
                    self.requests_listbox.insert(tk.END, f"Request from Client {request_message['client_id']}: {request_message['service']} in {request_message['location']}")
            except Exception as e:
                messagebox.showerror("Error", f"Error receiving requests: {e}")
                break

    def accept_request(self):
        selected_index = self.requests_listbox.curselection()
        if selected_index:
            request_info = self.requests_listbox.get(selected_index)
            self.requests_listbox.delete(selected_index)

            # Example response back to server
            response_data = {
                "type": "response",
                "data": {
                    "request_info": request_info,
                    "status": "accepted"
                }
            }
            self.provider_socket.send(pickle.dumps(response_data))
            messagebox.showinfo("Request Accepted", f"You accepted: {request_info}")

    def reject_request(self):
        selected_index = self.requests_listbox.curselection()
        if selected_index:
            request_info = self.requests_listbox.get(selected_index)
            self.requests_listbox.delete(selected_index)

            # Example response back to server
            response_data = {
                "type": "response",
                "data": {
                    "request_info": request_info,
                    "status": "rejected"
                }
            }
            self.provider_socket.send(pickle.dumps(response_data))
            messagebox.showinfo("Request Rejected", f"You rejected: {request_info}")

if __name__ == "__main__":
    app = ClientProviderApp()
    app.mainloop()
