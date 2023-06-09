import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit

if __name__ == "__main__":
     app = QApplication(sys.argv)


     w = QWidget()

     # 在窗口中添加控件 并将其添加到窗口中显示
     btn = QPushButton("按钮1")
     btn.setParent(w)
     btn.setGeometry(50,50,60,60)


     label = QLabel("直接设置parent",w)
     label.setGeometry(20,20,30,30) # 设置 位置 宽高


     edit = QLineEdit(w)
     edit.setPlaceholderText("请输入文本")
     edit.setGeometry(55,20,200,20)



     w.show()

     app.exec_()