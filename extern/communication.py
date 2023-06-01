#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bluetooth
import os

class Communication:
    def __init__(self):
        os.system("bluetoothctl discoverable on")
        os.system("bluetoothctl pairable on")
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.connections = []
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.type = "client"

    def wait_for_connection(self):
        """ Used in server mode """
        assert self.type == "server", ValueError("Must be server")

        self.sock.bind(("", bluetooth.PORT_ANY))
        self.sock.listen(1)
        port = self.sock.getsockname()[1]
        bluetooth.advertise_service(self.sock, "connect4-4", service_id=self.uuid,
                                    service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        print("Waiting for connection on RFCOMM channel", port)
        self.sock, self.client_info = self.sock.accept()
        print("Accepted connection from", self.client_info)

        # May need to wait for code 100
        code = self.sock.recv(3).decode()
        assert code == "100", ValueError(f"Wrong code {code}")

        # Accept connection
        self.sock.send("102".encode())
        # Server have to send 102 or 103

    def list_connections(self):
        """ List the connections. Usable only in cient mode """
        assert self.type == "client", ValueError("Must be client")
        nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True, flush_cache=True, lookup_class=False)
        self.connections = []
        for d in nearby_devices:
            # if "connect4" in d[1]:
            self.connections.append(d)
            print(d)
        return self.connections

    def connect(self, index):
        """ Connect to a server. Usable only on client mode """
        assert self.type == "client", ValueError("Must be client")
        matches = []
        while matches == []:
            matches = bluetooth.find_service(uuid=self.uuid, address=self.connections[index][0])
            print(matches)
        choosed = matches[0]

        self.sock.connect((choosed["host"], choosed["port"]))
        sleep(3)
        self.sock.send("100".encode())

        code = self.sock.recv(16).decode()
        if code not in ["102", "103"]:
            print(f"Code not correct {code}")
            exit()
        return code

    def send(self, column: int):
        self.sock.send(f"{column}".encode())

    def receive(self):
        return self.sock.recv(1024).decode()
