import socket
import threading


class ClientThread(threading.Thread):

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", clientAddress)

        employeeID = ["E00123", "E01033"]
        employeeName = ["Aadya Khan", "John Smith"]
        employeeSalary = [38566, 43123]

        while True:
            self.c_socket.send(bytes('HR System 1.0'
                                     '\nWhat is the employee id?', 'UTF-8'))
            data = self.c_socket.recv(512)
            employeeIDRecv = data.decode()
            print(employeeIDRecv)

            if employeeIDRecv in employeeID:
                self.c_socket.send(bytes('Salary (S) or Annual Leave (L) Query?', 'UTF-8'))
                data = self.c_socket.recv(512)
                msg = data.decode()

                if msg == 'S':
                    index = employeeID.index(employeeIDRecv)
                    msg = employeeSalary[index]
                    self.c_socket.send(bytes(msg, 'UTF-8'))
                if msg == 'L':
                    self.c_socket.send(bytes('Current Entitlement (C) or Leave taken for your (Y)', 'UTF-8'))
                    data = self.c_socket.recv(512)
                    msg = data.decode()

            else:
                self.c_socket.send(bytes('Sorry... I don\'t recognise that employee id', 'UTF-8'))

        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "127.0.0.1"
PORT = 64001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

counter = 0

while True:
    server.listen(1)
    my_socket, clientAddress = server.accept()
    counter = counter + 1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.start()
    print(f"Active Connections: {threading.active_count() - 1}")
