import random
from aberturar import aberturas_xadrez
from chessboard import Board

def best_move(board, cor, historico_jogadas):
    
    def encontrar_proximos_movimentos(sequencia, aberturas):
            proximos_movimentos = []
            for movimentos in aberturas.values():
                if movimentos[:len(sequencia)] == sequencia and len(movimentos) > len(sequencia):
                    proximos_movimentos.append(movimentos[len(sequencia)])
            return proximos_movimentos
        
    abertura = encontrar_proximos_movimentos(historico_jogadas, aberturas_xadrez)
    
    if abertura != []:
        movimento = random.choice(abertura)
        
        peca_tipo = movimento[0]
        peca_linha = int(movimento[2])
        peca_coluna = int(movimento[1])
        
        for piece in board.pieces:
            if piece[0].name == peca_tipo:
                for move in piece[0].moves + piece[0].captures:
                    if move == (peca_coluna, peca_linha):
                        move = (peca_coluna, peca_linha)
                        best_move = (move, 100, piece[0])
                        return best_move
    else:
        pass
    best_move = None
    final_move_value = 0
    list_of_best_moves = []

    for piece, row, col in board.pieces:

        if (cor == "w" and piece.name.isupper()) or (cor == "b" and piece.name.islower()):
            for move in piece.moves + piece.captures:

                move_value = 0  # Reset move_value para cada novo movimento
                for piece2, row2, col2 in board.pieces: # Peça inimiga
                    if (cor == "b" and piece2.name.isupper()) or (cor == "w" and piece2.name.islower()):
                        if move == (row2, col2): # Se tiver uma capitura do bot
                            move_value += piece2.value
                        if move in piece2.defensores: # Se a jogada for perder uma peça
                            move_value -= piece2.value
                        if (row, col) in piece2.captures: # Se estiver prestes a perder a peça qualquer movimento e melhor
                            move_value += piece.value
                """for piece3, row3, col3 in board.pieces: # Peça do bot
                    if (cor == "w" and piece3.name.isupper()) or (cor == "b" and piece3.name.islower()):
                        if move in piece3.defensores: # Jogar a peça em um lugar protegido
                            move_value += piece.value"""
                        
                if piece.name.upper() == "K" and (move in [(7, 6), (7, 1)] if cor == "w" else move in [(0, 6), (0, 1)]):
                    move_value += 1
                elif piece.name.upper() == "P":
                    if move in [(3, 4), (3, 3), (4, 4), (4, 3)]:
                        move_value += 0.75
                    elif move in [(2, 2), (5, 5), (2, 5), (5, 2), (3, 2), (4, 2), (5, 2), (2, 5), (3, 5), (4, 5), (2, 3), (2, 4), (5, 3), (5, 4)]:
                        move_value += 0.5
                elif piece.name.upper() in ["N", "B"]:
                    if move in [(3, 4), (3, 3), (4, 4), (4, 3)]:
                        move_value += 0.6
                    elif move in [(2, 2), (5, 5), (2, 5), (5, 2), (3, 2), (4, 2), (5, 2), (2, 5), (3, 5), (4, 5), (2, 3), (2, 4), (5, 3), (5, 4)]:
                        move_value += 0.4
                elif piece.name.upper() == "R" and (move in [(0, 4), (0, 3)] if cor == "w" else move in [(7, 4), (7, 3)]):
                    move_value += 0.5
                
                if move_value > final_move_value:
                    final_move_value = move_value
                    best_move = (move, move_value, piece)
                    list_of_best_moves.append(best_move)
                if final_move_value == 0  and best_move == None:
                    best_move = (move, move_value, piece)

    return best_move
