import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
import random


# WELCOME TO HELL ITSELF. I'M THE NARRATOR. YOU WON'T ENJOY YOUR TIME HERE, TRUST ME.
passive_i = 0
dialogue_over_flag = False
name_entry_flag = False
first_robot_startup_flag = False
first_robot_talk_flag = False
starting_dialogue_clear_flag = False
destroy_flag = False
flag_mass = [name_entry_flag, first_robot_startup_flag, first_robot_talk_flag, starting_dialogue_clear_flag]  # IMPORTANT GLOBAL VARIABLES.

guess_this = []
guess_string = []  # FOR HANGING PEOPLE.

robot_responses = open("robot_responses.txt").read().split("\n")
robot_new_responses = open("robot_responses.txt", "a")
hangman = open("hangman.txt").read().split("\n")
more_hangman = open("hangman.txt", "a")
saved_data = open("saved_data.txt").read().split("\n")
print(saved_data)
chat_name = saved_data[0]
flag_data = saved_data[1:]
for i in range(len(flag_data)):
    if flag_data[i] == "False":
        flag_mass[i] = not bool(flag_data[i])
    else:
        flag_mass[i] = bool(flag_data[i])
name_entry_flag, first_robot_startup_flag, first_robot_talk_flag, starting_dialogue_clear_flag = flag_mass[0], flag_mass[1], flag_mass[2], flag_mass[3]
for i in flag_data:
    if "False" in i or saved_data == []:
        save_data = open("saved_data.txt", "w")  # FOR SAVING AND LOADING.


