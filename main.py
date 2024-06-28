import pygame
from chessboard import Board
import random
from bot import best_move


pygame.init()

screen = pygame.display.set_mode((Board.COLS * Board.SQUARE_SIZE, Board.ROWS * Board.SQUARE_SIZE))
pygame.display.set_caption("Chess Board")
board = Board(screen)

def redesenhar_tabuleiro(screen, board, FEN):
    board.create_board()
    board.all_sprites.draw(screen)  # Desenha todas as peças
    board.ball_sprites.draw(screen)  # Desenha todas as bolas
    pygame.display.flip()
    
def pixel_to_board(pos):
    pos_x, pos_y = pos
    col = pos_x // Board.SQUARE_SIZE
    row = pos_y // Board.SQUARE_SIZE
    return row, col

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
rodada = fen.split(' ')[1]
board.draw_pieces(fen)
board.FEN_reader(fen, rodada)
historico_jogadas = []

cores = ["w" , "b"]
jogadores = ["bot", "player"]
cor1 = random.choice(cores)
if cor1 == "w":
    cor2 = cores[1]
else:
    cor2 = cores[0]
adversarios = {"bot": cor1, "player": cor2}

selected_piece = None
running = True
while running:
   
    rodada = fen.split(' ')[1]
    if adversarios["bot"] == rodada:
        move = best_move(board, adversarios["bot"], historico_jogadas)
        piace = move[2]
        (target_row, target_col) = move[0]
        board.update_piece_position(piace, target_row, target_col)
        jogada = piace.name + str(target_row) + str(target_col)
        historico_jogadas.append(jogada)
        if (target_row, target_col) in piace.captures:
            board.captura(piace)
        fen = board.FEN_updater(fen)
        redesenhar_tabuleiro(screen, board, fen)
        piace.moved += 1
        board.FEN_reader(fen, rodada)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [
                    s for s in board.all_sprites
                    if (s.rect.collidepoint(pos) and (s.name.isupper() if rodada == "w" else s.name.islower()))
                ]
            clicked_ball = False
            
            for sprite in board.ball_sprites:
                if sprite.rect.collidepoint(pos):
                    target_row, target_col = pixel_to_board(pos)

                    if selected_piece:

                        board.update_piece_position(selected_piece, target_row, target_col)
                        jogada = selected_piece.name + str(target_col) + str(target_row)
                        historico_jogadas.append(jogada)
                        if (target_row, target_col) in selected_piece.captures:
                            board.captura(selected_piece)
                        fen = board.FEN_updater(fen)
                        print(fen)
                        board.ball_sprites.empty()
                        redesenhar_tabuleiro(screen, board, fen)
                        selected_piece.moved += 1
                        board.FEN_reader(fen, rodada)
                        selected_piece = None
                    clicked_ball = True
                    break

            if not clicked_ball:
                board.ball_sprites.empty()  # Limpa todas as bolinhas
                redesenhar_tabuleiro(screen, board, fen)
            
            if clicked_sprites:
                selected_piece = clicked_sprites[0]
                cords = selected_piece.moves + selected_piece.captures
                board.show_moves(cords)

            if board.check_end_of_game():
                running = False

    pygame.display.flip()
pygame.quit()
