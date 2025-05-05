import pygame
from PySide6.QtCore import QObject, Signal, QTimer


class JoystickController(QObject):
    # 定义信号
    axis_changed = Signal(int, float)  # 参数：轴编号，值
    button_changed = Signal(int, int)  # 参数：按钮编号，状态
    hat_changed = Signal(int, tuple)    # 参数：帽子编号，(x,y)值

    def __init__(self):
        super().__init__()
        # 初始化pygame和手柄
        pygame.init()
        pygame.joystick.init()
        
        # 初始化属性
        self.done = False
        self.clock = pygame.time.Clock()
        self.joysticks = {}  # 存储所有已连接的手柄
        
        # 存储上一次的轴、按钮和帽子的值，用于检测变化
        self.last_axes_values = {}
        self.last_button_values = {}
        self.last_hat_values = {}
        
        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        
        self._init_joysticks()
        self.start_polling()

    def _init_joysticks(self):
        """初始化所有连接的手柄"""
        self.joysticks.clear()
        self.last_axes_values.clear()
        self.last_button_values.clear()
        self.last_hat_values.clear()
        
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks[i] = joystick
            # 初始化该手柄所有轴、按钮和帽子的上一次值
            self.last_axes_values[i] = [0.0] * joystick.get_numaxes()
            self.last_button_values[i] = [False] * joystick.get_numbuttons()
            self.last_hat_values[i] = [(0, 0)] * joystick.get_numhats()

    def start_polling(self, interval=16):  # 约60fps
        """开始轮询手柄状态"""
        self.timer.start(interval)

    def stop_polling(self):
        """停止轮询"""
        self.timer.stop()

    def get_joystick_count(self):
        """获取已连接的手柄数量"""
        return pygame.joystick.get_count()

    def get_joystick_name(self, joystick_id):
        """获取指定手柄的名称"""
        if joystick_id in self.joysticks:
            return self.joysticks[joystick_id].get_name()
        return None

    def get_axes_values(self, joystick_id):
        """获取指定手柄的所有轴的值"""
        if joystick_id not in self.joysticks:
            return []
            
        joystick = self.joysticks[joystick_id]
        axes_values = []
        for i in range(joystick.get_numaxes()):
            axis = joystick.get_axis(i)
            axes_values.append((i, axis))
        return axes_values

    def get_buttons_values(self, joystick_id):
        """获取指定手柄的所有按钮的状态"""
        if joystick_id not in self.joysticks:
            return []
            
        joystick = self.joysticks[joystick_id]
        button_values = []
        for i in range(joystick.get_numbuttons()):
            button = joystick.get_button(i)
            button_values.append((i, button))
        
        return button_values

    def get_hats_values(self, joystick_id):
        """获取指定手柄的所有帽子开关的值"""
        if joystick_id not in self.joysticks:
            return []
            
        joystick = self.joysticks[joystick_id]
        hat_values = []
        for i in range(joystick.get_numhats()):
            hat = joystick.get_hat(i)
            hat_values.append((i, hat))
        return hat_values

    def update(self):
        """更新手柄状态，处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.JOYDEVICEADDED:
                self._init_joysticks()
            elif event.type == pygame.JOYDEVICEREMOVED:
                self._init_joysticks()

        # 检查每个手柄的状态
        for joystick_id, joystick in self.joysticks.items():
            # 检查轴的值
            for axis in range(joystick.get_numaxes()):
                current_value = joystick.get_axis(axis)
                if abs(current_value - self.last_axes_values[joystick_id][axis]) > 0.01:
                    self.axis_changed.emit(axis, current_value)
                    self.last_axes_values[joystick_id][axis] = current_value

            # 检查按钮的状态
            for button in range(joystick.get_numbuttons()):
                current_state = joystick.get_button(button)
                if current_state != self.last_button_values[joystick_id][button]:
                    self.button_changed.emit(button, current_state)
                    self.last_button_values[joystick_id][button] = current_state

            # 检查帽子开关的状态
            for hat in range(joystick.get_numhats()):
                current_value = joystick.get_hat(hat)
                if current_value != self.last_hat_values[joystick_id][hat]:
                    self.hat_changed.emit(hat, current_value)
                    self.last_hat_values[joystick_id][hat] = current_value

    def quit(self):
        """退出并清理"""
        self.stop_polling()
        pygame.quit()

    def is_done(self):
        """返回是否应该退出"""
        return self.done


# 使用示例
if __name__ == '__main__':
    controller = JoystickController()
    
    while not controller.is_done():
        controller.update()
        
        # 获取所有手柄的信息
        for i in range(controller.get_joystick_count()):
            print(f"\n手柄 {i} ({controller.get_joystick_name(i)}):")
            print("轴的值:", controller.get_axes_values(i))
            print("按钮状态:", controller.get_buttons_values(i))
            print("帽子开关:", controller.get_hats_values(i))
        
        # 限制刷新率
        controller.clock.tick(20)
    
    controller.quit()