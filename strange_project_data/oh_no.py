import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QLineEdit, QPushButton,
                             QPlainTextEdit)
from PyQt5.QtGui import QPixmap
import random
import json


passive_i = 0
chat_name = ""
dialogue_over_flag = False
name_entry_flag = False
first_robot_startup_flag = False

with open("robot_responses.json") as robot_responses:
    robot_speak = json.loads(robot_responses)

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        global chat_name
        self.first_responses = ("I SEE YOU'RE\nNEW HERE.", "WELCOME.", "OVER THERE IS\nYOUR OWN\nCHATBOT.",
                                "DOESN'T LOOK\nLIKE MUCH...", "BUT PROVING ME WRONG\nIS YOUR\nRESPONSIBILITY.",
                                "FIRST, LET'S GIVE IT A NAME.")
        self.name_picked_responses = [chat_name + ".", "A FINE NAME.", "NOW...", "LET US BEGIN."]  # add more text
        self.robot_activated = ["HERE IT IS.", chat_name + " IS LIKE YOUR VERY OWN PET.",
                                "THE DIFFERENCE IS THAT YOU\nDON'T NEED TO TAKE CARE OF IT\nAS MUCH.",
                                "LET'S TRY TALKING TO IT."]
        self.talked_to_robot = ["IT DOESN'T KNOW MUCH YET.", "TEACH IT ALL SORTS OF NEW PHRASES!"]
        self.robo_animations = ["robot_starting.png", "robot_heads_up.png", "robot_arms.png", "robot_no_eyes.png",
                                "robot_blink.png", "robot_full.png"]

        self.setGeometry(640, 400, 300, 300)

        hbox = QHBoxLayout(self)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(QPixmap("robot_starting.png"))
        self.lbl.move(0, 0)

        hbox.addWidget(self.lbl)
        self.setLayout(hbox)

        self.dialogue_label = QLabel(self)
        self.dialogue_label.setMinimumSize(200, 50)
        self.dialogue_label.setText("longlonglonglonglonglonglong\nlonglonglonglonglonglonglong\nlong")
        self.dialogue_label.setText("HELLO.")
        self.dialogue_label.move(20, 20)

        self.name_entry = QLineEdit(self)
        self.name_entry.move(270, 260)
        self.name_entry.setDisabled(True)
        self.name_entry.hide()

        self.confirm_button = QPushButton("CONFIRM", self)
        self.confirm_button.resize(100, 50)
        self.confirm_button.move(270, 295)
        self.confirm_button.setDisabled(True)
        self.confirm_button.hide()
        self.confirm_button.clicked.connect(self.confirm_name)

        self.next_button = QPushButton("NEXT", self)
        self.next_button.resize(100, 50)
        self.next_button.move(550, 360)
        self.next_button.clicked.connect(self.flag_checks)

        self.gif_button = QPushButton(self)
        self.gif_button.hide()
        self.gif_button.clicked.connect(self.picture_change)

        self.send_button = QPushButton(self)
        self.send_button.hide()
        self.send_button.move(375, 340)
        self.send_button.setFixedSize(30, 30)
        self.send_button.clicked.connect(self.talk_to_it)

        # buttons for interactions with chatbot go here

        # chatbot dialogue and ways to talk to it go here
        self.robot_chatbox = QLabel(self)
        self.robot_chatbox.setMinimumSize(200, 50)
        self.robot_chatbox.move(310, 305)
        self.robot_chatbox.hide()

        self.robot_user = QLineEdit(self)
        self.robot_user.move(275, 340)
        self.robot_user.hide()

        self.move(300, 300)
        self.setWindowTitle("strange_project_demo")
        self.show()

    def advance_text(self, dialogue_mass):
        global passive_i
        global dialogue_over_flag
        if passive_i < len(dialogue_mass):
            self.dialogue_label.setText(dialogue_mass[passive_i])
            passive_i += 1
        else:
            passive_i = 0
            dialogue_over_flag = True

    def flag_checks(self):
        global dialogue_over_flag
        if name_entry_flag is False:
            if dialogue_over_flag is True:
                self.next_button.setDisabled(True)
                self.confirm_button.setDisabled(False)
                self.confirm_button.show()
                self.name_entry.setDisabled(False)
                self.name_entry.show()
                dialogue_over_flag = False
            else:
                self.advance_text(self.first_responses)
        elif first_robot_startup_flag is False:
            if dialogue_over_flag is True:
                for i in range(len(self.robo_animations) + 1):  # figure out how to animate
                    self.gif_button.click()
                    self.dialogue_label.setText("STARTING UP...")
                dialogue_over_flag = False
                self.next_button.show()
            else:
                self.advance_text(self.name_picked_responses)
                self.next_button.show()
        else:
            if dialogue_over_flag is False:
                self.advance_text(self.robot_activated)
            else:
                self.robot_chatbox.show()
                self.robot_chatbox.setText("hello.")
                self.robot_user.show()
                self.next_button.hide()
                self.send_button.show()

    def talk_to_it(self):  # the main feature
        global temporary_dict
        if self.robot_user.text() in robot_speak.keys():
            self.robot_chatbox.setText(robot_speak[self.robot_user.text()])
        else:
            with open("robot_responses.json", "w"):
                json.dumps(self.robot_user.text(), self.robot_chatbox.text())
            '''with open("robot_responses_backup.txt", "w") as write_this:
                write_this.write(str(self.robot_user.text(), self.robot_chatbox.text()))'''

    def play_with_it(self):  # the Tamagotchi aspect
        pass

    def destroy_it(self):  # reset button
        pass

    def exit_it(self):  # implement saving
        pass

    def confirm_name(self):
        global chat_name
        global name_entry_flag
        chat_name = self.name_entry.text()
        self.confirm_button.setDisabled(True)
        self.confirm_button.hide()
        self.name_entry.setDisabled(True)
        self.name_entry.hide()
        name_entry_flag = True
        self.name_picked_responses[0] = chat_name + "."
        self.next_button.setDisabled(False)

    def picture_change(self):
        global first_robot_startup_flag
        global passive_i
        print(passive_i)
        if passive_i < len(self.robo_animations):
            self.lbl.setPixmap(QPixmap(self.robo_animations[passive_i]))
            self.next_button.hide()
            passive_i += 1
            print(passive_i)
        else:
            passive_i = 0
            print(first_robot_startup_flag)
            if first_robot_startup_flag is False:
                first_robot_startup_flag = True



'''class Hm(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('how_quaint.ui', self)
        self.label.setText("OK")'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    '''new = Hm()
    new.show()'''
    ex = Example()
    sys.exit(app.exec_())