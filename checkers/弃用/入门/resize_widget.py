import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

if __name__ == "__main__":

    # 1.创建qt程序对象
    app = QApplication(sys.argv)

    w = QWidget()

    w.setWindowTitle("第一个PyQt")

    w.resize(1000,500)

    # # 获得屏幕中心坐标
    center_point = QDesktopWidget().availableGeometry().center()
    x,y=center_point.x(),center_point.y()
    # w.move(center_point.x()-500,center_point.y()-250)

    # 第二种方法移动到屏幕中心
    # print(w.frameGeometry())
    oldx,oldy,width,height = w.frameGeometry().getRect()
    w.move(x-width/2,y-height/2)

    w.show()

    # 2.程序进入循环等待状态
    app.exec_()