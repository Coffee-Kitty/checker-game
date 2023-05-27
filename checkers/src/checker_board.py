import copy

import numpy as np


class CheckerBoard(object):
    white_color = 0  # 白方为0
    black_color = 1  # 黑方为1
    board_width_check_nums = 10  # 棋盘宽为10   国跳100
    board_height_check_nums = 10  # 棋盘高为10   国跳100
    start_row = 4  # 每方拥有的棋子所占行数  如国跳100占据4行   国跳64占据3行



    # def transition_to_drawboard(self):
    #     """
    #     对于此 0，0 位置
    #     由于硬性要求  需要更改为  x,y -> x,9-y
    #     """
    #     new_checker_board = CheckerBoard(self.width, self.height, self.my_color, None)
    #     new_checker_board.board = np.zeros(shape=(2, self.width, self.height), dtype=np.int32)
    #     for i in range(new_checker_board.width):
    #         for j in range(new_checker_board.height):
    #             if self.board[self.white_color][i][j] == 1:
    #                 new_checker_board.board[self.white_color][i][new_checker_board.height - 1 - j] = 1
    #             elif self.board[self.black_color][i][j] == 1:
    #                 new_checker_board.board[self.black_color][i][new_checker_board.height - 1 - j] = 1
    #     return new_checker_board

    def __init__(self, width: int, height: int, my_color=white_color, init_board=None):
        """
        初始化棋盘   如果init_board不为None   则给予那时棋盘状态
        """
        self.board_width_check_nums = width
        self.board_height_check_nums = height
        self.my_color = my_color  # 当前轮到my_color走棋

        if init_board is not None:
            self.board = init_board
        else:
            # 如果没有提供初始棋盘 默认没开始 提供初始board
            self.board = np.zeros(shape=(2, self.board_width_check_nums, self.board_height_check_nums), dtype=np.int32)

            for x in range(self.board_width_check_nums):
                for y in range(0, self.start_row):
                    if (x + y) % 2 == 1:
                        self.board[self.black_color][x][y] = 1

            for x in range(self.board_width_check_nums):
                for y in range(self.board_height_check_nums - self.start_row, self.board_height_check_nums):
                    if (x + y) % 2 == 1:
                        self.board[self.white_color][x][y] = 1

    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        pass

    def show_board(self):
        for i in range(self.board_width_check_nums):
            for j in range(self.board_height_check_nums):
                if self.board[self.white_color][i][j] == 1:
                    print(f"white{(i,j)}",end='\t')
                elif self.board[self.black_color][i][j] == 1:
                    print(f"black{(i,j)}",end='\t')
                else:
                    print(f"empty{(i,j)}",end='\t')
            print(end='\n')