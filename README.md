# Hive
________

Implementation of the Hive game

Original game description : https://en.wikipedia.org/wiki/Hive_(game)


# Rules:
________

See the previously linked wiki !


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

Once you press the key, your piece should appear.

If it is not the case :

* It might be against the rules: for example, you might be trying to place a piece on a non-empty cell, or to place while there are adjacent ennemy pieces.

* It might be a bug .-.


To move a piece : first Left-Click on the piece you wish to move. A list of available moves should appear, as white hexagons. Then, simply click on the cell you wish to go to.

If this does not work :

* You might be trying to move an ennemy piece

* You might be trying to move a piece with no available moves: for example, moving it would break the 'One-Hive Rule'.

* It might be also be a bug .-.
