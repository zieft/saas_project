from abc import ABCMeta, abstractmethod
from time import sleep


class Window:
    @abstractmethod
    def start(self):  # 原子操作、钩子方法
        pass

    # 父类中写出框架和模板、逻辑
    # 在子类中再做具体实现
    @abstractmethod
    def repaint(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def run(self):
        # 这个run就是模板方法
        # 这里定义好框架，高层程序员直接拿来用
        self.start()
        while True:
            try:
                self.repaint()
                sleep(1)
            except KeyboardInterrupt:
                break
        self.stop()


class MyWindow(Window):
    def __init__(self, msg):
        self.msg = msg

    def start(self):
        print('window started!')

    def stop(self):
        print('window stopped')

    def repaint(self):
        print(self.msg)


MyWindow('Hello...').run()
