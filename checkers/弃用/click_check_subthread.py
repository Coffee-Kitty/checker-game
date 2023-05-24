from PyQt5.QtCore import QThread

from checkers.弃用.checker_board import CheckerBoard


class CheckerThread(QThread):
    """
    输入该棋子位置
    恢复棋盘状态
    然后将该棋子可下位置标红
    """
    def __init__(self, color, old_x, old_y, check_board:CheckerBoard):
        super().__init__()
        self.color = color
        self.old_x = old_x
        self.old_y = old_y
        self.checker_board = check_board

    def where_can_player(self, color) -> set:
        """
        返回该棋子可下的位置
        """
        where = set()
        dire = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        if self.checker_board.board[color][self.old_x][self.old_y] == 1:
            for pos in dire:
                if self.checker_board.check_position_can_player(color, pos[0] + self.old_x, pos[1] + self.old_y):
                    where.add((pos[0] + self.old_x, pos[1] + self.old_y))
        return where

    def run(self) -> None:
        self.checker_board.ui_init()
        where = self.where_can_player(self.color)
        for pos in where:
            self.checker_board.player(self.color, self.old_x, self.old_y, pos[0], pos[1])














