"""Runs the game."""

from data_parser import parse_game_data

import sys
import time

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0


class SetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.teams = []
        self.max_teams = 5

        self.title = 'Setup'
        self.top = 200
        self.left = 500
        self.width = 750
        self.height = 450
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        text1 = QLabel('INPUT TEAMS', self)
        text1.setFont(QFont('Arial', 40))
        text1.move(40, 40)
        text1.adjustSize()

        self.textbox = QLineEdit(self)
        self.textbox.setFont(QFont('Arial', 16))
        self.textbox.move(40, 120)
        self.textbox.resize(280, 40)

        add_button = QPushButton('+', self)
        add_button.setFont(QFont('Arial', 20))
        add_button.move(360, 125)
        add_button.resize(30, 30)
        add_button.clicked.connect(self.add_button_on_click)

        # TODO Put minus next to teams, use a factory function
        minus_button = QPushButton('-', self)
        minus_button.setFont(QFont('Arial', 20))
        minus_button.move(410, 125)
        minus_button.resize(30, 30)
        minus_button.clicked.connect(self.minus_button_on_click)

        self.team_labels = []
        for team in range(self.max_teams):
            new_label = QLabel('',self)
            new_label.move(470, 125+60*team)
            new_label.setFont(QFont('Arial', 20))
            self.team_labels.append(new_label)

        submit_button = QPushButton('Confirm', self)
        submit_button.move(40, 200)
        submit_button.setFont(QFont('Arial', 32))
        submit_button.resize(400, 100)
        submit_button.clicked.connect(self.confirm_button_on_click) 

        self.show()

    @pyqtSlot()
    def add_button_on_click(self):
        if len(self.teams) < self.max_teams and self.textbox.text() != '':
            # Show the team label.
            self.team_labels[len(self.teams)].setText(self.textbox.text())
            self.team_labels[len(self.teams)].adjustSize()
            # Add team.
            self.teams.append(Team(self.textbox.text()))

    @pyqtSlot()
    def minus_button_on_click(self):
        if len(self.teams) > 0:
            # Remove team.
            self.teams.pop()
            # Remove team label.
            self.team_labels[len(self.teams)].setText('')     

    @pyqtSlot()
    def confirm_button_on_click(self):
        # Move to main screen.
        if len(self.teams) > 1:
            self.new_window = MainWindow(self.teams)
            self.new_window.showFullScreen()
            self.hide()



class MainWindow(QMainWindow):
    def __init__(self, teams):
        super().__init__()

        self.teams = teams
        self.turn = 0
        self.topics = parse_game_data('game_data.txt')
        self.total_q = 0
        self.ans_q = 0
        
        self.padding = 50
        self.team_height = 200

        self.title = 'Main'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        exit_button = QPushButton('x', self)
        exit_button.setFont(QFont('Arial', 20))
        exit_button.move(1870, 20)
        exit_button.resize(30, 30)
        exit_button.clicked.connect(self.exit_button_on_click)

        team_width = (1920 - 2*self.padding) / len(self.teams)

        self.team_name_labels = []
        self.team_point_labels = []
        for i, team in enumerate(self.teams):
            x = self.padding + i*team_width
            y = self.padding
            team_name = QLabel(team.name, self)
            team_name.setFont(QFont('Arial', 24))
            team_name.move(int(x), int(y))
            team_name.resize(int(team_width)-30, 40)
            self.team_name_labels.append(team_name)
            if i == 0: team_name.setStyleSheet("border: 2px solid blue;")
            
            team_points = QLabel(f'{team.score}', self)
            team_points.setFont(QFont('Arial', 30))
            team_points.move(int(x), int(y)+50)
            team_points.adjustSize()
            self.team_point_labels.append(team_points)

        topic_width = (1920 - 2*self.padding) / len(self.topics)
        for i, topic in enumerate(self.topics):
            x = self.padding+ i*topic_width
            y = self.team_height+self.padding
            topic_name = QLabel(topic.name, self)
            topic_name.setFont(QFont('Arial', 24))
            topic_name.move(int(x), int(y))
            topic_name.adjustSize()

            question_height = (1080 - self.team_height - 2*self.padding - 100) / len(topic.questions)

            for ii, question in enumerate(topic.questions):
                self.total_q += 1 # FInds total num of questions
                xx = self.padding+ i*topic_width
                yy = self.team_height + self.padding + 100 + ii*question_height
                question_button = QPushButton(f'{question.points}', self)
                question_button.setFont(QFont('Arial', 40))
                question_button.move(int(xx), int(yy))
                question_button.resize(int(topic_width), int(question_height))
                question_button.clicked.connect(self.question_func_maker(question, question_button))

    def paintEvent(self, event):
        pad = self.padding

        painter = QPainter(self)
        painter.setPen(Qt.black)

        # Draw horizontal line.
        painter.drawLine(pad, self.team_height, 1920-pad, self.team_height)

    @pyqtSlot()
    def exit_button_on_click(self):
        self.close()

    def question_func_maker(self, question, question_button):
        @pyqtSlot()
        def question_click():
            self.question_window = QuestionWindow(question, self)
            self.question_window.showFullScreen()
            question_button.hide()
            self.turn += 1
            self.turn %= len(self.teams)
        return question_click

    def game_end(self):
        # TODO Open END GAME Window
        self.close()
        print('END GAME')


