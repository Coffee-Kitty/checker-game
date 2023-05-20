import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
import numpy as np

class CheckerBoard(QWidget):

    white_color = 0  # 白方为0
    black_color = 1  # 黑方为1

    width_num = 10  # 棋盘宽为10
    height_num = 10  # 棋盘高为10

    def __init__(self, my_color=white_color, init_board=None):
        super().__init__()
        self.ui = uic.loadUi("../ui/a.ui")

        # 我方棋颜色
        self.my_color = my_color
        # 棋盘
        if init_board is not None:
            self.board = init_board
        else:
            # 如果没有提供初始棋盘 默认没开始 提供初始board
            self.board = np.zeros(shape=(2, self.width_num, self.height_num), dtype=np.int32)

            # 我方棋子永远在下面 !!!
            for x in range(10):
                for y in range(0, 4):
                    if (x + y) % 2 == 0:
                        self.board[self.my_color][x][y] = 1
            # 然后是敌方棋子
            for x in range(10):
                for y in range(6, 9+1):
                    if (x + y) % 2 == 0:
                        self.board[1 - self.my_color][x][y] = 1

        # 画出棋盘
        self.ui_init()

    def ui_init(self):
        for i in range(self.width_num):
            for j in range(self.height_num):
                label = getattr(self.ui, f"label{i}{j}")
                if self.board[self.white_color][i][j] == 1:
                    pix = QPixmap('../images/white_checker.png')
                elif self.board[self.black_color][i][j] == 1:
                    pix = QPixmap('../images/black_checker.png')
                elif (i + j) % 2 == 0:  # i+j 是偶数则为深色格子 否则为浅色格子
                    pix = QPixmap('../images/black_block.png')
                else:
                    pix = QPixmap('../images/white_block.png')

                assert pix is not None, "图像出现问题"
                label.setPixmap(pix)
                label.setScaledContents(True)
                label.repaint()


    def check_bound(self, color, x, y):
        """
        检查位置是否合法
        包括
            1. 新位置是否越界
            2. 新位置 x+y 是否为深色格子  只有深色格子可以行棋
            3. 新位置是否有其他棋子
        """
        assert 0 <= x <= self.width_num and 0 <= y <= self.height_num, f"位置{x},{y}越界"

        assert (x + y) % 2 == 0

        assert self.board[color][x][y] != 1, f"{(x, y)}位置棋子已经有{color}棋！，不能重复下{color}棋"
        enemy_color = 1 - color
        assert self.board[enemy_color][x][y] != 1, f"{(x, y)}位置棋子已经有{enemy_color}棋！，不能再下{color}棋"


    def player(self, color, old_x, old_y, new_x, new_y):
        self.check_bound(color, new_x, new_y)

        old_label = getattr(self.ui, f"label{old_x}{old_y}")
        new_label = getattr(self.ui, f"label{new_x}{new_y}")


        if (old_x + old_y) % 2 == 0:  # i+j 是偶数则为深色格子 否则为浅色格子
            pix = QPixmap('../images/black_block.png')
            old_label.setPixmap(pix)
        else:
            pix = QPixmap('../images/white_block.png')
            old_label.setPixmap(pix)
        old_label.repaint()

        if color == self.white_color:
            pix = QPixmap('../images/white_checker.png')
            new_label.setPixmap(pix)
        else:
            pix = QPixmap('../images/black_checker.png')
            new_label.setPixmap(pix)
        new_label.repaint()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    checker_board = CheckerBoard()
    checker_board.ui.show()

    app.exec_()