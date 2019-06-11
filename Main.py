import Board
import BoardUI
import Pieces
import Moves


def start_game():
    b = Board.Board()
    ui = BoardUI.BoardUI(b)
    ui.render()
    ui.manage_events()


if __name__=="__main__":
    start_game()
