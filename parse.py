#!/usr/bin/env python3

import sys
from lark import Lark, Transformer
from textwrap import fill

hive_parser = Lark(open("hive.bnf").read(), start="file")


def game_tree(game_text):
    tree = hive_parser.parse(game_text)
    return tree


def print_game_tree(game_text):
    tree = game_tree(game_text)
    print(tree)


class TreeToExplanation(Transformer):
    def file(self, tags_and_game):
        tags, game = tags_and_game
        return "GAME EXPLANATION\n\n" + tags + "\n\n" + game

    def tags(self, tags):
        return "This game had the following tags:\n" + "\n".join(tags)

    def tag(self, key_and_value):
        key, value = key_and_value
        return "  " + key + ": " + value

    def game(self, turns):
        return "The game progressed as follows:\n" + "\n".join(turns)

    def turn(self, args):
        num = args[0]
        ply1 = args[1]
        description = "On turn " + str(num) + ", " + ply1
        if len(args) > 2:
            ply2 = args[2]
            description += ", then " + ply2 + "."
        return fill(description)

    def ply(self, args):
        return "".join(args)

    def move(self, piece):
        (piece,) = piece
        return piece + " moved"

    def drop(self, piece):
        (piece,) = piece
        return piece + " was placed"

    def climb(self, piece):
        piece1, piece2 = piece
        return piece1 + " climbed onto " + piece2

    def from_location(self, location):
        (location,) = location
        return " from " + location

    def to_location(self, location):
        (location,) = location
        return " onto the space " + location

    def location(self, args):
        piece = args[0]
        description = "next to " + piece
        if len(args) == 2:
           description += ", " + args[1]
        return description

    def neighbour_reference(self, args):
        if len(args) == 1:
            return "next to " + args[0]
        elif len(args) == 2:
            return args[1] + " places clockwise from " + args[0]
        elif len(args) == 3:
            # TODO: handle 2-argument sub-reference well
            return args[2] + " places clockwise from " + args[0] + " (the one " + args[1] + ")"
        raise AssertionError("Grammar shouldn't allow this")

    white_queen = lambda self, _: "white's queen"
    black_queen = lambda self, _: "black's queen"
    white_grasshopper = lambda self, _: "white's grasshopper"
    black_grasshopper = lambda self, _: "black's grasshopper"
    white_ant = lambda self, _: "white's ant"
    black_ant = lambda self, _: "black's ant"
    white_spider = lambda self, _: "white's spider"
    black_spider = lambda self, _: "black's spider"
    white_beetle = lambda self, _: "white's beetle"
    black_beetle = lambda self, _: "black's beetle"
    white_mosquito = lambda self, _: "white's mosquito"
    black_mosquito = lambda self, _: "black's mosquito"

    def angle(self, value):
        (value,) = value
        return str(value)

    win = lambda self, _: " and wins the game"

    def comment(self, comment):
        (comment,) = comment
        return " (" + comment + ")"



def explain_game_tree(game_text):
    return TreeToExplanation().transform(game_tree(game_text))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        game_text = open(sys.argv[1]).read()
    else:
        game_text = sys.stdin.read()
    print(explain_game_tree(game_text))
