import numpy as np

from checkers.src.checker_board import CheckerBoard
from checkers.src.mode_enumerate import Three_Mode


def load_board_drawBoard(load_board: str, mode: Three_Mode) -> CheckerBoard:
    """
    加载这样的board：
    1, 0, 0, ... 10,(注意末尾有空格和换行)
    （最后一行末尾就不要换行了）
    请先给出white棋，再给出black棋


    总体思路：首先根据不同的mode解析出相同的black和white棋盘
    然后根据black，white棋盘最好CheckerBoard类的使用即可
    """
    board = CheckerBoard(CheckerBoard.board_width_check_nums, CheckerBoard.board_height_check_nums,
                         CheckerBoard.white_color)
    black, white = [], []
    lines = load_board.split("\n")
    if mode == Three_Mode.mode1_i_j_transition:
        for num, line in enumerate(lines):
            if num >= board.board_height_check_nums:
                tem = []
                cur_line = line.split(", ")
                for i, cur in enumerate(cur_line):
                    if i >= board.board_height_check_nums:
                        continue
                    tem.append(int(cur))
                black.append(tem)
            else:
                tem = []
                cur_line = line.split(", ")
                for i, cur in enumerate(cur_line):
                    if i >= board.board_height_check_nums:
                        continue
                    tem.append(int(cur))
                white.append(tem)
    # elif mode == Three_Mode.mode2_OneToN_transition:
    #     for num, line in enumerate(lines):
    #         if num >= board.board_height_check_nums:
    #             tem = []
    #             cur_line = line.split(", ")
    #             for i, cur in enumerate(cur_line):
    #                 if i >= board.board_height_check_nums:
    #                     continue
    #                 tem.append(int(cur))
    #             black.append(tem)
    #         else:
    #             tem = []
    #             cur_line = line.split(", ")
    #             for i, cur in enumerate(cur_line):
    #                 if i >= board.board_height_check_nums:
    #                     continue
    #                 tem.append(int(cur))
    #             white.append(tem)
    # 然后根据black，white棋盘最好CheckerBoard类的使用
    board.board = np.zeros(shape=(2, board.board_width_check_nums, board.board_height_check_nums), dtype=np.int32)
    board.black_boss_check.clear()
    board.black_color_check.clear()
    board.white_boss_check.clear()
    board.white_color_check.clear()
    for i in range(board.board_width_check_nums):
        for j in range(board.board_height_check_nums):
            if white[i][j] == 1:
                board.board[board.white_color][i][j] = 1
                board.white_color_check.add((i, j))
            elif white[i][j] == 2:
                board.board[board.white_color][i][j] = 2
                board.white_boss_check.add((i, j))
            elif black[i][j] == 1:
                board.board[board.black_color][i][j] = 1
                board.black_color_check.add((i, j))
            elif black[i][j] == 2:
                board.board[board.black_color][i][j] = 2
                board.black_boss_check.add((i, j))
    return board
