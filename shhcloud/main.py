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
    # Get directories stored in $PATH
    command_dir = os.environ['PATH'].split(":")
    shell = os.environ['SHELL']

    valid_commands = []
    # Get names of all files immediately in all of the above directories and add to valid_commands
    for directory in command_dir:
        for valid_command in glob.glob(directory + "/*"):
            valid_commands.append(valid_command.split("/")[-1])

    # Get shell's built in commands by running 'compgen -b' and add them to valid_commands
    built_in_commands = os.popen('compgen -b').read().split('\n')
    valid_commands.extend(built_in_commands)

    # get aliases from shell
    aliases = os.popen(shell + ' -i -c alias').read().split('\n')
    if '' in aliases:
        aliases.remove('')

    aliases = {alias.replace('alias ', '').split('=')[0].replace("'", ''): alias.replace(
        'alias ', '').split('=')[1].replace("'", '') for alias in aliases}

    # Open and read .bash_history
    bash_history = open(os.path.join(home_dir, ".bash_history"), "r")
    commands = bash_history.readlines()
    # reomove unwanted \n and stuff from all the commands
    commands = [command.strip() for command in commands]

    words = []
    # split each command at " " and get the first word ie, the parent command
    for command in commands:
        split_command = command.split(" ")
        parent = split_command[0]
        if parent in valid_commands:
            # if the parent command is a valid command, add it to words
            words.append(parent)
        if parent in aliases.keys():
            words.append(aliases[parent].split(" ")[0])
        if (parent == "sudo"):
            # If parent command is sudo, get the child command (ie, for 'sudo mv' get 'mv')
            child = split_command[1]
            if child in valid_commands:
                words.append(child)

        # If pipes(|) exists in the command, get the command after each pipes
        for loc, word in enumerate(split_command):
            if word == "|":
                if split_command[loc+1] in valid_commands:
                    words.append(split_command[loc+1])
                # if it's a sudo, get the child command same as above
                if split_command[loc+1] == 'sudo':
                    words.append(split_command[loc+2])

    # Shuffle the words list (words repeating adjescently causes words to repeat in the picture)
    words = random.sample(words, len(words))
    # the below function needs the words to be part of a large string, so, join the above list
    text = " ".join(words)

    # do the magic
    wc = WordCloud(color_func=color_func, max_words=len(words), mask=None, stopwords=None,
                   margin=2, random_state=1, width=1920, height=1080).generate(text)

    # Save it to a file
    wc.to_file("wordcloud.jpg")


if __name__ == '__main__':
    main()
