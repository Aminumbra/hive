import Board
import BoardUI
import Pieces
import Moves


b = Board.Board()
ui = BoardUI.BoardUI(b)

b.board[10][10].append(Pieces.Spider())
b.board[11][10].append(Pieces.Ant(1))
b.board[12][10].append(Pieces.Queen(1))
b.board[10][11].append(Pieces.Beetle(1))
b.board[11][11].append(Pieces.Spider(1))
b.board[12][11].append(Pieces.Beetle(0))
b.board[10][12].append(Pieces.Grasshopper(0))
b.board[11][12].append(Pieces.Grasshopper(1))
b.board[11][13].append(Pieces.Queen(0))

b.white_queen = True
b.black_queen = True
b.movecount   = 6

ui.render()
ui.manage_events()