class QuestionWindow(QMainWindow):

    def __init__(self, question, main_window):
        super().__init__()

        self.question = question
        self.main_window = main_window

        # Ugly code but idc
        self.teams = main_window.teams
        self.turn = main_window.turn
        self.team_point_labels = main_window.team_point_labels
        self.team_name_labels = main_window.team_name_labels

        self.title = f'{question.question}'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        
        question_text = QLabel(f'{self.question.question}', self)
        question_text.setFont(QFont('Arial', 40))
        question_text.adjustSize()
        x = (1920 - question_text.width()) / 2
        y = (1080 - question_text.height()) / 2 - 150
        question_text.move(int(x), int(y))

        self.answer_text = QLabel(f'{self.question.answer}', self)
        self.answer_text.setFont(QFont('Arial', 40))
        self.answer_text.adjustSize()
        x = (1920 - self.answer_text.width()) / 2
        y = (1080 - self.answer_text.height()) / 2 + 150
        self.answer_text.move(int(x), int(y))
        self.answer_text.hide()

        points_text = QLabel(f'{self.question.points}', self)
        points_text.setFont(QFont('Arial', 50))
        points_text.adjustSize()
        points_text.move(30, 30)

        self.show_answer_button = QPushButton('Show Answer', self)
        self.show_answer_button.setFont(QFont('Arial', 30))
        self.show_answer_button.resize(300, 100)
        x = (1920 - self.show_answer_button.width()) / 2
        y = 1080 - 200
        self.show_answer_button.move(int(x), int(y))
        self.show_answer_button.clicked.connect(self.show_answer_button_on_click)

        self.team_labels = []
        self.team_points = []
        for i, team in enumerate(self.teams):
            x = 50
            y = 150 + 50*i

            team_name = QLabel(team.name, self)
            team_name.setFont(QFont('Arial', 24))
            team_name.move(int(x)+100, int(y))
            team_name.adjustSize()
            team_name.hide()
            self.team_labels.append(team_name)
            
            points = self.question.points if self.turn == i else 0
            team_points = QLineEdit(f'{points}', self)
            team_points.setFont(QFont('Arial', 24))
            team_points.move(int(x), int(y))
            team_points.resize(80, 40)
            team_points.hide()
            self.team_points.append(team_points)
            
        self.accept_button = QPushButton('Confirm',self)
        self.accept_button.setFont(QFont('Arial', 30))
        self.accept_button.resize(300, 100)
        x = (1920 - self.accept_button.width()) / 2
        y = 1080 - 200
        self.accept_button.move(int(x), int(y))
        self.accept_button.clicked.connect(self.accept_button_on_click)
        self.accept_button.hide()

    @pyqtSlot()
    def show_answer_button_on_click(self):
        self.answer_text.show()

        for i in range(len(self.teams)):
            self.team_labels[i].show()
            self.team_points[i].show()

        self.show_answer_button.hide()
        time.sleep(0.2) # Sleep to prevent accidental click on accept
        self.accept_button.show()

    def accept_button_on_click(self):
        for i, team in enumerate(self.teams):
            team.score += int(self.team_points[i].text())
            self.team_point_labels[i].setText(f'{team.score}')
            self.team_point_labels[i].adjustSize()
            if i == (self.turn + 1) % len(self.teams):
                self.team_name_labels[i].setStyleSheet("border: 2px solid blue;")
            else:
                self.team_name_labels[i].setStyleSheet("border: 0px;")

        self.main_window.ans_q += 1
        if self.main_window.ans_q == self.main_window.total_q:
            self.main_window.game_end()

        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SetupWindow()
    sys.exit(app.exec_())
