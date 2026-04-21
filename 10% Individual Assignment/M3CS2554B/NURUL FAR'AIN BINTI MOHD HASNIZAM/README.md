# NAME : NURUL FAR'AIN BINTI MOHD HASNIZAM
# STUDENT ID : 2024214892
# GROUP : M3CS2554B
# TITLE : SQUARE NUMBER GENERATOR

<img width="1132" height="489" alt="image" src="https://github.com/user-attachments/assets/c4b8fc4f-04e3-4d6e-86be-d97fb967bfb3" />

# Requirements
- Python 3.13
- VS Code

# Files
- server.py : The server-side script that listens for connections and performs the calculation.
- client.py : The client.py script that sends a number to the server and displays the result.

# Introduction
The objective of this individual task is to apply the fundamental concepts of Socket Programming using Python. The project involves building a network-based application called the Square Number Generator. In this application, a Client sends a specific integer to a Server which processes the data to find its square and returns the result back to the Client.

# Objectives
1. To understand Client-Server communication mechanisms using TCP (Transmission Control Protocol)
2. To implement the Python
   ~~~
   socket
   ~~~
   library for network connectivity
3. To master data encoding and decoding during transmission.

# System Design
The system follows a standard Client-Server architecture. We use TCP because it is connection-oriented, ensuring that the data is delivered reliably and in the correct order.

# Source Code Implementation
Server Side (server.py)
~~~
import socket

# Setup Server
# AF_INET refers to the address family (IPv4)
# SOCK_STREAM refers to the socket type (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 65432))
server_socket.listen(1)

print("--- SERVER SQUARE GENERATOR IS RUNNING ---")
print("Waiting for a connection from the client...")

while True:
    # Accept connection
    conn, addr = server_socket.accept()
    print(f"Client connected from: {addr}")
    
    # Receive data from client
    data = conn.recv(1024).decode()
    
    if data:
        try:
            # Convert received string to integer
            number = int(data)
            result = number * number
            print(f"Received number: {number}. Sending result: {result}")
            
            # Send the result back to the client
            conn.send(str(result).encode())
        except ValueError:
            # Error handling for non-integer inputs
            conn.send("Error: Please enter numbers only!".encode())
            
    # Close the specific connection
    conn.close()
~~~



Client Side (client.py)
~~~
import socket

# Setup Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server's IP address and port
client_socket.connect(('127.0.0.1', 65432))

# Input number
# Prompt the user to enter a value to be squared
number = input("Enter a number to be squared: ")
client_socket.send(number.encode())

# Receive result
result = client_socket.recv(1024).decode()
print(f"Result from Server: {result}")

# Close the connection
client_socket.close()
~~~

# How to run
1. Run the server first :
   ~~~
   python server.py
   ~~~
2. Open a second terminal and run the client :
   ~~~
   python client.py
   ~~~
3. Enter a number in the client terminal to receive the squared result.


# Results and Discussion
Execution Process
~~~
server.py
~~~
Output:
<img width="1232" height="868" alt="image" src="https://github.com/user-attachments/assets/3423e54e-dcd5-41d8-961f-adbdcc9e15ec" />


Execution Process
~~~
client.py
~~~
Output:
<img width="1228" height="792" alt="image" src="https://github.com/user-attachments/assets/b0f27ef6-472b-41f1-b5ec-5cb7d922316e" />


# Conclusion
This task successfully demonstrates the practical implementation of network communication. By using TCP sockets, the application ensures data integrity. The project has strengthened the understanding of the Transport Layer within the OSI model.

# Demostration Video
