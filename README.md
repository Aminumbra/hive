# Hive
________

Implementation of the Hive game

Original game description : https://en.wikipedia.org/wiki/Hive_(game)


# Rules:
________

See the previously linked wiki !

As for now, all the rules should be implemented :

- You can only place a piece on the board if it is not adjacent to any ennemy piece (except for the first piece that you put on the board)
- You can only move your pieces around once your Queen has been placed on the board
- You lose the game once your Queen is totally surrounded
- You must respect the One-Hive Rule (cf. the previous link for details)
- and so on


# How To play:
_______________


To start a new game, use the following command :

`python Main.py`


To place a piece on the board : first Right-Click on the cell you wish to place your piece on, then press the key corresponding to it :

- Queen : press q
- Spider : press s
- Beetle : press b
- Grasshopper : press g
- Ant : press a

Once you press the key, your piece should appear

If it is not the case :

* It might be against the rules: for example, you might be trying to place a piece on a non-empty cell, or to place while there are adjacent ennemy pieces

* It might be a bug .-.


To move a piece : first Left-Click on the piece you wish to move. A list of available moves should appear, as white hexagons. Then, simply click on the cell you wish to go to

If this does not work :

* You might be trying to move an ennemy piece

* You might be trying to move a piece with no available moves: for example, moving it would break the 'One-Hive Rule'

* It might be also be a bug .-.

# Interface:
____________

The GUI currently displays :
- The board, with the different pieces, which can be distinguished according to the letter written on them. As for now, you cannot scroll or zoom-out, and so the board is actually limited. Consequently, please try to place your first pieces on the center of the board, to avoid situations where your moves would be restricted by the screen borders. 
- The movecount, and the player whose turn it is
- The remaining pieces for each player (for more information, please see https://en.wikipedia.org/wiki/Hive_(game))
- A button for each piece, used to place a new piece of this type. This is not yet implemented, and so it is still necessary to use the previously-mentioned method with Right-Click + Keyboard to place a new piece on the board.
