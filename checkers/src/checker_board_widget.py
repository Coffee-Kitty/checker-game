import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QResizeEvent, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication


from checkers.src.checker_board import CheckerBoard


class CheckerBoardWidget(QWidget):

    def __init__(self, board: CheckerBoard):
        super().__init__()
        self.board = board


        self.startX = 0
        self.startY = 0
        self.widget_width_size = 800
        self.widget_height_size = 800
        self.setGeometry(self.startX, self.startY, self.widget_width_size, self.widget_height_size)

        # 一个棋子的格子的宽高
        self.grid_width_size = self.widget_width_size/self.board.checker_width
        self.grid_height_size = self.widget_height_size/self.board.checker_height


        self.setWindowTitle("国跳100 coffee_cat")



    def drawBrownSolidRectangle(self, left_top: tuple, right_bottom: tuple, painter: QPainter) -> None:
        """
        画深色格子  左上角坐标(x,y) 右下角坐标(x,y)
        """
        # 设置矩形的填充颜色为棕色
        painter.setBrush(QColor(165, 42, 42))  # 使用 RGB 值指定棕色
        # 绘制棕色实心矩形
        painter.drawRect(left_top[0], left_top[1], right_bottom[0]-left_top[0], right_bottom[1]-left_top[1])

    def drawWhiteSolidRectangle(self, left_top: tuple, right_bottom: tuple, painter: QPainter) -> None:
        """
        画浅色格子  左上角坐标(x,y) 右下角坐标(x,y)
        """
        # 设置矩形的填充颜色为浅棕色
        painter.setBrush(QColor(205, 133, 63))  # 使用 RGB 值指定浅棕色
        # 绘制浅棕色实心矩形
        painter.drawRect(left_top[0], left_top[1], right_bottom[0]-left_top[0], right_bottom[1]-left_top[1])

    def draw_white_checker(self, center_x: int, center_y: int, radius: int, painter: QPainter) -> None:

        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿效果
        painter.setBrush(Qt.white)
        # 绘制实心圆形
        radius = radius  # 圆形半径
        x = center_x  # 圆心横坐标
        y = center_y  # 圆心纵坐标
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def draw_black_checker(self, center_x: int, center_y: int, radius: int, painter: QPainter) -> None:

        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿效果
        painter.setBrush(Qt.black)
        # 绘制实心圆形
        radius = radius  # 圆形半径
        x = center_x  # 圆心横坐标
        y = center_y  # 圆心纵坐标
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)




    def paintEvent(self, a0: QPaintEvent) -> None:
        # 创建绘图对象
        painter = QPainter(self)

        # 画出棋盘
        draw_board = self.board.board
        for i in range(self.board.width):
            for j in range(self.board.height):
                if (i + j) % 2 == 0:  # i+j 是偶数则为深色格子 否则为浅色格子
                    (x,y)=(i*self.grid_width_size,j*self.grid_height_size)
                    self.drawBrownSolidRectangle((x,y),(x+self.grid_width_size,y+self.grid_height_size),painter)
                else:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.drawWhiteSolidRectangle((x, y), (x + self.grid_width_size, y + self.grid_height_size), painter)


        # 完成绘制，释放资源
        painter.end()



    def mousePressEvent(self, a0: QMouseEvent) -> None:
        pass


    def resizeEvent(self, a0: QResizeEvent) -> None:
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)

    checker_board_widget = CheckerBoardWidget(board=CheckerBoard(CheckerBoard.width, CheckerBoard.height, CheckerBoard.white_color))
    checker_board_widget.show()


    sys.exit(app.exec_())


