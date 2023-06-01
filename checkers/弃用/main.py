from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
import sys
import numpy as np


class CheckerWidget(QWidget):

    white_color = 0  # 白方为0
    black_color = 1  # 黑方为1

    def __init__(self, width_num, height_num, my_color=white_color, init_board=None):
        """
          注意 width 和 height指的是 棋盘是 n*n的
        """
        super().__init__()
        # 棋盘中每个格子的大小
        self.widthSize = 80
        self.heightSize = 80
        # 我方棋颜色
        self.my_color = my_color
        # 棋盘
        if init_board is not None:
            self.board = init_board
        else:
            self.board = np.zeros(shape=(2, width_num, height_num), dtype=np.int32)
            enenmy_end = int(height_num / 2 - 1)
            my_start = enenmy_end + 1
            for x in range(0, enenmy_end):
                for y in range(width_num):
                    if (x+y) % 2 == 1:
                        self.board[1-self.my_color][x][y] = 1
            for x in range(my_start+1, height_num):
                for y in range(width_num):
                    if (x + y) % 2 == 1:
                        self.board[self.my_color][x][y] = 1

        self.ui_init(width_num, height_num)



    def ui_init(self, width_num, height_num):
        """
        初始化棋盘,并根据 棋子位置进行调用player方法下棋
        """
        assert width_num == height_num, "棋盘宽高不相等"

        position = (0, 0)
        self.setGeometry(position[0], position[1],  self.widthSize*width_num, self.heightSize*height_num)

        # 创建网格布局
        gridLayOut = QGridLayout()
        gridLayOut.setSpacing(0)  # 设置格子之间间隔为0

        # 准备三种不同颜色的格子
        for i in range(width_num):
            for j in range(height_num):
                label = QLabel()

                if self.board[self.white_color][i][j] == 1:
                    pix = QPixmap('images/white_checker.png')
                elif self.board[self.black_color][i][j] == 1:
                    pix = QPixmap('images/black_checker.png')
                elif (i+j) % 2 == 0:  # i+j 是偶数则为浅色格子 否则为深色格子
                    pix = QPixmap('images/white_block.png')
                else:
                    pix = QPixmap('images/black_block.png')

                assert pix is not None, "图像出现问题"
                label.setPixmap(pix)
                label.setScaledContents(True)

                gridLayOut.addWidget(label, i, j)

        self.setLayout(gridLayOut)


    def check_bound(self, color, x, y):
        """
        检查位置是否合法
        """
        assert self.board[color][x][y] != 1, f"{(x,y)}位置棋子已经有{color}棋！，不能重复下{color}棋"
        enemy_color = 1 - color
        assert self.board[enemy_color][x][y] != 1, f"{(x,y)}位置棋子已经有{enemy_color}棋！，不能再下{color}棋"






if __name__ == "__main__":
    app = QApplication(sys.argv)


    checkers_board = CheckerWidget(10, 10)
    checkers_board.show()


    app.exec_()