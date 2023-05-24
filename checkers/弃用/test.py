from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import sys

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        # 创建绘图对象
        painter = QPainter(self)

        # 设置绘图参数
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿效果
        painter.setPen(QPen(Qt.black, 2))

        # 设置棋子的颜色为白色
        painter.setBrush(Qt.white)

        # 绘制白棋
        radius = 20  # 棋子半径
        x = 50  # 棋子中心点横坐标
        y = 50  # 棋子中心点纵坐标
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

        # 完成绘制，释放资源
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
