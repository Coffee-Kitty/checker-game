from PyQt5 import QtCore, QtGui, QtWidgets

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 注意 手动进行了修改  不是right_window.ui中的样子了
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Form.resize(203, 343)
        self.widget = QtWidgets.QWidget(Form)
        # self.widget.setGeometry(QtCore.QRect(0, 0, 197, 94))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.go_back_history_button = QtWidgets.QPushButton(self.widget)
        self.go_back_history_button.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.go_back_history_button)

        self.change_turn_button = QtWidgets.QPushButton(self.widget)
        self.change_turn_button.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.change_turn_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.time_edit = QtWidgets.QLineEdit(self.widget)
        self.time_edit.setObjectName("lineEdit")
        self.who_turn_edit = QtWidgets.QLineEdit(self.widget)
        self.who_turn_edit.setObjectName("lineEdit_2")
        # 先显示轮到谁走了，再显示计时
        self.verticalLayout.addWidget(self.who_turn_edit)
        self.verticalLayout.addWidget(self.time_edit)

        """
            再加一个记录log按钮便于调试
        """
        self.debug_button = QtWidgets.QPushButton(self.widget)
        self.debug_button.setObjectName("debug_button")
        self.verticalLayout.addWidget(self.debug_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.go_back_history_button.setText(_translate("Form", "悔棋"))
        self.change_turn_button.setText(_translate("Form", "交换落子方"))
        self.time_edit.setText(_translate("Form", "计时:   "))
        self.who_turn_edit.setText(_translate("Form", ""))
        self.debug_button.setText(_translate("Form", "记录log日志"))


