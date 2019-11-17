# This Python file uses the following encoding: utf-8

Password = 'Sunlabi001.'
import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import pymysql
from PyQt5.uic import loadUiType

page ,_ = loadUiType('timetable.ui')
createuser ,_ = loadUiType('registerUser.ui')
loginMain ,_ = loadUiType('login.ui')

#### Main Class #####


class LogMeIn(QWidget, loginMain):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.LoginFunc)

    def LoginFunc(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )

        self.cur=self.db.cursor()

        usernme = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM users '''
        self.cur.execute(sql)
        dbb = self.cur.fetchall()
        for i in dbb:
            if usernme == i[1] and password == i[4]:
                self.window = MainApp()
                self.window.show()
                self.close()

            else:
                self.label.setText('Please Check Your Login Details')




class MainApp(QMainWindow, page):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handled_Button()
        self.tabWidget.tabBar().setVisible(False)
        self.showgenerateTimetable()
        self.pushButton.clicked.connect(self.searchClass)

#####################################
### Function for handling Buttons ##
####################################

    def Handled_Button(self):
        self.actionCreate_New_Users.triggered.connect(self.addUserClass)
        self.actionEdit_New_User.triggered.connect(self.editUser)
        self.actionDelete_User.triggered.connect(self.editUser)   #self.editUser
        self.actionAdde_New_Teacher.triggered.connect(self.addteacherclass)
        self.actionEdit_Techer.triggered.connect(self.editTeachers)
        self.actionDelete_Teacher.triggered.connect(self.editTeachers)
        self.actionAdd_Subject.triggered.connect(self.SubjectShow)
        self.actionDelete_Subject.triggered.connect(self.showeditsubject)
        self.actionEdit_Subject.triggered.connect(self.showeditsubject)
        self.actionQuit.triggered.connect(self.quitApp)
        self.actionAdd_Class_2.triggered.connect(self.showAddClass)


    def quitApp(self):
        warning = QMessageBox.warning(self, 'QUIT APP', 'Are you sure you want to Exit this app?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sys.exit()
        else:
            pass
    

    def addUserClass(self):
        self.window2 = UserReg()
        self.window2.show()
    def editUser(self):
        self.window =EditUsers()
        self.window.show()

    def addteacherclass(self):
        self.window=AddNewTeacher()
        self.window.show()
        
    def editTeachers(self):
        self.window = EditTeachersMain()
        self.window.show()

    def SubjectShow(self):
        self.window = SubjectMain()
        self.window.show()
    def showeditsubject(self):
        self.window = EditDeleteSubject()
        self.window.show()

    def showAddClass(self):
        self.window = createClass()
        self.window.show()


    
######################################################
###### TABLE WIDEGT ##############################

    def showgenerateTimetable(self):
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )

        self.cur=self.db.cursor()        
        self.cur.execute(' SELECT classname FROM class')
        DBB =self.cur.fetchall()
                
        for i in DBB:
            self.comboBox.addItem(str(i[0]))
            self.comboBox_2.addItem(str(i[5]))

    def searchClass(self):
        searchId = self.comboBox.currentText()
        searchday = self.comboBox_2.currentText()
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )

        self.cur=self.db.cursor()

        
        SQL = '''SELECT subjectname, teacher_taken_subject, class_taken_subject, period_of_subject, days_for_subject FROM subject WHERE class_taken_subject=%s AND days_for_subject=%s'''
        self.cur.execute(SQL, [searchId,  searchday])
        DBB = self.cur.fetchall()
        for row, form in enumerate(DBB):
            for colum , item in enumerate(form):
                self.tableWidget.setItem(row, colum, QTableWidgetItem(str(item)))
                colum += 1
                self.label.setText('TimeTable For ' + searchId + ' Today ' + searchday)

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

        self.db.close()

######### Add Class ##########
AddClass , _ = loadUiType("addClass.ui")

class createClass(QWidget, AddClass):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)



####################################################
### Subject Class to Add Subject to class ##########
####################################################


subjectclass ,_ =loadUiType('addSubject.ui')

class SubjectMain(QWidget, subjectclass):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.show()
        self.pushButton.clicked.connect(self.add_subject)

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',)
        self.cur = self.db.cursor()

        self.cur.execute(' SELECT teachername FROM teachers')
        DBB =self.cur.fetchall()
        
        for i in DBB:
            self.comboBox_2.addItem(str(i[0]))

    def add_subject(self):
        names = self.comboBox.currentText()
        teacher = self.comboBox_2.currentText()
        classsub = self.comboBox_3.currentText()
        days = self.comboBox_4.currentText()
        period = self.comboBox_5.currentText()

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',)
        self.cur = self.db.cursor()

        self.cur = self.db.cursor()
        self.cur.execute(''' INSERT INTO subject (subjectname, teacher_taken_subject, class_taken_subject, period_of_subject, days_for_subject)
        VALUES (%s, %s, %s, %s, %s)''', (names, teacher, classsub, period, days))

        self.db.commit()
        self.db.close()
        self.close()


editsubject ,_ = loadUiType('editDeleteSubject.ui')

class EditDeleteSubject(QWidget, editsubject):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.searchSubject)
        self.pushButton.clicked.connect(self.deletesubject)
        self.pushButton_2.clicked.connect(self.editsubject)

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',)
        self.cur = self.db.cursor()

        self.cur.execute(' SELECT subjectname FROM subject')
        DBB =self.cur.fetchall()        
        for i in DBB:
            self.comboBox.addItem(str(i[0]))
 

    def searchSubject(self):
        subjectSearch = self.comboBox.currentText()
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )

        self.cur=self.db.cursor()
        self.cur.execute('SELECT * FROM subject WHERE subjectname = %s', subjectSearch )
        DBB = self.cur.fetchall()

        for dat in DBB:
            self.comboBox_7.setCurrentText(dat[1])
            self.comboBox_9.setCurrentText(dat[2])
            self.comboBox_10.setCurrentText(dat[3])
            self.comboBox_6.setCurrentText(dat[5])
            self.comboBox_8.setCurrentText(dat[4])

    def deletesubject(self):
        deletesub = self.comboBox_7.currentText() 
        self.cur = self.db.cursor()
        warning = QMessageBox.warning(self, 'Delete subject', 'Are you sure you want to delete this User?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('DELETE FROM subject WHERE subjectname = %s ', deletesub )
            self.db.commit()
            self.comboBox_7.setCurrentText(str(0))
            self.comboBox_9.setCurrentText(str(0))
            self.comboBox_10.setCurrentText(str(0))
            self.comboBox_6.setCurrentText(str(0))
            self.comboBox_8.setCurrentText(str(0))
            self.close()

    def editsubject(self):
        saveId = self.comboBox.currentText()

        subjectname = self.comboBox_7.currentText()
        teachersname = self.comboBox_9.currentText()
        classsubject = self.comboBox_10.currentText()
        daysofweek = self.comboBox_6.currentText()
        period = self.comboBox_8.currentText()

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',)

        self.cur = self.db.cursor()
        warning = QMessageBox.warning(self, 'Edit subject', 'Are you sure you want to Edit this Subject?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''
                UPDATE subject SET subjectname=%s, teacher_taken_subject=%s, class_taken_subject=%s, period_of_subject=%s, days_for_subject=%s WHERE subjectname=%s ''',
                (subjectname, teachersname, classsubject, period, daysofweek, saveId))
            self.db.commit()
            self.db.close()
            
            self.comboBox_7.setCurrentText(str(0))
            self.comboBox_9.setCurrentText(str(0))
            self.comboBox_10.setCurrentText(str(0))
            self.comboBox_6.setCurrentText(str(0))
            self.comboBox_8.setCurrentText(str(0))
            self.close()
        else:
            pass


