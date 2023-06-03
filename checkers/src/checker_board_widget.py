import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QResizeEvent, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit

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
        self.end_list = [((int, int), [(int, int)])]
        self.history = []  # 历史记录list  用list模拟队列queue
        self.transition_history = []   # 记录王棋转变之际

        self.count = 0  # 记录回合数

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

    def drawaAtivateSolidRectangle(self, left_top: tuple, right_bottom: tuple, painter: QPainter, color: int) -> None:
        """
        画浅色格子  左上角坐标(x,y) 右下角坐标(x,y)
        """
        # 设置矩形的填充颜色为
        painter.setBrush(color)
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

    def draw_boss_checker(self, center_x: int, center_y: int, radius: int, painter: QPainter, color: int):
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿效果
        # 设置矩形的填充颜色为
        if color == Qt.black:
            painter.setBrush(Qt.red)  # 黑王琪为红色
        else:
            painter.setBrush(Qt.green)  # 白王琪为绿色

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
                elif draw_board[self.board.white_color][i][j] == 2:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.draw_boss_checker(int(x + self.grid_width_size / 2), int(y + self.grid_height_size / 2),
                                           int((self.grid_width_size + self.grid_height_size) / 4), painter, Qt.white)
                elif draw_board[self.board.black_color][i][j] == 2:
                    (x, y) = (i * self.grid_width_size, j * self.grid_height_size)
                    self.draw_boss_checker(int(x + self.grid_width_size / 2), int(y + self.grid_height_size / 2),
                                           int((self.grid_width_size + self.grid_height_size) / 4), painter, Qt.black)

        if len(self.where) > 0:
            for w in self.where:
                (x, y) = (w[0] * self.grid_width_size, w[1] * self.grid_height_size)
                if self.board.my_color == self.board.white_color:
                    self.drawaAtivateSolidRectangle((int(x), int(y)),
                                                    (int(x + self.grid_width_size), int(y + self.grid_height_size)),
                                                    painter, Qt.green)
                else:
                    self.drawaAtivateSolidRectangle((int(x), int(y)),
                                                    (int(x + self.grid_width_size), int(y + self.grid_height_size)),
                                                    painter, Qt.red)

        # 完成绘制，释放资源
        painter.end()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            x = int(a0.pos().x() / self.grid_width_size)
            y = int(a0.pos().y() / self.grid_height_size)
            print(f"点击了位置：{(x, y)}")
            print(f"where{self.where}")
            print(f"if_can_eat{self.if_can_eat}")
            (old_x, old_y) = self.clicked_check

            # 1.如果点击的位置 能够下，那么下棋 并注意history
            if len(self.where) > 0 and (x, y) in self.where:
                transition_to_boss = False
                # 首先确保新点击位置为老位置的合法走子位置
                if self.board.board[self.board.my_color][old_x][old_y] == 2:
                    all_eat_situation = self.board.boss_position_can_move(old_x, old_y)[1]
                else:
                    all_eat_situation = self.board.position_can_move(old_x, old_y)[1]
                all_end_pos = [i[0] for i in all_eat_situation]
                if (x, y) in all_end_pos:
                    # 更改board
                    who_can_eat = None
                    if self.if_can_eat:
                        for tmp in all_eat_situation:
                            if tmp[0] == (x, y):
                                who_can_eat = tmp[1]
                        assert who_can_eat is not None, "吃子判定出错了"
                        # 这里需要进一步保证老位置为合理的吃子前位置
                        # 强制可以吃子时必须吃子
                        if len(who_can_eat) == 0:
                            return
                        flag1 = False
                        if self.board.board[self.board.my_color][old_x][old_y] == 1:
                            flag1 = True
                        self.board.eat(self.board.my_color, old_x, old_y, x, y, who_can_eat)
                        if flag1 and self.board.board[1 - self.board.my_color][x][y] == 2:
                            transition_to_boss = True
                    else:
                        flag1 = False
                        if self.board.board[self.board.my_color][old_x][old_y] == 1:
                            flag1 = True
                        self.board.player(self.board.my_color, old_x, old_y, x, y)
                        if flag1 and self.board.board[1 - self.board.my_color][x][y] == 2:
                            transition_to_boss = True

                    # 记录history 由于已经进行了 player eat操作 my_color已经发生了改变
                    if self.board.my_color == self.board.white_color:
                        self.history.append(("black", (old_x, old_y), (x, y), self.if_can_eat, who_can_eat))
                    else:
                        self.history.append(("white", (old_x, old_y), (x, y), self.if_can_eat, who_can_eat))
                    if transition_to_boss:
                        self.transition_history.append(self.count)
                    print("history更新为" + self.history.__str__())
                    self.count += 1
                    # # 重新设置计时器
                    # self.timer = QTimer(self)
                    # self.timer.timeout.connect(self.time_has_timeout)
                    # self.timer.start(self.time_can_hold)  # 先设置10秒
                    # 清空where ， clicked_check,
                    self.clicked_check = (-1, -1)
                    # 注意更改my_color  因为已经落子后，接着轮到对方下子
                    # self.board.my_color = 1 - self.board.my_color # 这一个操作应该再play eat unplay中做
                    if self.board.check_if_my_lose():
                        self.i_has_lost()
                        return
                    self.if_can_eat, self.end_list = self.board.getNextAction()
                    self.where = [tem[0] for tem in self.end_list]
                    # 重绘制
                    self.repaint()
                return

            # 2.如果不能下，那么如果此位置是一个 本方棋子，就重新更新clicked_check
            if self.board.board[self.board.my_color][x][y] != 0:
                print(f"此位置为{self.board.my_color}棋{(x, int(self.board.board_width_check_nums - 1 - y))}")

                self.clicked_check = (x, y)
                self.if_can_eat, self.end_list = self.board.getNextAction()
                print(f"此时对应吃子集合{self.end_list.__str__()}")
                self.where = [tem[0] for tem in self.end_list]

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

    def i_has_lost(self):
        """
        我方输掉
        """
        mssage = QMessageBox(self)
        mssage.setGeometry(0, 0, 500, 500)
        if self.board.my_color == self.board.white_color:
            mssage.setText(f"我方white棋输，黑棋胜")
        else:
            mssage.setText(f"我方black棋输，白棋胜")
        mssage.show()


    def goback_history(self):
        try:
            assert len(self.history) != 0, "游戏已恢复到最开始，无法再接着恢复"
        except Exception as e:
            print(e.__str__())
            print("游戏已经恢复到最开始状态，别点击啦")
            return

        self.count -= 1
        # 需要查看是否是王棋转变之际
        has_transit = False
        current_count = self.count
        if len(self.transition_history) > 0:
            record_count = self.transition_history.pop()
            if current_count == record_count:
                has_transit = True
            else:
                self.transition_history.append(record_count)

        color_str, (old_x, old_y), (x, y), is_eat, eaten_list = self.history.pop()
        if color_str == "white":
            color = self.board.white_color
        else:
            color = self.board.black_color
        if not is_eat:
            self.board.player_goback_history(color, old_x, old_y, x, y)
        else:
            self.board.eat_goback_history(color, old_x, old_y, x, y, eaten_list)
        # 不管是怎么变得王  都要回来
        if has_transit:
            self.board.board[color][old_x][old_y] = 1
            if color == self.board.white_color:
                self.board.white_boss_check.remove((old_x, old_y))
                self.board.white_color_check.add((old_x, old_y))
            else:
                self.board.black_boss_check.remove((old_x, old_y))
                self.board.black_color_check.add((old_x, old_y))

        # 更改后退后 注意下棋方改变
        self.clicked_check = (-1, -1)

        # self.board.my_color = 1 - self.board.my_color  此操作在悔棋un_player un_eat中进行
        self.if_can_eat, self.end_list = self.board.getNextAction()
        self.where = [tem[0] for tem in self.end_list]
        # 重绘制
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
