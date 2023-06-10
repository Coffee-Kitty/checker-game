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
    elif mode == Three_Mode.mode2_OneToN_transition:
        """
        white:99,87\n
        white_boss:9\n
        black:0\n
        black_boss:91
        """
        for i in range(CheckerBoard.board_width_check_nums):
            tem1 = []
            tem2 = []
            for j in range(CheckerBoard.board_height_check_nums):
                tem1.append(0)
                tem2.append(0)
            black.append(tem1)
            white.append(tem2)

        for num, line in enumerate(lines):
            if num == 0:
                line = line.replace("white:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    cur = int(cur)
                    # 11 - > (1,1)
                    pos_X = int(cur / CheckerBoard.board_width_check_nums)
                    pos_Y = int(cur % CheckerBoard.board_height_check_nums)
                    white[pos_X][pos_Y] = 1
            elif num == 1:
                line = line.replace("white_boss:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    cur = int(cur)
                    # 11 - > (1,1)
                    pos_X = int(cur / CheckerBoard.board_width_check_nums)
                    pos_Y = int(cur % CheckerBoard.board_height_check_nums)
                    white[pos_X][pos_Y] = 2
            elif num == 2:
                line = line.replace("black:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    cur = int(cur)
                    # 11 - > (1,1)
                    pos_X = int(cur / CheckerBoard.board_width_check_nums)
                    pos_Y = int(cur % CheckerBoard.board_height_check_nums)
                    black[pos_X][pos_Y] = 1
            elif num == 3:
                line = line.replace("black_boss:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    cur = int(cur)
                    # 11 - > (1,1)
                    pos_X = int(cur / CheckerBoard.board_width_check_nums)
                    pos_Y = int(cur % CheckerBoard.board_height_check_nums)
                    black[pos_X][pos_Y] = 2
    else:
        for i in range(CheckerBoard.board_width_check_nums):
            tem1 = []
            tem2 = []
            for j in range(CheckerBoard.board_height_check_nums):
                tem1.append(0)
                tem2.append(0)
            black.append(tem1)
            white.append(tem2)

        for num, line in enumerate(lines):
            if num == 0:
                line = line.replace("white:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    pos_X = ord(cur[0]) - 65
                    pos_Y = ord(cur[1]) - 65
                    white[pos_X][pos_Y] = 1
            elif num == 1:
                line = line.replace("white_boss:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    pos_X = ord(cur[0]) - 65
                    pos_Y = ord(cur[1]) - 65
                    white[pos_X][pos_Y] = 2
            elif num == 2:
                line = line.replace("black:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    pos_X = ord(cur[0]) - 65
                    pos_Y = ord(cur[1]) - 65
                    black[pos_X][pos_Y] = 1
            elif num == 3:
                line = line.replace("black_boss:", "")
                cur_line = line.split(",")
                for i, cur in enumerate(cur_line):
                    pos_X = ord(cur[0]) - 65
                    pos_Y = ord(cur[1]) - 65
                    black[pos_X][pos_Y] = 2
    # 然后根据black，white棋盘最好CheckerBoard类的使用
    board.board = np.zeros(shape=(2, board.board_width_check_nums, board.board_height_check_nums), dtype=np.int32)
    board.black_boss_check.clear()
    board.black_color_check.clear()
    board.white_boss_check.clear()
    board.white_color_check.clear()
    for i in range(board.board_width_check_nums):
        for j in range(board.board_height_check_nums):
            if white[i][j] == 1:
                board.board[board.white_color][i][board.board_width_check_nums-1-j] = 1
                board.white_color_check.add((i, board.board_width_check_nums-1-j))
            elif white[i][j] == 2:
                board.board[board.white_color][i][board.board_width_check_nums-1-j] = 2
                board.white_boss_check.add((i, board.board_width_check_nums-1-j))
            elif black[i][j] == 1:
                board.board[board.black_color][i][board.board_width_check_nums-1-j] = 1
                board.black_color_check.add((i, board.board_width_check_nums-1-j))
            elif black[i][j] == 2:
                board.board[board.black_color][i][board.board_width_check_nums-1-j] = 2
                board.black_boss_check.add((i, board.board_width_check_nums-1-j))
    return board
