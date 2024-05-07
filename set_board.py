import pygame
import random
from pieces import pieces

def par_ou_impar(numero):
    if numero % 2 == 0:
        return True
    else:
        return False
    
def board(screen):
        square_number = {}
        x = 0
        y = 0
        for i in range(0 , 8):
            for j in range(0 , 8):
                 if par_ou_impar(i + j):
                    color = (71, 70, 74)
                 else:
                    color = (207, 203, 214)

                 pygame.draw.rect(screen, color, (x, y, 75, 77))
                 square_number[f"{i+1}.{j+1}"] = ((i * 75), (j * 77))
                 x += 75
            y += 77
            x = 0
        pygame.display.update()    
        return square_number
        

def set_board(screen, square_number):
    peao = pieces(value=1, nome="peao", id="P", p='./pecas/peao_p.png', b='./pecas/peao_b.png')
    torre = pieces(value=2, nome="torre", id="T", p='./pecas/torre_p.png', b='./pecas/torre_b.png')
    cavalo = pieces(value=3, nome="cavalo", id="C", p='./pecas/cavalo_p.png', b='./pecas/cavalo_b.png')
    bispo = pieces(value=4, nome="bispo", id="B", p='./pecas/bispo_p.png', b='./pecas/bispo_b.png')
    rei = pieces(value=5, nome="rei", id="R", p='./pecas/rei_p.png', b='./pecas/rei_b.png')
    rainha = pieces(value=6, nome="rainha", id="Q", p='./pecas/rainha_p.png', b='./pecas/rainha_b.png')

    peaos = [peao, peao, peao, peao, peao, peao, peao, peao]

    if random.choice([True, False]):
        cor_adversario = 'p'
        cor_voce = 'b'
    else:
        cor_adversario = 'b'
        cor_voce = 'p'

    if cor_adversario == 'p':
        pecas = [torre, cavalo, bispo, rainha, rei, bispo, cavalo, torre]
    else:
        pecas = [torre, cavalo, bispo, rei, rainha, bispo, cavalo, torre]

    rects_adversario = {}
    rects_voce = {}

    cores_adversario = {peca.id: getattr(peca, cor_adversario) for peca in pecas}
    cores_voce = {peca.id: getattr(peca, cor_voce) for peca in pecas}

    cores_peao_adversario = {peao.id: getattr(peao, cor_adversario) for peao in peaos}
    cores_peao_voce = {peao.id: getattr(peao, cor_voce) for peao in peaos}

    for i, peca in enumerate(pecas):
        img_adversario = cores_adversario[peca.id]
        screen.blit(pygame.image.load(img_adversario), square_number[f"{i + 1}.{1}"])

        rect_peca_adversario = pygame.Rect(square_number[f"{i + 1}.{1}"], (75, 77))

        nome_peca_adversario = f"{peca.nome}_adversario_{i}"
        rects_adversario[nome_peca_adversario] = (rect_peca_adversario, img_adversario)

    for i, peca in enumerate(pecas):
        img_voce = cores_voce[peca.id]
        screen.blit(pygame.image.load(img_voce), square_number[f"{i + 1}.{8}"])

        rect_peca_voce = pygame.Rect(square_number[f"{i + 1}.{8}"], (75, 77))

        nome_peca_voce = f"{peca.nome}_voce_{i}"
        rects_voce[nome_peca_voce] = (rect_peca_voce, img_voce)

    for i, peao in enumerate(peaos):
        img_peao_adversario = cores_peao_adversario[peao.id]
        screen.blit(pygame.image.load(img_peao_adversario), square_number[f"{i + 1}.{2}"])

        rect_peao_adversario = pygame.Rect(square_number[f"{i + 1}.{2}"], (75, 77))

        nome_peao_adversario = f"{peao.nome}_adversario_{i}"
        rects_adversario[nome_peao_adversario] = (rect_peao_adversario, img_peao_adversario)

        img_peao_voce = cores_peao_voce[peao.id]
        screen.blit(pygame.image.load(img_peao_voce), square_number[f"{i + 1}.{7}"])

        rect_peao_voce = pygame.Rect(square_number[f"{i + 1}.{7}"], (75, 77))

        nome_peao_voce = f"{peao.nome}_voce_{i}"
        rects_voce[nome_peao_voce] = (rect_peao_voce, img_peao_voce)

    pygame.display.update()
    return rects_voce, rects_adversario , cor_voce