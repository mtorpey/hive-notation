#!/usr/bin/env python3

import sys
from lark import Lark

hive_parser = Lark(open("hive.bnf").read(), start="move")


def game_tree(game_text):
    tree = hive_parser.parse(game_text)
    return tree


def print_game_tree(game_text):
    tree = game_tree(game_text)
    print(tree.pretty())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        game_text = open(sys.argv[1]).read()
    else:
        game_text = sys.stdin.read()
    print_game_tree(game_text)
