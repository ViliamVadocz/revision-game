"""Runs the game."""

from data_parser import parse_game_data

import sys

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

        self.title = "Setup"
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
        self.topics = parse_game_data('game_data.txt')
        
        self.padding = 50
        self.team_height = 200

        self.title = "Main"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        exit_button = QPushButton('x', self)
        exit_button.setFont(QFont('Arial', 20))
        exit_button.move(1870, 20)
        exit_button.resize(30, 30)
        exit_button.clicked.connect(self.exit_button_on_click)

        team_width = (1920 - 2*self.padding) / len(self.teams)

        for i, team in enumerate(self.teams):
            team_name = QLabel(team.name, self)
            team_name.setFont(QFont('Arial', 24))
            team_name.move(self.padding+i*team_width, self.padding)
            team_name.resize(team_width, 30)
            
            team_points = QLabel(f'{team.score}', self)
            team_points.setFont(QFont('Arial', 30))
            team_points.move(self.padding+i*team_width, self.padding+50)
            team_points.adjustSize()
            

        topic_width = (1920 - 2*self.padding) / len(self.topics)
        for i, topic in enumerate(self.topics):
            topic_name = QLabel(topic.name, self)
            topic_name.setFont(QFont('Arial', 24))
            topic_name.move(self.padding+ i*topic_width, self.team_height+self.padding)
            topic_name.adjustSize()

            question_height = (1080 - self.team_height - 2*self.padding - 100) / len(topic.questions)

            for ii, question in enumerate(topic.questions):
                question_button = QPushButton(f'{question.points}', self)
                question_button.setFont(QFont('Arial', 40))
                question_button.move(self.padding+ i*topic_width, self.team_height + self.padding + 100 + ii*question_height)
                question_button.resize(topic_width, question_height)
                #question_button.clicked.connect(self.exit_button_on_click)

    def paintEvent(self, event):
        pad = self.padding

        painter = QPainter(self)
        painter.setPen(Qt.black)

        # Draw horizontal line.
        painter.drawLine(pad, self.team_height, 1920-pad, self.team_height)


    @pyqtSlot()
    def exit_button_on_click(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SetupWindow()
    sys.exit(app.exec_())
