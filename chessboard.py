import pygame
from pygame.sprite import Sprite

class ChessPiece(Sprite):
    def __init__(self, name, value, img, pos):
        super().__init__()
        self.name = name
        self.value = value
        self.moved = 0
        self.moves = []
        self.captures = []
        self.defensores = []
        self.img = img
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def update_moves_and_captures(self, board, row, col, fen_info):
        self.moves = []
        self.captures = []
    
        if self.name.upper() == 'K':
            self._king_moves(board, row, col, fen_info)
        elif self.name.upper() == 'Q':
            self._queen_moves(board, row, col)
        elif self.name.upper() == 'R':
            self._rook_moves(board, row, col)
        elif self.name.upper() == 'B':
            self._bishop_moves(board, row, col)
        elif self.name.upper() == 'N':
            self._knight_moves(board, row, col)
        elif self.name.upper() == 'P':
            self._pawn_moves(board, row, col)

    def _king_moves(self, board, row, col, fen_info):
        deltas = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

        roque_brancas_curto, roque_brancas_longo, roque_pretas_curto, roque_pretas_longo = False, False, False, False
        for i in fen_info:
            if i == 'K':
                roque_brancas_curto = True
            elif i == 'Q':
                roque_brancas_longo = True
            elif i == 'k':
                roque_pretas_curto = True
            elif i == 'q':
                roque_pretas_longo = True

        # Implementação do roque
        if self.name.isupper() and row == 7 and col == 4:
            if board[row][col + 1] == '0' and board[row][col + 2] == '0' and roque_brancas_curto:
                self.moves.append((row, col + 2))
            if board[row][col - 1] == '0' and board[row][col - 2] == '0' and board[row][col - 3] == '0' and roque_brancas_longo:
                self.moves.append((row, col - 2))
        elif self.name.islower() and row == 0 and col == 4:
            if board[row][col + 1] == '0' and board[row][col + 2] == '0' and roque_pretas_curto:
                self.moves.append((row, col + 2))
            if board[row][col - 1] == '0' and board[row][col - 2] == '0' and board[row][col - 3] == '0' and roque_pretas_longo:
                self.moves.append((row, col - 2))

        for delta in deltas:
            new_row, new_col = row + delta[0], col + delta[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == '0':
                    self.moves.append((new_row, new_col))
                    self.defensores.append((new_row, new_col))
                elif board[new_row][new_col].islower() if self.name.isupper() else board[new_row][new_col].isupper():
                    self.captures.append((new_row, new_col))

    def _queen_moves(self, board, row, col):
        self._sliding_moves(board, row, col, [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)])

    def _rook_moves(self, board, row, col):
        self._sliding_moves(board, row, col, [(0, -1), (-1, 0), (0, 1), (1, 0)])

    def _bishop_moves(self, board, row, col):
        self._sliding_moves(board, row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def _knight_moves(self, board, row, col):
        deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for delta in deltas:
            new_row, new_col = row + delta[0], col + delta[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == '0':
                    self.moves.append((new_row, new_col))
                    self.defensores.append((new_row, new_col))
                elif board[new_row][new_col].islower() if self.name.isupper() else board[new_row][new_col].isupper():
                    self.captures.append((new_row, new_col))
                elif board[new_row][new_col].isupper() if self.name.isupper() else board[new_row][new_col].islower():
                    self.defensores.append((new_row, new_col))

    def _pawn_moves(self, board, row, col):
        direction = -1 if self.name.isupper() else 1
        start_row = 6 if self.name.isupper() else 1
        deltas = [(direction, 0)]
        self.defensores.append((((row + 1) * direction), col + 1))
        self.defensores.append((((row + 1) * direction), col - 1))
        if self.moved == 0 and board[row + 1 * direction][col] == '0':
            deltas.append((2 * direction, 0))

        for delta in deltas:
            new_row, new_col = row + delta[0], col + delta[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == '0':
                    self.moves.append((new_row, new_col))
        
        # Captures for pawns
        capture_deltas = [(direction, -1), (direction, 1)]
        for delta in capture_deltas:
            new_row, new_col = row + delta[0], col + delta[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] != '0' and (board[new_row][new_col].islower() if self.name.isupper() else board[new_row][new_col].isupper()):
                    self.captures.append((new_row, new_col))

    def _sliding_moves(self, board, row, col, deltas):
        for delta in deltas:
            new_row, new_col = row + delta[0], col + delta[1]
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == '0':
                    self.moves.append((new_row, new_col))
                    self.defensores.append((new_row, new_col))
                elif board[new_row][new_col].islower() if self.name.isupper() else board[new_row][new_col].isupper():
                    self.captures.append((new_row, new_col))
                    break
                elif board[new_row][new_col].isupper() if self.name.isupper() else board[new_row][new_col].islower():
                    self.defensores.append((new_row, new_col))
                    break
                else:
                    break
                new_row += delta[0]
                new_col += delta[1]

pieces_data = {
    "K": ("K", 900, ("./pecas/rei_b.png", "./pecas/rei_p.png")),
    "Q": ("Q", 9, ("./pecas/rainha_b.png", "./pecas/rainha_p.png")),
    "R": ("R", 5, ("./pecas/torre_b.png", "./pecas/torre_p.png")),
    "B": ("B", 3, ("./pecas/bispo_b.png", "./pecas/bispo_p.png")),
    "N": ("N", 3, ("./pecas/cavalo_b.png", "./pecas/cavalo_p.png")),
    "P": ("P", 1, ("./pecas/peao_b.png", "./pecas/peao_p.png"))
}

class Board:
    SQUARE_SIZE = 77
    ROWS, COLS = 8, 8
    DARK_COLOR = (71, 70, 74)
    LIGHT_COLOR = (207, 203, 214)

    def __init__(self, screen):
        self.screen = screen
        self.square_number = self.create_board()
        self.ball_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.pieces = []  # Armazena todas as peças do tabuleiro
        self.pecas_capturadas = []
    def create_board(self):
        square_number = {}
        for i in range(Board.ROWS):
            for j in range(Board.COLS):
                color = Board.DARK_COLOR if (i + j) % 2 == 0 else Board.LIGHT_COLOR
                x = j * Board.SQUARE_SIZE
                y = i * Board.SQUARE_SIZE
                pygame.draw.rect(self.screen, color, (x, y, Board.SQUARE_SIZE, Board.SQUARE_SIZE))
                square_number[f"{i}.{j}"] = (x, y)
        
        pygame.display.update()
        return square_number

    def draw_pieces(self, fen):
        y = 0
        x = 0 
        for i in fen:
            if i == " ":
                break
            if i == "/":
                y += 1
                x = 0
            elif i in "12345678":
                x += int(i)
            elif i.isupper():
                piece_data = pieces_data[i]
                pos = self.square_number[f"{y}.{x}"]
                sprite = ChessPiece(i, piece_data[1], piece_data[2][0], pos)
                self.all_sprites.add(sprite)
                self.pieces.append((sprite, y, x))
                x += 1
            elif i.islower():
                piece_data = pieces_data[i.upper()]
                pos = self.square_number[f"{y}.{x}"]
                sprite = ChessPiece(i, piece_data[1], piece_data[2][1], pos)
                self.all_sprites.add(sprite)
                self.pieces.append((sprite, y, x))
                x += 1

        self.all_sprites.draw(self.screen)
        pygame.display.update()

    def checkforcheks(self, rodada):
        def is_between(pos, start, end, mode='both'):
            (x1, y1), (x2, y2), (x, y) = start, end, pos
            
            if mode == 'orthogonal':  # Combinação de horizontal e vertical
                horizontal_check = y1 == y2 == y and (x1 <= x <= x2 or x2 <= x <= x1)
                vertical_check = x1 == x2 == x and (y1 <= y <= y2 or y2 <= y <= y1)
                return horizontal_check or vertical_check
            
            elif mode == 'diagonal':
                return (x2 - x1) * (y - y1) == (x - x1) * (y2 - y1) and (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1)
            
            elif mode == 'both':
                orthogonal_check = (y1 == y2 == y and (x1 <= x <= x2 or x2 <= x <= x1)) or (x1 == x2 == x and (y1 <= y <= y2 or y2 <= y <= y1))
                diagonal_check = (x2 - x1) * (y - y1) == (x - x1) * (y2 - y1) and (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1)
                return orthogonal_check or diagonal_check
        
        check = False
        atacante = None
        rei = None
        linha, coluna = 0, 0
        linha2, coluna2 = 0, 0

        # Verifica se o rei está em xeque
        for piece, row, col in self.pieces:
            if (rodada == "b" and piece.name == "K") or (rodada == "w" and piece.name == "k"):
                linha2, coluna2 = row, col
                rei = piece
                pos = (row, col)
                rei_moves_copy = rei.moves.copy()
                for move in rei_moves_copy:
                    for piece2, row2, col2 in self.pieces:
                        if piece2.name != rei.name:
                            if (piece2.name.isupper() and rei.name.islower()) or (piece2.name.islower() and rei.name.isupper()):
                                for piece4, row4, col4 in self.pieces:
                                    if move == (row2, col2) and (row2, col2) in piece4.defensores and (piece4.name != rei.name):
                                        rei.moves.remove(move)
                                if piece2.name in ["r", "b", "q", "R", "B", "Q"]:
                                    rook_pin, queen_pin, bishop_pin = [],[],[]
                                    for piece3, row3, col3 in self.pieces:
                                        if piece3.name != rei.name:
                                            if (piece3.name.islower() and rei.name.islower()) or (piece3.name.isupper() and rei.name.isupper()):
                                                if piece2.name in ["r", "R"] and is_between((row3, col3), (row, col), (row2, col2), 'orthogonal'):
                                                    rook_pin.append(piece3)
                                                if piece2.name in ["b", "B"] and is_between((row3, col3), (row, col), (row2, col2), 'diagonal'):
                                                    bishop_pin.append(piece3)
                                                if piece2.name in ["q", "Q"] and is_between((row3, col3), (row, col), (row2, col2), 'both'):
                                                    queen_pin.append(piece3)
                                    if len(rook_pin) == 1:
                                        rook_pin[0].moves.clear()
                                    if len(bishop_pin) == 1:
                                        bishop_pin[0].moves.clear()
                                    if len(queen_pin) == 1:
                                        queen_pin[0].moves.clear()

                                if move in piece2.moves or move in piece2.defensores:
                                    try:
                                        rei.moves.remove(move)
                                    except ValueError:
                                        pass
                                if pos in piece2.captures:
                                    atacante = piece2
                                    linha, coluna = row2, col2
                                    check = True

        # Se o rei está em xeque, ajusta os movimentos das outras peças
        if check:
            for piece, row, col in self.pieces:
                if piece.name != rei.name:
                    if (piece.name.isupper() and rei.name.isupper()) or (piece.name.islower() and rei.name.islower()):
                        new_moves = [move for move in piece.moves if is_between(move, (linha2, coluna2), (linha, coluna), 'both')]
                        new_captures = [move for move in piece.captures if move == (linha, coluna)]
                        piece.moves = new_moves
                        piece.captures = new_captures

    def FEN_reader(self, fen , rodada):
        rows = fen.split(' ')[0].split('/')
        fen_info = ''.join(fen.split(' ')[1:])
        board = []
        for row in rows:
            expanded_row = ""
            for char in row:
                if char.isdigit():
                    expanded_row += '0' * int(char)
                else:
                    expanded_row += char
            board.append(expanded_row)

        for piece, row, col in self.pieces:
            piece.update_moves_and_captures(board, row, col, fen_info)

        self.checkforcheks(rodada)

        
    def show_moves(self, cords):
        Ball.draw_balls(self, cords)
    
    def update_piece_position(self, selected_piece, target_row, target_col):
        # Atualiza a posição da peça selecionada na lista de peças
        selected_piece.rect.topleft = self.square_number[f"{target_row}.{target_col}"]
        for i, (piece, row, col) in enumerate(self.pieces):
            if piece == selected_piece:
                self.pieces[i] = (piece, target_row, target_col)
                break

        if selected_piece.name == "K" and target_row == 7 and target_col == 6:
            for piece, row, col in self.pieces:
                if piece.name == "R" and piece.rect.topleft == self.square_number["7.7"]:
                    self.update_piece_position(piece, 7, 5)
        elif selected_piece.name == "K" and target_row == 7 and target_col == 2:
            for piece, row, col in self.pieces:
                if piece.name == "R" and piece.rect.topleft == self.square_number["7.0"]:
                    self.update_piece_position(piece, 7, 3)
        elif selected_piece.name == "k" and target_row == 0 and target_col == 6:
            for piece, row, col in self.pieces:
                if piece.name == "r" and piece.rect.topleft == self.square_number["0.7"]:
                    self.update_piece_position(piece, 0, 5)
        elif selected_piece.name == "k" and target_row == 0 and target_col == 2:
            for piece, row, col in self.pieces:
                if piece.name == "r" and piece.rect.topleft == self.square_number["0.0"]:
                    self.update_piece_position(piece, 0, 3)
    
    def FEN_updater(self, fen):
        new_fen = ""
        promotion = False
        for row in range(8):  # Itera sobre cada linha
            num = 0  # Contador para casas vazias
            for col in range(8):  # Itera sobre cada coluna
                found_piece = False
                for piece, piece_row, piece_col in self.pieces:  # Itera sobre as peças
                    
                    if piece.rect.topleft == self.square_number[f"{row}.{col}"]:
                        if (piece.name == "p" and piece_row == 7) or (piece.name == "P" and piece_row == 0): 
                            promotion = True
                        if num > 0:
                            new_fen += str(num)
                            num = 0
                        if promotion:
                            promoção = str(input("Peao promovido (Q, N, B, R): "))
                            print(promoção)
                            
                            if piece.name.isupper():
                                new_fen += promoção
                            else:
                                new_fen += promoção.lower()

                            promotion = False
                            found_piece = True
                            break
                        else:
                            new_fen += piece.name
                        found_piece = True
                        break
                if not found_piece:
                    num += 1
            if num > 0:  # Adiciona qualquer número acumulado no final da linha
                new_fen += str(num)
            new_fen += "/" if row < 7 else ""
    
        # Adiciona a parte restante da FEN (lado a jogar, direitos de roque, etc.)
        fen_parts = fen.split(' ')
        modified_parts = ''.join(fen_parts[1:])
        swich, swich2 = True , True

        for part in modified_parts: #wKQkq-01
            if part == "w":
                new_fen += " b "
            elif part == "b":
                new_fen += " w "
            elif part == "K"and swich == True or part == "Q" and swich == True:
                roque, longo, curto = True, True, True
                for piece in self.pieces:
                    if piece[0].name == "K":
                        if piece[0].moved > 0:
                            roque = False
                    elif piece[0].name == "R" and piece[0].rect.topleft == self.square_number["7.0"]:
                        if piece[0].moved > 0:
                            longo = False
                    elif piece[0].name == "R" and piece[0].rect.topleft == self.square_number["7.7"]:
                        if piece[0].moved > 0:
                            curto = False
                if roque and longo:
                    new_fen += "Q"
                if roque and curto:
                    new_fen += "K"
                swich = False
            elif part == "k" and swich2 == True or part == "q" and swich2 == True:
                roque, longo, curto = True, True, True
                for piece in self.pieces:
                    if piece[0].name == "k":
                        if piece[0].moved > 0:
                            roque = False
                    elif piece[0].name == "r" and piece[0].rect.topleft == self.square_number["0.0"]:
                        if piece[0].moved > 0:
                            longo = False
                    elif piece[0].name == "r" and piece[0].rect.topleft == self.square_number["0.7"]:
                        if piece[0].moved > 0:
                            curto = False
                if roque and longo:
                    new_fen += "q"
                if roque and curto:
                    new_fen += "k"
                swich2 = False

        rounds = int(fen_parts[-1])
        rodadas = int(fen_parts[-2])
        rounds += 1
        if rounds % 2 == 0:
            rodadas = rounds // 2
        new_fen += f" - {str(rodadas)} {str(rounds)}"
        return new_fen
    
       
    def captura (self, selected_piece):
        capturada = None
        for sprite in self.all_sprites:
            if selected_piece.rect.collidepoint(sprite.rect.topleft) and sprite != selected_piece:
                capturada = sprite
                break
        self.pecas_capturadas.append(capturada)
        self.all_sprites.remove(capturada)
        self.pieces = [(piece, row, col) for piece, row, col in self.pieces if piece != capturada]
        self.redraw_board()

    def redraw_board(self):
        # Redesenha o tabuleiro e as peças
        self.create_board()
        self.all_sprites.draw(self.screen)
        pygame.display.update()
    
    def check_end_of_game(self):
        for capturar in self.pecas_capturadas:
            if capturar.name == 'k':
                print ("White Wins")
                return True
            elif capturar.name == 'K':
                print ("Black Wins")
                return True
        moves_white = []
        moves_black = []
        for piece, row, col in self.pieces:
            if piece.name.isupper():
                moves_white += piece.moves
                moves_white += piece.captures
            else:
                moves_black += piece.moves
                moves_black += piece.captures
        if moves_white == []:
            print ("Black Wins")
            return True
        elif moves_black == []:
            print ("White Wins")
            return True
        elif moves_white == [] and moves_black == []:
            print ("Draw")
            return True
        return False


class Ball(pygame.sprite.Sprite):
    def __init__(self, color = (128, 128, 128, 128), radius = 12, position = (0, 0)):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = position

    @staticmethod
    def draw_balls(board, cords):
        for cord in cords:
            x, y = cord
            pos_x, pos_y = board.square_number[f"{x}.{y}"]
            position = (pos_x + Board.SQUARE_SIZE // 2, pos_y + Board.SQUARE_SIZE // 2)
            ball = Ball(position=position)
            board.ball_sprites.add(ball)
        board.ball_sprites.draw(board.screen)
        pygame.display.update()
