"""Used for parsing the game data text file into classes."""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Question:
    question : str 
    answer : str
    points : int


@dataclass
class Topic:
    name : str
    questions : List[Question] = field(default_factory=list)


def parse_line(line : str) -> Tuple[str, str, int]:
    """Parses a single question line to get the question, answer, points.
    
    Arguments:
        line {str} -- The line to parse.
    
    Returns:
        Tuple[str, str, int] -- Question, answer, and points.
    """
    line = line[:-1] # Strips newline character
    question_end = line.find(';')
    question = line[:question_end]

    line = line[question_end+1:]
    answer_end = line.find(';')
    answer = line[:answer_end]

    points = int(line[answer_end+1:])

    return question, answer, points


def parse_game_data(file_name : str) -> List[Topic]:
    """Goes over the file and parses it for topics,
    questions, answers, and points.

    The file should be formatted like this:

        ExampleTopic1[\\n]
        First Question?;First answer;100[\\n]
        Seconds Question?;Second answer;200[\\n]
        Third Question?;Third answer;300[\\n]
        [\\n]
        ExampleTopic2[\\n]
        First Question?;First answer;100[\\n]
        Seconds Question?;Second answer;200[\\n]
        Third Question?;Third answer;300[\\n]
        [\\n]

    The newline characters should not be typed explicitly!
    
    Arguments:
        file_name {str} -- The file name. Should include the extention.
    
    Returns:
        List[Topic] -- List of topics, each with their questions.
    """
    # Opens file.
    data = open(file_name, 'r')

    # Sets up variables.
    current_topic = None
    parsed_data = []

    # Loops over each line in the file.
    for line in data:
        
        # Creates new topic if there is none.
        if current_topic is None:
            current_topic = Topic(line[:-1])

        # Saves topic if encountered empty line.
        elif line == '\n':
            parsed_data.append(current_topic)
            current_topic = None

        # Parses question line and adds to topic.
        else:
            question, answer, points = parse_line(line)
            new_question = Question(question, answer, points)
            current_topic.questions.append(new_question)

    return parsed_data


# TEST CODE
if __name__ == '__main__':
    # Just prints the parsed data.
    parsed_data = parse_game_data('game_data.txt')
    for topic in parsed_data:
        print(topic.name)
        for question in topic.questions:
            print(question.question, question.answer, question.points)