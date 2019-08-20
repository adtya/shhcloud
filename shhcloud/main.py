import os
import numpy as np
import random
import glob
from PIL import Image
from wordcloud import WordCloud


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    color = "rgb(%d, %d, %d)" % (random.randint(128, 255),
                                 random.randint(128, 255),
                                 random.randint(128, 255))
    return(color)


def main():
    home_dir = os.environ['HOME']
    command_dir = os.environ['PATH'].split(":")

    valid_commands = []
    for directory in command_dir:
        for valid_command in glob.glob(directory + "/*"):
            valid_commands.append(valid_command.split("/")[-1])

    built_in_commands = os.popen('compgen -b').read().split('\n')
    valid_commands.extend(built_in_commands)
    bash_history = open(os.path.join(home_dir, ".bash_history"), "r")

    commands = bash_history.readlines()
    commands = [command.strip() for command in commands]
    words = []
    for command in commands:
        split_command = command.split(" ")
        parent = split_command[0]
        if parent in valid_commands:
            words.append(parent)
        if (parent == "sudo"):
            child = split_command[1]
            if child in valid_commands:
                words.append(child)

        for loc, word in enumerate(split_command):
            if word == "|":
                if split_command[loc+1] in valid_commands:
                    words.append(split_command[loc+1])
                if split_command[loc+1] == 'sudo':
                    words.append(split_command[loc+2])

    words = random.sample(words, len(words))
    text = " ".join(words)

    wc = WordCloud(color_func=color_func, max_words=len(words), mask=None, stopwords=None,
                   margin=2, random_state=1, width=1920, height=1080).generate(text)

    wc.to_file("wordcloud.jpg")


if __name__ == '__main__':
    main()
