import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from pyqt5_plugins.examplebuttonplugin import QtGui

from checkers.src.checker_board import CheckerBoard
from checkers.src.checker_board_widget import CheckerBoardWidget
from checkers.ui.right_window import Ui_Form


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.startX = 0
        self.startY = 0
        self.widget_width_size = 1200
        self.widget_height_size = 800
        self.setGeometry(self.startX, self.startY, self.widget_width_size, self.widget_height_size)

        layout = QHBoxLayout()
        # 首先左侧是棋盘
        self.checker_board_widget = CheckerBoardWidget(
            board=CheckerBoard(CheckerBoard.board_width_check_nums, CheckerBoard.board_height_check_nums,
                               CheckerBoard.white_color))
        self.checker_board_widget.setParent(self)

        # 然后右侧按钮
        self.right_widget = QWidget()
        right_ui = Ui_Form()
        right_ui.setupUi(self.right_widget)
        self.right_widget.setParent(self)

        self.right_widget.wid = 200
        self.right_widget.hei = 800
        self.right_widget.setGeometry(self.checker_board_widget.widget_width_size, 0, self.right_widget.wid,
                                      self.right_widget.hei)

    def resizeEvent(self, a0: QResizeEvent) -> None:


        # a1 = QResizeEvent(
        #     QSize(a0.size().width() - self.right_widget.wid, a0.size().height()),
        #     a0.oldSize())
        # 新的窗口大小
        (new_wid, new_hei) = a0.size().width(), a0.size().height()
        # 如果棋盘不是正方形会出错误
        if new_hei != new_wid-200:
            new_hei = min(new_wid-200, new_hei)
            new_wid = new_hei+200
        print(f"{(new_wid,new_hei)}")
        # 设置棋盘缩放
        self.checker_board_widget.widget_width_size = new_wid-200
        self.checker_board_widget.widget_height_size = new_hei

        # 一个棋子的格子的宽高
        self.checker_board_widget.grid_width_size = self.checker_board_widget.widget_width_size / self.checker_board_widget.board.board_width_check_nums
        self.checker_board_widget.grid_height_size = self.checker_board_widget.widget_height_size / self.checker_board_widget.board.board_height_check_nums
        self.checker_board_widget.setGeometry(self.checker_board_widget.startX,self.checker_board_widget.startY,self.checker_board_widget.widget_width_size,self.checker_board_widget.widget_height_size)

        # 设置右侧按钮缩放
        self.right_widget.wid = 200
        self.right_widget.hei = new_hei
        self.right_widget.setGeometry(self.checker_board_widget.widget_width_size, 0, self.right_widget.wid,
                                      self.right_widget.hei)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
