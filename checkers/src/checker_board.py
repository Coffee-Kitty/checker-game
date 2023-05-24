import copy

import numpy as np


class CheckerBoard(object):

    white_color = 0  # 白方为0
    black_color = 1  # 黑方为1
    width = 10  # 棋盘宽为10   国跳100
    height = 10  # 棋盘高为10   国跳100
    start_row = 4  # 每方拥有的棋子所占行数  如国跳100占据4行   国跳64占据3行

    checker_width = 80
    checker_height = 80

    def __init__(self, width: int, height: int, my_color: int, init_board=None):
        """
        初始化棋盘   如果init_board不为None   则给予那时棋盘状态
        """
        self.width = width
        self.height = height
        self.my_color = my_color  # 当前轮到my_color走棋

        if init_board is not None:
            self.board = init_board
        else:
            # 如果没有提供初始棋盘 默认没开始 提供初始board
            self.board = np.zeros(shape=(2, self.width, self.height), dtype=np.int32)

            # 我方棋子永远在下面 !!!
            for x in range(self.width):
                for y in range(0, self.start_row):
                    if (x + y) % 2 == 0:
                        self.board[self.my_color][x][y] = 1
            # 然后是敌方棋子
            for x in range(self.width):
                for y in range(self.height-self.start_row, self.height):
                    if (x + y) % 2 == 0:
                        self.board[1 - self.my_color][x][y] = 1


    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        pass