class ChatBot_v1(QWidget):  # DON'T SCREW ME OVER.

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):  # WHERE EVERYTHING IS STORED.
        global chat_name
        self.setFixedSize(660, 430)

        self.first_responses = ("I SEE YOU'RE\nNEW HERE.", "WELCOME.", "OVER THERE IS\nYOUR OWN\nCHATBOT.",
                                "DOESN'T LOOK\nLIKE MUCH...", "BUT PROVING ME WRONG\nIS YOUR\nRESPONSIBILITY.",
                                "FIRST, LET'S GIVE IT A NAME.")
        self.name_picked_responses = [chat_name + ".", "A FINE NAME.", "NOW...", "LET US BEGIN."]  # add more text
        self.robot_activated = ["HERE IT IS.", chat_name + " IS LIKE YOUR VERY OWN PET.",
                                "THE DIFFERENCE IS THAT YOU\nDON'T NEED TO TAKE CARE OF IT\nAS MUCH.",
                                "LET'S TRY TALKING TO IT."]
        self.talked_to_robot = ["IT DOESN'T KNOW MUCH YET.", "TEACH IT ALL SORTS OF NEW PHRASES!", "BUT YOU KNOW WHAT?", "I'LL LET YOU\nFIGURE OUT THE REST\nON YOUR OWN."]
        self.robot_destroyed = ["ALAS, POOR CHATBOT.", "All IT DID WAS ITS JOB,\nAND PROPERLY AT THAT.",
                                "NOW YOU'RE GONNA HAVE TO\nLISTEN TO ME AGAIN.", "YOU SCREWED YOURSELF OVER.",
                                "GOOD JOB.", "..."]

        self.robo_animations = ["robot_starting.png", "robot_heads_up.png", "robot_arms.png", "robot_no_eyes.png",
                                "robot_blink.png", "robot_full.png"]

        self.hangman_animations = ["hangman_one_wrong.png", "hangman_two_wrong.png", "hangman_three_wrong.png", "hangman_four_wrong.png",
                                   "hangman_five_wrong.png", "hangman_six_wrong.png", "hangman_seven_wrong.png", "hangman_eight_wrong.png",
                                   "hangman_dead.png"]

        self.setGeometry(640, 400, 300, 300)

        hbox = QHBoxLayout(self)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(QPixmap("robot_starting.png"))
        self.lbl.move(0, 0)

        self.hangman_label = QLabel(self)
        self.hangman_label.setPixmap(QPixmap("hangman_none.png"))
        self.hangman_label.setFixedSize(220, 240)
        self.hangman_label.move(15, 45)
        self.hangman_label.hide()

        hbox.addWidget(self.lbl)
        self.setLayout(hbox)

        self.dialogue_label = QLabel(self)
        self.dialogue_label.setMinimumSize(200, 50)
        self.dialogue_label.setText("longlonglonglonglonglonglong\nlonglonglonglonglonglonglong\nlong")
        self.dialogue_label.setText("HELLO.")
        self.dialogue_label.move(210, 20)

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

        self.send_button_copy = QPushButton(self)
        self.send_button_copy.hide()
        self.send_button_copy.move(375, 340)
        self.send_button_copy.setFixedSize(30, 30)
        self.send_button_copy.clicked.connect(self.send_letter)

        self.send_button_sug = QPushButton(self)
        self.send_button_sug.hide()
        self.send_button_sug.move(375, 340)
        self.send_button_sug.setFixedSize(30, 30)
        self.send_button_sug.clicked.connect(self.write_word)

        self.talk_button = QPushButton("TALK", self)
        self.talk_button.move(0, 340)
        self.talk_button.hide()
        self.talk_button.clicked.connect(self.talk_to_it)
        self.play_button = QPushButton("PLAY", self)
        self.play_button.move(0, 370)
        self.play_button.hide()
        self.play_button.clicked.connect(self.play_with_it)
        self.reset_button = QPushButton("RESET", self)
        self.reset_button.move(560, 340)
        self.reset_button.hide()
        self.reset_button.clicked.connect(self.destroy_it)
        self.exit_button = QPushButton("EXIT", self)
        self.exit_button.move(560, 370)
        self.exit_button.hide()
        self.exit_button.clicked.connect(self.exit_it)
        self.button_mass = [self.talk_button, self.play_button, self.reset_button, self.exit_button]

        self.suggest_button = QPushButton("SUGGEST", self)
        self.suggest_button.move(0, 340)
        self.suggest_button.hide()
        self.suggest_button.clicked.connect(self.suggest_word)

        self.robot_chatbox = QLabel(self)
        self.robot_chatbox.setMinimumSize(200, 50)
        self.robot_chatbox.move(275, 305)
        self.robot_chatbox.hide()

        self.robot_user = QLineEdit(self)
        self.robot_user.move(275, 340)
        self.robot_user.hide()

        self.stop_button = QPushButton("CLOSE", self)
        self.stop_button.move(275, 370)
        self.stop_button.hide()
        self.stop_button.clicked.connect(self.default_robot)

        self.move(300, 300)
        self.setWindowTitle("strange_project_demo")
        self.show()

    def advance_text(self, dialogue_mass):  # FOR WHEN I'M TALKING.
        global passive_i
        global dialogue_over_flag
        if passive_i < len(dialogue_mass):
            self.dialogue_label.setText(dialogue_mass[passive_i])
            passive_i += 1
        else:
            passive_i = 0
            dialogue_over_flag = True

    def default_robot(self):  # FOR WHEN YOU'RE NOT NEW.
        self.hide_chat()
        self.stop_button.hide()
        self.next_button.hide()
        self.show_four_buttons()
        self.dialogue_label.setText("WHAT DO YOU WANT TO DO WITH " + chat_name + "?")

    def flag_checks(self):  # FOR WHEN YOU'RE NEW.
        global dialogue_over_flag, starting_dialogue_clear_flag
        global destroy_flag
        global save_data
        if destroy_flag is False:
            if starting_dialogue_clear_flag is False:
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
                elif first_robot_talk_flag is False:
                    if dialogue_over_flag is False:
                        self.advance_text(self.robot_activated)
                    else:
                        self.show_chat()
                        self.robot_chatbox.setText("hello.")
                        self.next_button.hide()
                        self.dialogue_label.setText("CLICK THAT LITTLE BUTTON\nTO SEND YOUR\nMESSAGE.")
                        dialogue_over_flag = False
                else:
                    if dialogue_over_flag is False:
                        self.advance_text(self.talked_to_robot)
                    else:
                        try:
                            starting_dialogue_clear_flag = True
                            dialogue_over_flag = False
                            save_data.write(chat_name + "\n" + str(name_entry_flag) + "\n" + str(first_robot_startup_flag) + "\n" + str(first_robot_talk_flag) + "\n" + str(starting_dialogue_clear_flag))
                            self.default_robot()
                        except Exception as e:
                            print(e)
            else:
                for i in range(len(self.robo_animations)):
                    self.picture_change()
                self.default_robot()
        else:
            if dialogue_over_flag is False:
                self.advance_text(self.robot_destroyed)
            else:
                self.dialogue_label.setText("CLOSE THE APPLICATION.")

    def show_four_buttons(self):  # OUT OF THE MAIN MENU.
        for i in range(len(self.button_mass)):
            self.button_mass[i].show()

    def hide_four_buttons(self):  # IN THE MAIN MENU.
        for i in range(len(self.button_mass)):
            self.button_mass[i].hide()

    def talk_to_it(self):  # THE MAIN FEATURE.
        global robot_new_responses
        global first_robot_talk_flag
        global robot_responses
        if first_robot_talk_flag is True:
            self.stop_button.show()
        self.dialogue_label.setText("WANNA TALK TO IT?")
        self.show_chat()
        self.hide_four_buttons()
        self.robot_chatbox.setText(random.choice(robot_responses))
        # print(random.choice(robot_responses))
        if self.robot_user.text() != "":
            if self.robot_user.text() not in robot_responses and self.robot_user.text() + "." not in robot_responses\
                    and self.robot_user.text().lower() not in robot_responses:
                if self.robot_user.text()[-1] == "?":
                    if "i don't know, " + self.robot_user.text() not in robot_responses:
                        self.robot_chatbox.setText(("i don't know, " + self.robot_user.text()).lower())
                        robot_new_responses.write("\n" + self.robot_user.text().lower())
                        robot_new_responses.write(("\n" + "i don't know, " + self.robot_user.text()).lower())
                    elif "i don't know, " + self.robot_user.text() in robot_responses:
                        try:
                            self.robot_chatbox.setText(robot_responses
                                                       [robot_responses.index("i don't know, " + self.robot_user.text()) + 1])
                        except IndexError:
                            self.robot_chatbox.setText("...")
                elif self.robot_user.text()[-1] not in ".,!~":
                    robot_new_responses.write(("\n" + self.robot_user.text() + ".").lower())
                else:
                    robot_new_responses.write(("\n" + self.robot_user.text()).lower())
            else:
                self.robot_chatbox.setText(random.choice(robot_responses))
            self.robot_user.clear()
        if first_robot_talk_flag is False:
            first_robot_talk_flag = True
            self.next_button.show()
            self.hide_chat()
            self.flag_checks()

    def play_with_it(self):  # THE TAMAGOTCHI ASPECT.
        global hangman
        global more_hangman
        global passive_i
        global guess_this
        global guess_string
        passive_i = 0
        self.hide_four_buttons()
        self.send_button_sug.hide()
        self.stop_button.show()
        self.show_chat()
        self.send_button.hide()
        self.send_button_copy.show()
        self.suggest_button.show()
        self.hangman_label.show()
        self.dialogue_label.setText("YOU'RE PLAYING HANGMAN.")
        guess_this = list(random.choice(hangman))
        guess_string = list("*" * len(guess_this))
        self.robot_chatbox.setText("*" * len(guess_this))
        '''print(guess_this)
        print(guess_string)'''

    def destroy_it(self):  # RESET BUTTON.
        # PLEASE DO NOT TOUCH WITHOUT PERMISSION.
        global name_entry_flag, first_robot_startup_flag, first_robot_talk_flag, starting_dialogue_clear_flag
        global destroy_flag
        global chat_name
        global passive_i
        passive_i = 0
        try:
            name_entry_flag = False
            first_robot_startup_flag = False
            first_robot_talk_flag = False
            starting_dialogue_clear_flag = False
            chat_name = ""
            self.hide_four_buttons()
            with open("saved_data.txt", "w") as save_data:
                save_data.write(chat_name + "\n" + str(name_entry_flag) + "\n" + str(first_robot_startup_flag)
                                + "\n" + str(first_robot_talk_flag) + "\n" + str(starting_dialogue_clear_flag))
            with open("robot_responses.txt", "w") as robot_goodbyes:
                with open("robot_responses_backup.txt") as memory_wipe:
                    robot_goodbyes.write(memory_wipe.read())
            with open("hangman.txt", "w") as first_hang:
                with open("hangman_backup.txt") as last_hang:
                    first_hang.write(last_hang.read())
            self.dialogue_label.setText("...")
            self.lbl.setPixmap(QPixmap("robot_starting.png"))
            self.next_button.show()
            destroy_flag = True
            self.flag_checks()
            pass
        except Exception as e:
            print(e)

    def exit_it(self):  # SAVING IMPLEMENTED.
        self.dialogue_label.setText("USE THE X BUTTON PLEASE.")

    def send_letter(self):  # FOR USE IN HANGMAN.
        global guess_this
        global passive_i
        print(passive_i)
        print(len(self.hangman_label.text()))
        i_count = 0
        if len(self.robot_user.text()) <= 1:
            if self.robot_user.text() in guess_this and self.robot_user.text() != "":
                for i in self.robot_user.text():
                    for j in range(len(guess_this)):
                        if guess_this[j] == i:
                            guess_string[j] = i
                            self.robot_chatbox.setText("".join(guess_string))
                for i in guess_string:
                    if "*" in i:
                        i_count += 1
                if i_count == 0:
                    self.dialogue_label.setText("YOU WIN!")
                    self.send_button_copy.setDisabled(True)
            else:
                if passive_i < len(self.hangman_animations) - 1:
                    print(self.hangman_animations[passive_i])
                    self.hangman_label.setPixmap(QPixmap(self.hangman_animations[passive_i]))
                    passive_i += 1
                else:
                    self.dialogue_label.setText("YOU LOSE!")
                    self.hangman_label.setPixmap(QPixmap(self.hangman_animations[-1]))
                    self.send_button_copy.setDisabled(True)
                    passive_i = 0
        else:
            self.dialogue_label.setText("USE ONLY ONE LETTER.")
        self.robot_user.clear()

    def suggest_word(self):  # SUGGESTION ACTIVATION.
        self.send_button_copy.hide()
        self.robot_chatbox.hide()
        self.send_button_sug.show()
        self.dialogue_label.setText("CUSTOMIZE HANGMAN\nWITH YOUR OWN WORDS.")

    def write_word(self):  # THE ACTUAL SUGGESTIONS.
        global more_hangman
        if len(self.robot_user.text()) <= 2 and self.robot_user.text() != "":
            self.dialogue_label.setText("TOO SHORT.")
            self.robot_user.clear()
        elif len(self.robot_user.text()) > 7:
            self.dialogue_label.setText("TOO LONG.")
            self.robot_user.clear()
        elif self.robot_user.text() in hangman or self.robot_user.text().lower() in hangman:
            self.dialogue_label.setText("SUGGEST SOMETHING NEW.")
            self.robot_user.clear()
        elif self.robot_user.text() == "":
            self.dialogue_label.setText("CUSTOMIZE HANGMAN\nWITH YOUR OWN WORDS.")
        else:
            more_hangman.write("\n" + self.robot_user.text().lower())
            self.robot_user.clear()
            self.play_with_it()


    def show_chat(self):  # WHEN YOU NEED EVERYONE TO SEE...
        self.robot_chatbox.show()
        self.robot_user.show()
        self.send_button.show()

    def hide_chat(self):  # WHEN YOU NEED NO ONE TO SEE...
        self.robot_chatbox.hide()
        self.robot_user.hide()
        self.send_button.hide()
        self.send_button_copy.hide()
        self.send_button_sug.hide()
        self.suggest_button.hide()
        self.stop_button.hide()
        self.hangman_label.setPixmap(QPixmap("hangman_none.png"))
        self.hangman_label.hide()

    def confirm_name(self):  # NAME CONFIRMATION.
        global chat_name
        global name_entry_flag
        global save_data
        chat_name = self.name_entry.text()
        self.confirm_button.setDisabled(True)
        self.confirm_button.hide()
        self.name_entry.setDisabled(True)
        self.name_entry.hide()
        name_entry_flag = True
        self.name_picked_responses[0] = chat_name + "."
        self.next_button.setDisabled(False)

    def picture_change(self):  # ANIMATIONS. DON'T WORK.
        global first_robot_startup_flag
        global passive_i
        print(passive_i)
        self.dialogue_label.setText("STARTING UP...")
        if passive_i < len(self.robo_animations):
            self.lbl.setPixmap(QPixmap(self.robo_animations[passive_i]))
            self.next_button.hide()
            passive_i += 1
        else:
            passive_i = 0
            if first_robot_startup_flag is False:
                first_robot_startup_flag = True



'''class Hm(QMainWindow):  # JUST A DUMMY FILE. DOESN'T EXIST.
    def __init__(self):
        super().__init__()

        uic.loadUi('how_quaint.ui', self)
        self.label.setText("OK")'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    '''new = Hm()
    new.show()'''  # IT FAILED, IT SERVES NO PURPOSE TO ME.
    ex = ChatBot_v1()
    sys.exit(app.exec_())