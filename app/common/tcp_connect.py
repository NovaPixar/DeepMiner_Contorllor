import socket


class TcpConnect:
    def __init__(self):
        self.serverAddress = None
        self.RobotIP = None
        self.RobotPort = None
        self.isConnect = False
        self.connectMessage = ""
        self.clientSocket = None

    def checkConnection(self, RobotIP, RobotPort):
        self.RobotIP = RobotIP
        self.RobotPort = int(RobotPort)
        self.serverAddress = (self.RobotIP, self.RobotPort)
        print("正在连接到机器...")
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientSocket.connect(self.serverAddress)
            print("已连接到服务端")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            self.connectMessage = f"连接失败: {e}"
            return False
