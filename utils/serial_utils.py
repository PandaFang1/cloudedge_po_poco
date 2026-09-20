class Ser:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def connect(self):
        # Connect to the serial port
        pass

    def write(self, data):
        # Write data to the serial port
        pass

    def read(self):
        # Read data from the serial port
        pass

    def close(self):
        # Close the serial port connection
        pass