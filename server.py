import socket
import threading

employeeID = ["E00123", "E01033"]
employeeName = ["Aadya Khan", "John Smith"]
employeeSalary = [38566, 43123]
salaryYear = [2016, 2017, 2018]
yearlySalForKhan = [29800, 32032, 35604]
yearlySalForSmith = [30800, 36032, 41604]
overTimeForKhan = [2412, 2134, 3212]
overTimeForSmith = [2123, 2124, 2587]
currentLeave = [25, 20]
leaveYear = [2016, 2017, 2018]
yearlyLeaveForKhan = [22, 32, 31]
yearlyLeaveForSmith = [18, 31, 31]


def msgYearlyTotal(index, year):
    indexYear = salaryYear.index(year)
    if index == 0:
        basicPay = yearlySalForKhan[indexYear]
        overTime = overTimeForKhan[indexYear]

    if index == 1:
        basicPay = yearlySalForSmith[indexYear]
        overTime = overTimeForSmith[indexYear]

    msgToClientSal = f'\nEmployee {employeeName[index]}' \
                     f'\nTotal Salary for {year}: Basic pay, {basicPay}, Overtime, {overTime}' \
                     f'\nWould you like to continue (C) or exit (X)?'

    return msgToClientSal


def msgLeaveForYear(index, year):
    indexYear = leaveYear.index(year)
    if index == 0:
        leaveTaken = yearlyLeaveForKhan[indexYear]

    if index == 1:
        leaveTaken = yearlyLeaveForSmith[indexYear]

    msg = f'\nEmployee {employeeName[index]}' \
          f'\nLeave take in {year}: {leaveTaken} days' \
          f'\nWould you like to continue (C) or exit (X)?'

    return msg


class ClientThread(threading.Thread):

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", clientAddress)

        data = self.c_socket.recv(2048)
        msg = data.decode()
        print("from client", msg)

        leave = False

        while not leave:
            leave = False
            self.c_socket.send(bytes('\nHR System 1.0'
                                     '\nWhat is the employee id?', 'UTF-8'))
            data = self.c_socket.recv(2048)
            employeeIDRecv = data.decode()
            print("from client", employeeIDRecv)

            if employeeIDRecv in employeeID:
                print("Valid ID")
                self.c_socket.send(bytes('\nSalary (S) or Annual Leave (L) Query?', 'UTF-8'))
                data = self.c_socket.recv(512)
                msg = data.decode()

                if msg == 'S' or msg == 's':
                    self.c_socket.send(bytes('\nCurrent salary (C) or total salary (T) for year?', 'UTF-8'))
                    while True:
                        data = self.c_socket.recv(512)
                        msgSalary = data.decode()
                        if msgSalary == 'C' or msgSalary == 'c':
                            index = employeeID.index(employeeIDRecv)
                            msgSalSend = f'\nEmployee {employeeName[index]} ' \
                                         f'\nCurrent basic salary: {employeeSalary[index]}' \
                                         f'\nWould you like to continue (C) or exit (X)?'
                            self.c_socket.send(bytes(msgSalSend, 'UTF-8'))
                            data = self.c_socket.recv(512)
                            msg = data.decode()

                            if msg == 'X' or msg == 'x':
                                leave = True

                            break

                        elif msgSalary == 'T' or msgSalary == 't':
                            index = employeeID.index(employeeIDRecv)
                            self.c_socket.send(bytes('\nWhat year?', 'UTF-8'))
                            data = self.c_socket.recv(512)
                            msgYear = data.decode()
                            year = int(msgYear)
                            msg = msgYearlyTotal(index, year)

                            self.c_socket.send(bytes(msg, 'UTF-8'))
                            data = self.c_socket.recv(512)
                            msg = data.decode()

                            if msg == 'X' or msg == 'x':
                                leave = True

                            break

                        else:
                            self.c_socket.send(bytes('\nNot an option!'
                                                     '\nCurrent salary (C) or total salary (T) for year?', 'UTF-8'))

                elif msg == 'L' or msg == 'l':
                    self.c_socket.send(bytes('\nCurrent Entitlement (C) or Leave taken for your (Y)', 'UTF-8'))
                    while True:
                        data = self.c_socket.recv(512)
                        msgLeave = data.decode()
                        if msgLeave == 'C' or msgLeave == 'c':
                            index = employeeID.index(employeeIDRecv)
                            msgCLeave = f'\nEmployee {employeeName[index]}' \
                                        f'\nCurrent annual leave entitlement: {currentLeave[index]}' \
                                        f'\nWould you like to continue (C) or exit (X)?'

                            self.c_socket.send(bytes(msgCLeave, 'UTF-8'))
                            data = self.c_socket.recv(512)
                            msg = data.decode()

                            if msg == 'X' or msg == 'x':
                                leave = True

                            break

                        elif msgLeave == 'Y' or msgLeave == 'y':
                            index = employeeID.index(employeeIDRecv)
                            self.c_socket.send(bytes('\nWhat year?', 'UTF-8'))
                            data = self.c_socket.recv(512)
                            msgYear = data.decode()
                            year = int(msgYear)
                            msgYLeave = msgLeaveForYear(index, year)

                            self.c_socket.send(bytes(msgYLeave, 'UTF-8'))
                            data = self.c_socket.recv(512)
                            msg = data.decode()

                            if msg == 'X' or msg == 'x':
                                leave = True

                            break

                        else:
                            self.c_socket.send(bytes('\nNot an option!'
                                                     '\nCurrent Entitlement (C) or Leave taken for your (Y)', 'UTF-8'))

                else:
                    self.c_socket.send(bytes('\nNot an option!'
                                             '\nCurrent salary (C) or total salary (T) for year?', 'UTF-8'))

            else:
                self.c_socket.send(bytes('\nSorry... I don\'t recongnise that employee ID'
                                         '\nWhat is the employee id?', 'UTF-8'))

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
