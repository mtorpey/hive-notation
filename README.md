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
- Moves are sometimes described in unnecessary detail, including the moving
  piece, its number, the piece and number it moves next to, and on which side.
  Sometimes just naming a piece is enough to give an unambiguous move!

Goals
-----
We want a notation that has the following featues:
- **Don't rely on a fixed board orientation** -- Players can sit anywhere around
  a board, and shouldn't have to process game notation "upside-down".  There's
  no such thing as "North".
- **Don't rely on memory of the game** -- Notation for a move should only use
  the current state of the board, without assuming knowledge of the moves that
  got us here.  In particular, don't expect anyone to remember which piece is
  "Ant 1" and which is "Ant 2".
- **Be succinct** -- Each move by a player should be a short string without
  spaces, so it can be recorded and shared easily.  Try not to use two
  characters where one will do.
- **Don't include unnecessary information** -- Sometimes in Hive a description
  such as "white places an ant next to his queen" or even "black moves her
  grasshopper" can be enough to describe an unambiguous move.  There's no need
  to include extra information such as angles in these cases.
- **Be consistent with PGN (portable game notation)** -- This is a well-known
  notation system for chess, with variants designed for games like draughts and
  shogi.  Where we can be similar to this, we should.

These features are all part of our main goal: **A notation system that is easy
for humans to learn and use**.

Description
-----------
Here we will describe how the notation works.  The quickest way to understand it
is to see it in action with an explanation: have a look at
`examples/game3-annotated.txt`.  But if you want a full explanation, read on.

### Moves

A single move by a player is written as a single string, without spaces, in the
following form:

    [+] moving_piece [x under_piece] [[from_location -] to_location] [#]

The symbols have the following meaning:
- `+` means "add" a piece to the hive, i.e. place it from your supply
- `moving_piece` is the only mandatory part of the notation, and represents the
  piece that is moving.  It should be one of the characters `AaBbGgQqSs`
  representing an **a**nt, **b**eetle, **g**rasshopper, **q**ueen, or
  **s**pider.  Upper case is white, lower case black (for expansions, add
  `LlMmPp` as appropriate).
- `x` means that we are **climbing** on top of another piece (usually this is
  done by a beetle).  It should be followed by `under_piece`, a letter for the
  piece that we are moving onto.
- `to_location` is a description of the location our piece is moving to
  (explained below).
- `from_location` is included if necessary, in the same format, followed by a
  hyphen to separate it from `to_location`.  This may be required if there are
  two pieces of the same type that could legally move to the `to_location`
  indicated.
- `#` means that this move ends the game.  The result may be a win, loss, or
  draw for the active player.

Locations are phrased in terms of neighbouring pieces and angles.  A location
has the following form:

    neighbour [another_piece [angle]]

`neighbour` is a piece next to this location, `another_piece` is a piece next to
`neighbour`, and `angle` is the number of places clockwise around `neighbour`
that this location sits from `another_piece`.  This is a lot easier to
understand when you see examples.

Here are some examples of moves:
- `g` -- Black's grasshopper moves.
- `BxA` -- White's beetle climbs onto white's ant.
- `+QGs2` -- White places his queen next to white's grasshopper, 2 places
  clockwise around it from black's spider.
- `ABs1-ga3#` -- White's ant (the one currently next to white's beetle, 1 place
  clockwise around it from black's spider) moves next to black's grasshopper, 3
  places clockwise around it from black's ant.  This ends the game!

Note that locations don't have to include an angle, or even another piece.  Look
at the following examples:
- `bQ` -- Black's beetle moves next to white's queen
- `+agS` -- Black places an ant next to her own grasshopper (the one next to
  white's spider).

Those last two examples could have been `bQA3` or `+agS2`, but if we don't need
that extra information for an unambiguous move, it doesn't need to be included.

There's one more catch to how locations work: just in case the description of a
location is still ambiguous even after `neighbour`, `another_piece` and `angle`,
you can insert a pair of round brackets between `another_piece` and `angle`
explaining further.  For example:
- `gab(S)2` -- Black's grasshopper moves next to black's ant, two places round
  from black's beetle.  (Which one of black's beetles?  The one next to white's
  spider!)
- `+gaQ(s2)3` -- Black places a grasshopper next to her own ant, 3 places
  clockwise from white's queen.  (White's queen is next to black's spider, and
  the black ant in question is two places round clockwise from the spider).

These extra brackets are rarely needed -- perhaps once or twice per game.

### The whole game

A "turn" consists of two *moves*: one by the first player, one by the second
player.  When recording a whole game, these turns should be numbered starting
from 1, and the turn number followed by a dot should precede each move, as in
the following example.

    1. +G +s 2. +SGs2 +ssG3 3. +QGS1 +ass2 4. Ss +qsG2 5. +SGQ1 +gqs2

This continues until the game ends.  Additional whitespace can be inserted
anywhere, and for clarity you may wish to put each turn on a new line.  As in
PGN, a maximum line length of 80 characters is recommended.

### Files

You can use fragments of this notation to describe particular moves or games, on
paper, in online posts, or anywhere you want to record part of a Hive game.
However, you can also store a game as a full file, with the extension `.txt` or
`.hive`.  This is often done in `.pgn` files for chess.  If you make such a
file, you can include comments and tags as follows.

### Comments

Single-line comments can be included after a semi-colon `;`, and multi-line
comments can be included inside curly braces `{}` (just like PGN).  Don't use
round brackets to indicate alternative moves, since these are reserved for
locations as described above.

### Tags

Just like a PGN file in chess, you can start a Hive game file with any number of
*tag pairs*, giving information about the event, date, time, names of
participants, or anything else you wish to include.  A tag consists of a name
and a double quote-delimited string for its value.  For example:

    [Event "Hive Society round-robin final"]
    [Site "St Andrews, Scotland"]
    [Date "2020-02-14"]

There are no mandatory tags, but see
[PGN tag pairs](https://en.wikipedia.org/wiki/Portable_Game_Notation#Tag_pairs)
for common examples.  If playing with an expansion, you should specify an
`ExpansionPieces` tag with the symbols of all expansion pieces in play:

    [ExpansionPieces "Mm"]



Examples
--------
See the `examples/` directory for several real games set down in this notation.
Especially see `examples/game3-annotated.txt` for a game with a full running
explanation in English.



Tools in this repo
------------------
This directory contains a program `parse.py` that can be used to turn a file in
Hive notation into a verbose English description of the game.  Call it as
follows:

    ./parse.py examples/game2.txt

You can also use it as part of a bash pipeline:

    cat examples/game2.txt | ./parse.py > english-description.txt
