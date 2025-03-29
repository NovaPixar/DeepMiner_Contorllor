from PySide6.QtCore import QThread, Signal


class ConnectionThread(QThread):
    connectionResult = Signal(bool)

    def __init__(self, ip, port, connector):
        super().__init__()
        self.ip = ip
        self.port = port
        self.connector = connector

    def run(self):
        result = self.connector.checkConnection(self.ip, self.port)
        self.connectionResult.emit(result)