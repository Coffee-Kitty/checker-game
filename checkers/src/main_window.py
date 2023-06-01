import sys

from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QMessageBox
from pyqt5_plugins.examplebuttonplugin import QtGui

from checkers.src.checker_board import CheckerBoard
from checkers.src.checker_board_widget import CheckerBoardWidget
from checkers.ui.right_window import Ui_Form


class MainWindow(QMainWindow):
    time_can_hold = 100000  # 100秒

    def __init__(self):
        super().__init__()
        self.startX = 0
        self.startY = 0
        self.widget_width_size = 1200
        self.widget_height_size = 800
        self.setGeometry(self.startX, self.startY, self.widget_width_size, self.widget_height_size)

        # 左侧是棋盘
        self.checker_board_widget = CheckerBoardWidget(
            board=CheckerBoard(CheckerBoard.board_width_check_nums, CheckerBoard.board_height_check_nums,
                               CheckerBoard.white_color))
        self.checker_board_widget.setParent(self)

        # 右侧按钮
        self.right_widget = QWidget()
        self.right_ui = Ui_Form()
        self.right_ui.setupUi(self.right_widget)
        self.right_widget.setParent(self)

        self.right_widget.wid = 200
        self.right_widget.hei = 800
        self.right_widget.setGeometry(self.checker_board_widget.widget_width_size, 0, self.right_widget.wid,
                                      self.right_widget.hei)
        self.right_ui.go_back_history_button.clicked.connect(self.go_back_history_clicked)



        # 计时器
        self.timer = QTimer(self)
        # 超时绑定的槽函数
        self.timer.timeout.connect(self.time_has_timeout)
        # 达到指定时间触发一次的槽函数
        self.timer.singleShot(10, self.timer_show)
        self.timer.start(self.time_can_hold)  # 先设置10秒
        self.count = 0  # 记录已知的history长度

    def timer_show(self):
        # 如果棋盘中有人下棋了，下棋方发生改变了，则重新开始计时
        if len(self.checker_board_widget.history) > self.count:
            self.count = len(self.checker_board_widget.history)
            # 然后重置定时器
            self.timer.stop()
            # 计时器
            self.timer = QTimer(self)
            # 超时绑定的槽函数
            self.timer.timeout.connect(self.time_has_timeout)
            # 达到指定时间触发一次的槽函数
            self.timer.singleShot(10, self.timer_show)
            self.timer.start(self.time_can_hold)  # 先设置10秒

        self.right_ui.time_edit.clear()
        if self.checker_board_widget.board.my_color == self.checker_board_widget.board.black_color:
            self.right_ui.time_edit.setText(f"黑棋 剩余时间{self.timer.remainingTime().__str__()}毫秒")
        else:
            self.right_ui.time_edit.setText(f"白棋 剩余时间{self.timer.remainingTime().__str__()}毫秒")
        # 重新触发即可
        self.timer.singleShot(10, self.timer_show)

    def time_has_timeout(self):
        """
        到时间后返回对方胜利即可
        """
        print("超时了")
        mssage = QMessageBox(self)
        mssage.setGeometry(0, 0, 500, 500)
        if self.checker_board_widget.board.my_color == self.checker_board_widget.board.white_color:
            mssage.setText(f"white棋 超时了，黑棋胜")
        else:
            mssage.setText(f"black棋超时了，白棋胜")
        # 关闭定时器
        self.timer.stop()
        mssage.show()

    def resizeEvent(self, a0: QResizeEvent) -> None:

        # a1 = QResizeEvent(
        #     QSize(a0.size().width() - self.right_widget.wid, a0.size().height()),
        #     a0.oldSize())
        # 新的窗口大小
        (new_wid, new_hei) = a0.size().width(), a0.size().height()
        # 如果棋盘不是正方形会出错误
        if new_hei != new_wid - 200:
            new_hei = min(new_wid - 200, new_hei)
            new_wid = new_hei + 200
        print(f"{(new_wid, new_hei)}")
        # 设置棋盘缩放
        self.checker_board_widget.widget_width_size = new_wid - 200
        self.checker_board_widget.widget_height_size = new_hei

        # 一个棋子的格子的宽高
        self.checker_board_widget.grid_width_size = self.checker_board_widget.widget_width_size / self.checker_board_widget.board.board_width_check_nums
        self.checker_board_widget.grid_height_size = self.checker_board_widget.widget_height_size / self.checker_board_widget.board.board_height_check_nums
        self.checker_board_widget.setGeometry(self.checker_board_widget.startX, self.checker_board_widget.startY,
                                              self.checker_board_widget.widget_width_size,
                                              self.checker_board_widget.widget_height_size)

        # 设置右侧按钮缩放
        self.right_widget.wid = 200
        self.right_widget.hei = new_hei
        self.right_widget.setGeometry(self.checker_board_widget.widget_width_size, 0, self.right_widget.wid,
                                      self.right_widget.hei)

    def go_back_history_clicked(self):
        self.checker_board_widget.goback_history()
        # 悔棋后得重新计算时间
        self.timer.stop()
        # 计时器
        self.timer = QTimer(self)
        # 超时绑定的槽函数
        self.timer.timeout.connect(self.time_has_timeout)
        # 达到指定时间触发一次的槽函数
        self.timer.singleShot(10, self.timer_show)
        self.timer.start(self.time_can_hold)  # 先设置10秒

        # 并且注意记录的history的长度减一
        self.count -= 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
