import Board
import BoardUI
import Pieces
import Moves


def start_game():
    b = Board.Board()
    ui = BoardUI.BoardUI(b)
    ui.render()

    winner = -1

    while True:

        ui.wait_for_move()
        
        if Moves.has_lost(b, 0):
            winner = 1
            break
        
        if Moves.has_lost(b, 1):
            winner = 0
            break

    ui.render_endgame(winner)
    ui.manage_all_events()

if __name__=="__main__":
    start_game()
