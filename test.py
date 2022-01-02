employeeID = ["E00123", "E01033"]

employeeIDRecv = input("Enter ID:\t")

if employeeIDRecv in employeeID:
    print("Is employee")

else:
    print("Not employee")

while True:
    self.c_socket.send(bytes('HR System 1.0'
                             '\nWhat is the employee id?', 'UTF-8'))
    data = self.c_socket.recv(512)
    employeeIDRecv = data.decode()
    print("got here")



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