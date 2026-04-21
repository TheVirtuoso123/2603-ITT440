# NAME : NURUL FAR'AIN BINTI MOHD HASNIZAM
# STUDENT ID : 2024214892
# GROUP : M3CS2554B
# TITLE : SQUARE NUMBER GENERATOR

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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 65432))
server_socket.listen(1)

print("--- SERVER SQUARE GENERATOR SEDANG BERJALAN ---")
print("Menunggu sambungan daripada client...")

while True:
    # Terima sambungan
    conn, addr = server_socket.accept()
    print(f"Client bersambung dari: {addr}")
    
    # Terima nombor dari client
    data = conn.recv(1024).decode()
    
    if data:
        try:
            number = int(data)
            result = number * number
            print(f"Menerima nombor: {number}. Menghantar hasil: {result}")
            
            # Hantar jawapan balik
            conn.send(str(result).encode())
        except ValueError:
            conn.send("Sila masukkan nombor sahaja!".encode())
            
    conn.close()
~~~



Client Side (client.py)
~~~
import socket

# Setup Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 65432))

# Input nombor
number = input("Masukkan nombor yang ingin dikuasa duakan: ")
client_socket.send(number.encode())

# Terima hasil
jawapan = client_socket.recv(1024).decode()
print(f"Hasil dari Server: {jawapan}")

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
<img width="1236" height="854" alt="image" src="https://github.com/user-attachments/assets/d4ecbcf8-c316-4982-a836-0397c6efdc5e" />



Execution Process
~~~
client.py
~~~
Output:
<img width="1232" height="791" alt="image" src="https://github.com/user-attachments/assets/c8f2cf15-e9a2-4cc1-a5a7-db4c99bab26d" />

# Conclusion
This task successfully demonstrates the practical implementation of network communication. By using TCP sockets, the application ensures data integrity. The project has strengthened the understanding of the Transport Layer within the OSI model.