#######################################################
########## Teachers Class #############################
#######################################################

addteacher ,_ = loadUiType('newteacher.ui')


class AddNewTeacher(QWidget, addteacher):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.registerTeacher)

    def registerTeacher(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )
        Name = self.lineEdit.text()
        subject = self.lineEdit_2.text()
        address = self.lineEdit_3.text()
        phone = self.lineEdit_4.text()

        try:
            self.cur = self.db.cursor()
            self.cur.execute('''INSERT INTO teachers (teachername, teacherphone, teachersubject, teachersaddress)
            VALUES (%s, %s, %s, %s)''', (Name, phone, subject, address))
            self.db.commit()
            self.close()
        except:
            self.label_7.setText('Please Check All Field Again ')



editTeachersUi ,_ = loadUiType('editdelete_teachers.ui')
class EditTeachersMain(QWidget, editTeachersUi):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.searchTeachers)
        self.pushButton_3.clicked.connect(self.SaveTeachers)
        self.pushButton_2.clicked.connect(self.removeteacher)

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )
        self.cur = self.db.cursor()


        self.cur.execute('SELECT teachername FROM teachers')
        DBB = self.cur.fetchall()
        
        for names in DBB:
            self.comboBox.addItem(names[0])
            EditTeachersMain.close(self)   

    def SaveTeachers(self):
        saveId = self.comboBox.currentText()

        username = self.lineEdit.text()
        subject = self.lineEdit_2.text()
        phone = self.lineEdit_3.text()
        address = self.lineEdit_4.text()

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',)

        self.cur = self.db.cursor()
        self.cur.execute('''
            UPDATE teachers SET teachername=%s, teacherphone=%s, teachersubject=%s, teachersaddress=%s WHERE teachername=%s ''',
            (username, phone, subject, address, saveId))
        self.db.commit()
        self.db.close()
        self.comboBox.setCurrentText(str(0))
        self.lineEdit.setText(' ')
        self.lineEdit_2.setText(' ')
        self.lineEdit_4.setText(' ')
        self.lineEdit_3.setText(' ')
        self.close()
        
    def searchTeachers(self):
        try:
            teachersearch = self.comboBox.currentText()
            self.db = pymysql.connect(
                host='localhost',
                user='root',
                password=Password,
                db='timetable',
            )
            self.cur = self.db.cursor()

            self.cur.execute('SELECT * FROM teachers WHERE teachername=%s ', teachersearch)
            DBB =self.cur.fetchone()
            
            self.lineEdit.setText(DBB[1])
            self.lineEdit_2.setText(DBB[3])
            self.lineEdit_3.setText(str(DBB[2]))
            self.lineEdit_4.setText(DBB[4])
        except:
            pass

    def removeteacher(self):
        self.TODELET = self.lineEdit.text()
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )
        try:
            self.cur = self.db.cursor()
            warning = QMessageBox.warning(self, 'Delete Teacher', 'Are you sure you want to delete this User?', QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('DELETE FROM teachers WHERE teachername = %s ', self.TODELET )
                self.db.commit()
                self.lineEdit.setText(' ')
                self.lineEdit_2.setText(' ')
                self.lineEdit_4.setText(' ')
                self.lineEdit_3.setText(' ')
                self.comboBox.setCurrentText(str(0))
        except:
            pass

            ### keep crashing if search is NOne, need to fix this
   

########################################################
### User Createtion Class
#########################################################

class UserReg(QWidget, createuser):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Registration)

    
    def Registration(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )
        username = self.lineEdit.text()
        email = self.lineEdit_2.text()
        phone = self.lineEdit_4.text()
        password= self.lineEdit_3.text()
        password2 = self.lineEdit_5.text()

        try:
            if password == password2:
                self.cur = self.db.cursor()
                self.cur.execute('''INSERT INTO users (User_name, User_email, User_phone, User_password)
                VALUES (%s, %s, %s, %s)''',
                (username, email, phone, password))
                self.db.commit()
                            
            else:
                pass
        except:
            self.label_7.setText('Please Check All Field Again')


