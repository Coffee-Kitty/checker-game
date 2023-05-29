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
        self.grid_width_size = self.widget_width_size / self.board.board_width_check_nums
        self.grid_height_size = self.widget_height_size / self.board.board_height_check_nums

        self.setWindowTitle("国跳100 coffee_cat")

        # 接下来是事件处理
        self.clicked_check = (-1, -1)  # 当前点击的棋子位置
        self.where = []  # 记录当前所有的子的 可以落子的地方并将其绘制
        self.if_can_eat = False
        self.eaten_list = []
        self.history = []  # 历史记录list  用list模拟队列queue

    def drawBrownSolidRectangle(self, left_top: tuple, right_bottom: tuple, painter: QPainter) -> None:
        """
        画深色格子  左上角坐标(x,y) 右下角坐标(x,y)
        """
        # 设置矩形的填充颜色为棕色
        painter.setBrush(QColor(99, 87, 70))  # 使用 RGB 值指定棕色
        # 绘制棕色实心矩形
        painter.drawRect(left_top[0], left_top[1], right_bottom[0] - left_top[0], right_bottom[1] - left_top[1])

    def drawWhiteSolidRectangle(self, left_top: tuple, right_bottom: tuple, painter: QPainter) -> None:
        """
        画浅色格子  左上角坐标(x,y) 右下角坐标(x,y)
        """
        # 设置矩形的填充颜色为
        painter.setBrush(QColor(174, 165, 150))  # 使用 RGB 值指定浅棕色
        # 绘制实心矩形
        painter.drawRect(left_top[0], left_top[1], right_bottom[0] - left_top[0], right_bottom[1] - left_top[1])

    def drawaAtivateSolidRectangle(self, left_top: tuple, right_bottom: tuple, painter: QPainter) -> None:
        """
        画浅色格子  左上角坐标(x,y) 右下角坐标(x,y)
        """
        # 设置矩形的填充颜色为
        painter.setBrush(Qt.green)
        # 绘制实心矩形
        painter.drawRect(left_top[0], left_top[1], right_bottom[0] - left_top[0], right_bottom[1] - left_top[1])

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
        """
        尤其注意  原本board上的的(0,0)位置的棋子应该落在（i，9-j）的位置
        """

        # 创建绘图对象
        painter = QPainter(self)

        # 画出棋盘和棋子
        draw_board = self.board.board

        for i in range(self.board.board_width_check_nums):
            for j in range(self.board.board_height_check_nums):
                if (i + j) % 2 == 0:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.drawWhiteSolidRectangle((int(x), int(y)),
                                                 (int(x + self.grid_width_size), int(y + self.grid_height_size)),
                                                 painter)
                else:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.drawBrownSolidRectangle((int(x), int(y)),
                                                 (int(x + self.grid_width_size), int(y + self.grid_height_size)),
                                                 painter)

                # 画出棋子
                if draw_board[self.board.white_color][i][j] == 1:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.draw_white_checker(int(x + self.grid_width_size / 2), int(y + self.grid_height_size / 2),
                                            int((self.grid_width_size + self.grid_height_size) / 4), painter)
                elif draw_board[self.board.black_color][i][j] == 1:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.draw_black_checker(int(x + self.grid_width_size / 2), int(y + self.grid_height_size / 2),
                                            int((self.grid_width_size + self.grid_height_size) / 4), painter)

        if len(self.where) > 0:
            for w in self.where:
                print(w)
                (x, y) = (w[0] * self.grid_width_size, w[1] * self.grid_height_size)
                self.drawaAtivateSolidRectangle((int(x), int(y)),
                                                (int(x + self.grid_width_size), int(y + self.grid_height_size)),
                                                painter)

        # 完成绘制，释放资源
        painter.end()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            x = int(a0.pos().x() / self.grid_width_size)
            y = int(a0.pos().y() / self.grid_height_size)
            print(f"点击了位置：{(x, y)}")
            (old_x, old_y) = self.clicked_check

            self.if_can_eat, self.where, self.eaten_list = self.board.getNextAction()



            # 1.如果点击的位置 能够下，那么下棋 并注意history
            if len(self.where) > 0 and (x, y) in self.where and (x,y) in self.board.position_can_move(old_x, old_y)[1]:
                # 更改board
                if self.if_can_eat:
                    self.board.eat(self.board.my_color,old_x,old_y,x,y, self.eaten_list)
                else:
                    self.board.player(self.board.my_color,old_x,old_y,x,y)
                # 记录history
                if self.board.my_color == self.board.white_color:
                    self.history.append(("white", (old_x, old_y), (x, y)))
                else:
                    self.history.append(("black", (old_x, old_y), (x, y)))
                print("history更新为" + self.history.__str__())
                # 清空where ， clicked_check,
                self.clicked_check = (-1, -1)
                # 注意更改my_color  因为已经落子后，接着轮到对方下子
                self.board.my_color = 1 - self.board.my_color
                self.if_can_eat, self.where, self.eaten_list = self.board.getNextAction()
                # 重绘制
                self.repaint()

                return

            # 2.如果不能下，那么如果此位置是一个 本方棋子，就重新更新clicked_check
            if self.board.board[self.board.my_color][x][y] == 1:
                print(f"此位置为白棋{(x, int(self.board.board_width_check_nums - 1 - y))}")

                self.clicked_check = (x, y)


            # elif self.board.board[self.board.black_color][x][y] == 1:
            #     print(f"此位置为黑棋{(x, int(self.board.board_width_check_nums - 1 - y))}")
            #     where = self.board.position_can_move(x, y)
            #     if len(where) > 0:
            #         self.where = where
            #         self.clicked_check = (x, y)
            #         self.repaint()
            # 3.---------------------不是一个棋子，不予理会
            else:
                print("点击位置不是本方棋子或者没有棋子")
            self.repaint()

    # def resizeEvent(self, a0: QResizeEvent) -> None:
    #     # 新的窗口大小
    #     (new_wid, new_hei) = a0.size().width(), a0.size().height()
    #
    #     # 如果棋盘不是正方形会出错误
    #     if new_hei != new_wid:
    #         new_hei = new_wid = min(new_wid, new_hei)
    #
    #     self.widget_width_size = new_wid
    #     self.widget_height_size = new_hei
    #
    #     # 一个棋子的格子的宽高
    #     self.grid_width_size = self.widget_width_size / self.board.board_width_check_nums
    #     self.grid_height_size = self.widget_height_size / self.board.board_height_check_nums


if __name__ == "__main__":
    app = QApplication(sys.argv)

    board = CheckerBoard(CheckerBoard.board_width_check_nums, CheckerBoard.board_height_check_nums,
                         CheckerBoard.white_color)
    board.show_board()

    checker_board_widget = CheckerBoardWidget(
        board=board)
    checker_board_widget.show()

    sys.exit(app.exec_())
