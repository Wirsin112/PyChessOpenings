from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton, QLineEdit, QMainWindow
import sys
from src.Client.menu import Menu

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyChess"
        self.top = 500
        self.left = 500
        self.width = 500
        self.height = 400
        self.login = True
        self.log_show_bool = True
        self.reg_show_bool = True
        self.InitWindow_login()
        self.InitWindow_register()

    def InitWindow_login(self):
        self.log_text = QLabel(self)
        self.log_text.setText("Username")
        self.log_text.setFont(QFont('Arial', 20))
        self.log_text.setGeometry(50, 90, 400, 40)

        self.pas_text = QLabel(self)
        self.pas_text.setText("Password")
        self.pas_text.setFont(QFont('Arial', 20))
        self.pas_text.setGeometry(50, 190, 400, 40)

        self.in_login = QLineEdit(self)
        self.in_login.setGeometry(50, 125, 400, 25)

        self.in_register = QLineEdit(self)
        self.in_register.setEchoMode(2)
        self.in_register.setGeometry(50, 225, 350, 25)

        self.log_reg = QPushButton("Login", self)
        self.log_reg.setGeometry(50, 300, 400, 50)
        self.log_reg.setStyleSheet("background-color: white")
        self.log_reg.clicked.connect(self.Switch_to_menu)

        self.log_button = QPushButton("Login", self)
        self.log_button.setGeometry(150, 25, 100, 50)
        self.log_button.setStyleSheet("background-color: grey")
        self.log_button.clicked.connect(self.Switch_reg_log)

        self.reg_button = QPushButton("Register", self)
        self.reg_button.setGeometry(250, 25, 100, 50)
        self.reg_button.clicked.connect(self.Switch_log_reg)
        self.reg_button.setStyleSheet("background-color: white")

        self.log_show = QPushButton("show", self)
        self.log_show.setGeometry(400, 225, 50, 25)
        self.log_show.clicked.connect(self.Show_hide_log_pass)
        self.log_show.setStyleSheet("background-color: white")

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def InitWindow_register(self):
        self.user_text = QLabel(self)
        self.user_text.setText("Username")
        self.user_text.setFont(QFont('Arial', 20))
        self.user_text.setGeometry(50, 70, 400, 40)

        self.mail_text = QLabel(self)
        self.mail_text.setText("E-mail")
        self.mail_text.setFont(QFont('Arial', 20))
        self.mail_text.setGeometry(50, 140, 400, 40)

        self.pasw_text = QLabel(self)
        self.pasw_text.setText("Password")

        self.pasw_text.setFont(QFont('Arial', 20))
        self.pasw_text.setGeometry(50, 210, 400, 40)

        self.in_user = QLineEdit(self)
        self.in_user.setGeometry(50, 110, 400, 25)

        self.in_mail = QLineEdit(self)
        self.in_mail.setGeometry(50, 180, 400, 25)

        self.in_passwrod = QLineEdit(self)
        self.in_passwrod.setGeometry(50, 250, 350, 25)
        self.in_passwrod.setEchoMode(2)

        self.reg_show = QPushButton("Show", self)
        self.reg_show.setGeometry(400, 250, 50, 25)
        self.reg_show.clicked.connect(self.Show_hide_reg_pass)
        self.reg_show.setStyleSheet("background-color: white")

    def Switch_log_reg(self):
        if self.login == True:
            self.login = False
            self.log_text.hide()
            self.pas_text.hide()
            self.in_login.hide()
            self.in_register.hide()
            self.log_show.hide()
            self.log_button.setStyleSheet("background-color: white")
            self.reg_button.setStyleSheet("background-color: grey")
            self.log_reg.setText("Register")

            self.user_text.show()
            self.mail_text.show()
            self.pasw_text.show()
            self.in_user.show()
            self.in_mail.show()
            self.in_passwrod.show()
            self.reg_show.show()

    def Switch_reg_log(self):
        if self.login == False:
            self.login = True
            self.user_text.hide()
            self.mail_text.hide()
            self.pasw_text.hide()
            self.in_user.hide()
            self.in_mail.hide()
            self.reg_show.hide()
            self.in_passwrod.hide()
            self.log_button.setStyleSheet("background-color: grey")
            self.reg_button.setStyleSheet("background-color: white")
            self.log_reg.setText("Login")

            self.log_text.show()
            self.pas_text.show()
            self.in_login.show()
            self.in_register.show()
            self.log_show.show()

    def Show_hide_log_pass(self):
        if self.log_show_bool:
            self.log_show_bool = not self.log_show_bool
            self.in_register.setEchoMode(0)
            self.log_show.setText("Hide")
        else:
            self.log_show_bool = not self.log_show_bool
            self.in_register.setEchoMode(2)
            self.log_show.setText("Show")

    def Show_hide_reg_pass(self):
        if self.reg_show_bool:
            self.reg_show_bool = not self.reg_show_bool
            self.in_passwrod.setEchoMode(0)
            self.reg_show.setText("Hide")
        else:
            self.reg_show_bool = not self.reg_show_bool
            self.in_passwrod.setEchoMode(2)
            self.reg_show.setText("Show")
    def Switch_to_menu(self):
        self.a = Menu()
        self.a.show()
        self.hide()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Login()
    sys.exit(App.exec())