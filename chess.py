import pygame
import set_board
import moves

pygame.init()

screen_width = 850
screen_length = 616

screen = pygame.display.set_mode((screen_width , screen_length))
pygame.display.set_caption("Chess bot")
timer = pygame.time.Clock()
fps = 60

screen.fill((80, 31, 145))
square_number = {}
square_number = set_board.board(screen)
rects_voce, rects_adversario, cor_voce = set_board.set_board(screen , square_number)

circulos = {}
pre_circulos = {}
jogadores = [rects_adversario, rects_voce]
font = pygame.font.Font(None, 18)

# Variável para rastrear o índice do jogador atual

if cor_voce == 'b':
    indice_jogador_atual = 1  # "você" começa
else:
    indice_jogador_atual = 0  # "adversário" começa

firt_game_move = True
running = True
while running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            status = False
            mouse_x, mouse_y = pygame.mouse.get_pos()

            jogador_atual = jogadores[indice_jogador_atual]

            for nome_peca, (rect_peca, img) in jogador_atual.items():
                if rect_peca.collidepoint(mouse_x, mouse_y):
                    imagem = img
                    nome = nome_peca
                    if not len(pre_circulos) == 0:
                        moves.remove_circulos(screen, circulos, rects_adversario, rects_voce, jogador_atual)
                    circulos , nome_id = moves.moves_opition(screen, nome_peca, rect_peca, rects_adversario, rects_voce, jogador_atual)
                    pre_circulos = circulos.copy()
                    rect_peca_clicada = rect_peca  # Armazena o retângulo da peça clicada
                    break

            for chave, rect_circulo in circulos.items():
                if rect_circulo.collidepoint(mouse_x, mouse_y):
                    running = moves.move(screen, rect_circulo, rect_peca_clicada, imagem, circulos, rects_adversario, rects_voce, jogador_atual, nome , nome_id, font)
                    status = True  # Usa o retângulo da peça clicada
                    break
                    
            if status: # Alternar para o próximo jogador
                indice_jogador_atual = (indice_jogador_atual + 1) % len(jogadores)

pygame.quit()