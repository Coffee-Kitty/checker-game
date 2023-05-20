import sys
from PyQt5.QtWidgets import QApplication,QWidget

if __name__ == "__main__":

    # 1.创建qt程序对象
    app = QApplication(sys.argv)

    w = QWidget()

    w.setWindowTitle("第一个PyQt")
    w.show()

    # 2.程序进入循环等待状态
    app.exec_()