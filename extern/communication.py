#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bluetooth
import os
from time import sleep
import threading


class Communication:
    def __init__(self, mode:str="client"):
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.connections = []
        os.system("bluetoothctl discoverable on")
        os.system("bluetoothctl pairable on")
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.type = mode
        self.thread_connections = threading.Thread(target=self.list_connections) # Update the connections in the background
        self.thread_connections.start()

    def send(self, value: str):
        self.sock.send(value.encode())

    def receive(self):
        return self.sock.recv(1024).decode()

    def wait_for_connection(self) -> str:
        """Used in server mode"""
        assert self.type == "server", ValueError("Must be server")

        self.sock.bind(("", bluetooth.PORT_ANY))
        self.sock.listen(1)
        port = self.sock.getsockname()[1]
        bluetooth.advertise_service(
            self.sock,
            "connect4-4",
            service_id=self.uuid,
            service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
        )

        print("Waiting for connection on RFCOMM channel", port)
        self.sock, self.client_info = self.sock.accept()
        print("Accepted connection from", self.client_info)

        # Need to wait for code 100 or 101
        code = self.receive()
        return code

    def get_name_client(self) -> str:
        """ Get the name of the device trying to connect to us """
        assert self.type == "server", ValueError(f"Must be server, not {self.type}")
        mac = self.client_info[0]
        for d in self.connections:
            if d[0] == self.client_info[0]:
                return d[1]
        return "[unknow device]"

    def list_connections(self) -> None:
        """List the connections. Can be used in both mode"""
        nearby_devices = bluetooth.discover_devices(
            duration=5, lookup_names=True, flush_cache=True, lookup_class=False
        )
        self.connections = []
        for d in nearby_devices:
            # Filter the devices
            # if "connect4" in d[1]:
            self.connections.append(d)

    def connect(self, index: int, message: str) -> str:
        """Connect to a server. Usable only on client mode"""
        assert self.type == "client", ValueError("Must be client")
        print(self.connections, index)
        addr = self.connections[index][0]
        matches = []
        i = 0
        while matches == []:
            print("Searching", " " * 30, end="\r")
            matches = bluetooth.find_service(uuid=self.uuid, address=addr) # Find the device we choosed
            if matches == []:
                i += 1
                # Somtimes it does not found it despite it being here, wait a little then search again
                print(f"Nothing found, sleeping... x{i}", end="\r")
                sleep(2.5)
            else:
                print(matches)
        choosed = matches[0]

        self.sock.connect((choosed["host"], choosed["port"]))
        self.send(message)

        # Receive the code, but let something else decide what to do with the code
        code = self.receive()
        return code
