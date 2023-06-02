#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import bluetooth
bluetooth = None
import os
from time import sleep

class Communication:
    def __init__(self):
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.connections = []
        os.system("bluetoothctl discoverable on")
        os.system("bluetoothctl pairable on")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.type = "client"

    def send(self, value: str):
        self.sock.send(value.encode())

    def receive(self):
        return self.sock.recv(1024).decode()

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
        code = self.receive()
        assert code == "100" or code == "101", ValueError(f"Wrong code {code}")

        # Accept connection
        self.send("102")
        # Server have to send 102 or 103

    def list_connections(self):
        """ List the connections. Usable only in cient mode """
        assert self.type == "client", ValueError("Must be client")
        nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True, flush_cache=True, lookup_class=False)
        self.connections = []
        for d in nearby_devices:
            # if "connect4" in d[1]:
            self.connections.append(d)
        return self.connections

    def connect(self, index: int, message: str) -> str:
        """ Connect to a server. Usable only on client mode """
        assert self.type == "client", ValueError("Must be client")
        print(self.connections, index)
        addr = self.connections[index][0]
        matches = []
        i = 0
        while matches == []:
            print("Searching", " "*30, end="\r")
            matches = bluetooth.find_service(uuid=self.uuid, address=addr)
            if matches == []:
                i += 1
                print(f"Nothing found, sleeping... x{i}", end="\r")
                sleep(2.5)
            else:
                print(matches)
        choosed = matches[0]

        self.sock.connect((choosed["host"], choosed["port"]))
        self.send(message)

        code = self.receive()
        if code not in ["102", "103"]:
            print(f"Code not correct {code}")
            exit()
        return code
