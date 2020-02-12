A game notation for Hive
========================

Hive is a strategic board game, designed by John Yianni, with simple rules and
deep strategy.  This repository describes a way of recording a game of Hive in
text format, in much the same way as Chess's
[PGN](https://en.wikipedia.org/wiki/Portable_Game_Notation), so that it can be
shared and analysed later.  We also include a formal description of the notation
as a BNF grammar, and a couple of tools for parsing files.

Other notations
---------------
Other attempts to produce a notation for Hive already exist, with some success,
for example:
- [BoardSpace](https://www.boardspace.net/english/about_hive_notation.html)
- [jclopes](https://github.com/jclopes/hive#Notation)
- [Dave Dyer](https://boardgamegeek.com/thread/117554/hive-notation)

These systems share many features, and are partially successful -- indeed, the
first two are used in computer game implementations of Hive.  But they all share
several limitations that make them awkward for use by humans:
- They rely on a fixed orientation, which only makes sense when viewing the game
  board from one direction.
- Pieces are numbered based on the order in which they were placed, meaning that
  knowledge of the game's history is required in order to understand a given
  move.  Orienting bug heads to store this information is unwieldy, and cannot
  be expected from people playing with physical pieces.
- The use of slashes and stars to 

Goals
-----


Description
-----------


Examples
--------
