from os import name
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLabel, QComboBox
from PyQt5.uic import loadUi
import MySQLdb as mdb
from PyQt5.QtGui import QPixmap
import smtplib
import random
import math
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Login(QDialog):
    def __init__(self):

        super(Login, self).__init__()
        loadUi("./login.ui", self)
        self.loginpushbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.forgotpass.clicked.connect(self.gotopasswordreset)

    def loginfunction(self):
        try:
            name = self.name.text()
            password = self.password.text()
            db = mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
            cur = db.cursor()
            cur.execute(
                'SELECT * FROM userdata WHERE name= %s AND password = %s', (name, password,))
            result = cur.fetchone()
            if result == None:
                QMessageBox.about(self, 'Login', 'Incorrect Email/Password')
                # self.labelResult.setText("Incorrect Email/Password")
            else:
                QMessageBox.about(
                    self, 'Login',  "You are logged in successfully!")

                # self.labelResult.setText("You are logged in successfully!")
        except mdb.Error as e:
            QMessageBox.about(self, 'Login', "Sorry! something went wrong")
            # self.labelResult.setText("Error! something went wrong")

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotopasswordreset(self):
        passwordreset = Passwordreset()
        widget.addWidget(passwordreset)
        widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("./createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.loginpushbutton.clicked.connect(self.gotologin)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        try:
            email = self.email.text()
            name = self.name.text()
            password = self.password.text()
            phone = self.phone.text()
            dob = self.dob.text()
            gender = self.gender.currentText()

            db = mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
            cur = db.cursor()
            cur.execute(
                'SELECT * FROM userdata WHERE email= %s or name=%s', (email, name, ))
            result = cur.fetchone()
            if result:
                QMessageBox.about(self, 'register', 'Account already exist!')
            elif not name or not password or not email or not dob:
                QMessageBox.about(self, 'Register',
                                  'Please fill out the form properly !')
            elif self.password.text() == self.confirmpass.text():

                db = mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
                cur = db.cursor()
                cur.execute("INSERT INTO userdata(name,  email, password,phone,dob,gender) VALUES(%s, %s, %s,%s,%s,%s)",
                            (name, email, password, phone, dob, gender))
                db.commit()
                QMessageBox.about(self, 'Register',
                                  'You have registered successfully!')
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
                # self.labelResult.setText("Incorrect Email/Password")
            else:
                QMessageBox.about(self, 'Register',
                                  "your passwords didn't match!")

                # self.labelResult.setText("You are logged in successfully!")
        except mdb.Error as e:
            QMessageBox.about(self, 'Register', "Sorry! something went wrong")

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Passwordreset(QDialog):
    def __init__(self):
        super(Passwordreset, self).__init__()
        loadUi("./resetpass.ui", self)
        self.reset.clicked.connect(self.sendmailfunction)

    def sendmailfunction(self):
        global email
        #global OTP

        email = self.email.text()
        db = mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
        cur = db.cursor()
        cur.execute('SELECT * FROM userdata WHERE email= %s ', (email, ))
        result = cur.fetchone()
        if not email:
            QMessageBox.about(
                self, 'Resetpassword', "Invalid input,Please Enter string!!")
            
        elif result:
            digits = "0123456789"
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            otp = OTP
            msg = otp + " is your OTP!!  Do NOT share with anyone"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('apexinfotechexcellenceco@gmail.com', 'pass@1New')
            subject = "Reset Password OTP"
            body = msg
            message = f"Subject:{subject}\n\n{body}"
            s.sendmail('apexinfotechexcellenceco', email, message)

            QMessageBox.about(
                self, 'Resetpassword', "Please, check your mail,OTP is sent for password reset")
            # new=OTP
            new, notp = QtWidgets.QInputDialog.getText(
                self, 'OTP', 'Enter your OTP:')

            if new==OTP:

                QMessageBox.about(self, 'Resetpassword',
                                  " You Entered correct OTP !!")
                changepass = Changepass()
                widget.addWidget(changepass)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                QMessageBox.about(self, 'Resetpassword',
                              "Sorry you Entered incorrect OTP try again!!")
                passwordreset = Passwordreset()
                widget.addWidget(passwordreset)
                widget.setCurrentIndex(widget.currentIndex()+1)

        else:
            QMessageBox.about(self, 'Resetpassword',
                              "Please Enter valid Email-ID!!!!")


class Changepass(QDialog):
    def __init__(self):
        super(Changepass, self).__init__()
        loadUi("./changepass.ui", self)
        self.setpassword.clicked.connect(self.changepassfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def changepassfunction(self):
        password = self.password.text()
        if self.password.text() == self.confirmpass.text():

            db = mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
            cur = db.cursor()
            cur.execute("UPDATE userdata SET password=%s WHERE email=%s",
                        (password, email))
            db.commit()
            QMessageBox.about(self, 'Resetpassword',
                              'Your password reset successfully!')
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
            # self.labelResult.setText("Incorrect Email/Password")
        else:
            QMessageBox.about(self, 'Resetpassword',
                              "your passwords didn't match!")

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainwindow = Login()

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setStyleSheet("QDialog{\n"
                     "background-image:url(bgg.jpg)\n"
                     "}")
    widget.setFixedWidth(750)
    widget.setFixedHeight(750)
    widget.show()
    app.exec_()