################################################
####              Edit Users Class      ########
################################################

edituses,_ = loadUiType('editdelete_users1.ui')
from PyQt5.QtWidgets import QMessageBox

class EditUsers(QWidget, edituses):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.searchUsers)
        self.pushButton_2.clicked.connect(self.removeUsers)
        self.pushButton_3.clicked.connect(self.saveusers)

    
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )

        self.cur=self.db.cursor()
        self.cur.execute('SELECT User_name FROM users')
        DBB = self.cur.fetchall()
        

        for data in DBB:
            self.comboBox.addItem(str(data[0]))
            EditUsers.close(self)


    def searchUsers(self):
        usersearch = self.comboBox.currentText()
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )


        self.cur=self.db.cursor()
        self.cur.execute('SELECT * FROM users WHERE User_name = %s', usersearch )
        DBB = self.cur.fetchone()
        
        self.lineEdit.setText(DBB[1])
        self.lineEdit_2.setText(DBB[2])
        self.lineEdit_4.setText(str(DBB[3]))
        self.lineEdit_3.setText(DBB[4])

        self.db.commit()


    def removeUsers(self):
        self.TODELET = self.lineEdit.text()
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',
        )

        self.cur = self.db.cursor()
        warning = QMessageBox.warning(self, 'Delete User', 'Are you sure you want to delete this User?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('DELETE FROM users WHERE User_name = %s ', self.TODELET )
            self.db.commit()
            self.lineEdit.setText(' ')
            self.lineEdit_2.setText(' ')
            self.lineEdit_4.setText(' ')
            self.lineEdit_3.setText(' ')
            self.comboBox.setCurrentText(str(0))

        else:
            pass


    def deleteusers(self):
        return self.editusers()


    def saveusers(self):
        saveId = self.comboBox.currentText()
        username = self.lineEdit.text()
        email = self.lineEdit_2.text()
        phone = self.lineEdit_4.text()
        password = self.lineEdit_3.text()
        password2 = self.lineEdit_5.text()

        if password == password2:
            self.db = pymysql.connect(
            host='localhost',
            user='root',
            password=Password,
            db='timetable',)

            self.cur = self.db.cursor()
            self.cur.execute(''' UPDATE users SET User_name=%s, User_email=%s, User_phone=%s, User_password=%s WHERE User_name=%s '''
            , (username, email, phone, password, saveId))
            self.db.commit()

            time.sleep(5)
            self.close()

        else:
            self.label_7.setText('Please Check details')


def runall():
    app = QApplication(sys.argv)
    window = LogMeIn()
    window.show()
    app.exec_()


if __name__ == '__main__':
    runall()

