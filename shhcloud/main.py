import glob
import os
import random
import sys
from collections import Counter
from wordcloud import WordCloud


def color_func(word, _unused_font_size, _unused_position, _unused_orientation, _unused_random_state=None, **kwargs):
    color = "rgb({0}, {1}, {2})".format(
        random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)
    )
    return color


def main():
    arg_list = sys.argv
    img_width = 1920
    img_height = 1080
    working_dir = os.getcwd()
    save_file = os.path.join(working_dir, "wordcloud.jpg")
    if arg_list != []:
        for loc, arg in enumerate(arg_list):
            if arg == "-s":
                try:
                    w = arg_list[loc + 1]
                    h = arg_list[loc + 2]
                    if w.isnumeric() and h.isnumeric():
                        print(w.isnumeric, h.isnumeric)
                        img_width = w
                        img_height = h
                    else:
                        print(
                            "oops! width and height should be integers. the given values are ignored and",
                            img_width,
                            "and",
                            img_height,
                            "are used",
                        )
                except:
                    print(
                        "oops! width and height should be integers. the given values are ignored and",
                        img_width,
                        "and",
                        img_height,
                        "are used",
                    )
            elif arg == "-f":
                try:
                    f = arg_list[loc + 1]
                    if f[0] == "." and f[1].isalnum:
                        save_file = os.path.join(working_dir, f[1, -1])
                    elif f[0] == "/":
                        save_file = f
                    elif f[0].isalnum:
                        save_file = os.path.join(working_dir, f)
                except:
                    print("invalid path, default(./wordcloud.jpg) will be used")
            else:
                pass

    home_dir = os.environ["HOME"]
    # Get directories stored in $PATH
    command_dir = os.environ["PATH"].split(":")
    shell = os.environ["SHELL"]

    valid_commands = []
    # Get names of all files immediately in all of the above directories and add to valid_commands
    for directory in command_dir:
        for valid_command in glob.glob(directory + "/*"):
            valid_commands.append(valid_command.split("/")[-1])

    # Get shell's built in commands by running 'compgen -b' and add them to valid_commands
    built_in_commands = os.popen("compgen -b").read().split("\n")
    valid_commands.extend(built_in_commands)

    # get aliases from shell
    aliases = os.popen(shell + " -i -c alias").read().split("\n")
    if "" in aliases:
        aliases.remove("")

    aliases = {
        alias.replace("alias ", "")
        .split("=")[0]
        .replace("'", ""): alias.replace("alias ", "")
        .split("=")[1]
        .replace("'", "")
        for alias in aliases
    }

    # Open and read .bash_history
    with open(os.path.join(home_dir, ".bash_history"), "r") as bash_history:
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
        if parent == "sudo":
            # If parent command is sudo, get the child command (ie, for 'sudo mv' get 'mv')
            child = split_command[1]
            if child in valid_commands:
                words.append(child)

        # If pipes(|) exists in the command, get the command after each pipes
        for loc, word in enumerate(split_command):
            if word == "|":
                if split_command[loc + 1] in valid_commands:
                    words.append(split_command[loc + 1])
                # if it's a sudo, get the child command same as above
                if split_command[loc + 1] == "sudo":
                    words.append(split_command[loc + 2])

    # Create a frequency table from the words list
    freq_table = Counter(words)

    # Do the magic with frequency table instead
    wc = WordCloud(
        color_func=color_func,
        max_words=len(freq_table),
        width=int(img_width),
        height=int(img_height),
    ).generate_from_frequencies(freq_table)

    # Save it to a file
    try:
        wc.to_file(save_file)
    except:
        print(
            "oops! something went wrong while writing to the file. Please check if the given path is writable"
        )
        exit(1)


if __name__ == "__main__":
    main()
