import pygame
from pieces import pieces

# Dicionário para armazenar os círculos
circulos = {}

def has_piece(x, y, rects_adversario, rects_voce, jogador_atual):
    x -= 37  # Optional offset adjustment (if needed)
    y -= 37

    for rect, _ in jogador_atual.values():
        if rect.collidepoint(x, y):
            return False
        
    if x < 0 or y < 0 or x >= 600 or y >= 616:
        return False

    return True

def can_capture(jogador_atual, rects_adversario, rects_voce):
    if jogador_atual == rects_voce:
        enermy = rects_adversario
        return enermy
    elif jogador_atual == rects_adversario:
        enermy = rects_voce
        return enermy

def circulo(x, y, screen, rects_adversario ,rects_voce, jogador_atual):
    if has_piece(x, y, rects_adversario, rects_voce, jogador_atual):
        pygame.draw.circle(screen, (150, 150, 150), (x, y), 15, 15)
        # print(f"circulo desenhado em: {x} , {y}")
        rect_circulo = pygame.Rect(x - 15, y - 15, 30, 30)

        chave = f"circulo_{len(circulos) + 1}"
        circulos[chave] = rect_circulo
        return circulos
    
not_moved = []
nome_id = ""
def moves_opition(screen, nome_peca, rect_peca, rects_adversario, rects_voce, jogador_atual):
    x = 37 + rect_peca.x
    y = 37 + rect_peca.y
    lista = True
    
    if nome_peca.startswith("peao"):
        nome_id = ""
        # Verificação para o jogador
        if nome_peca.startswith("peao_voce"):
            i = -1
        else:
            i = 1

        frente = True
        enermy = can_capture(jogador_atual, rects_adversario, rects_voce)

        for rect, imagem in rects_adversario.values():
            if rect.collidepoint(x - 37 , y - 37 + (77 * i)):
                frente = False
                break
        
        for rect, imagem in rects_voce.values():
            if rect.collidepoint(x - 37, y - 37 + (77 * i)):
                frente = False
                break

        for nome in not_moved:
            if nome_peca == nome:
                lista = False
                break
        else:
            lista = True
            
        if frente:
            if lista:
                circulo(x, y + (77 * i), screen, rects_adversario, rects_voce, jogador_atual)
                circulo(x, y + (154 * i), screen, rects_adversario, rects_voce, jogador_atual)
                
            else:
                circulo(x, y + (77 * i), screen, rects_adversario, rects_voce, jogador_atual)

        for nome_peca_adv, (rect_adv, _) in enermy.items():
            if rect_adv.collidepoint(rect_peca.x + 75, rect_peca.y + (77 * i)) or rect_adv.collidepoint(rect_peca.x - 75, rect_peca.y + (77 * i)):
                circulo(rect_adv.x + 37, rect_adv.y + 37, screen, rects_adversario, rects_voce, jogador_atual)
                
    elif nome_peca.startswith("cavalo"):
        nome_id = "N"
        deltas = [(150, 77), (150, -77), (-150, 77), (-150, -77),
                  (75, 154), (75, -154), (-75, 154), (-75, -154)]
        for dx, dy in deltas:
            circulo(x + dx, y + dy, screen, rects_adversario, rects_voce, jogador_atual)

    elif nome_peca.startswith("torre") or nome_peca.startswith("bispo") or nome_peca.startswith("rainha"):
        deltas = []
        if nome_peca.startswith("torre"):
            nome_id = "R"
            deltas = [(0, 77), (0, -77), (75, 0), (-75, 0)]
        if nome_peca.startswith("bispo"):
            nome_id = "B"
            deltas = [(75, 77), (75, -77), (-75, 77), (-75, -77)]
        if nome_peca.startswith("rainha"):
            nome_id = "Q"
            deltas = [(75, 0), (-75, 0), (0, 77), (0, -77), (75, 77), (75, -77), (-75, 77), (-75, -77)]

        for dx, dy in deltas:
            value = 0
            for i in range(1, 8):
                new_x = x + dx * i
                new_y = y + dy * i
                if has_piece(new_x, new_y, rects_adversario, rects_voce, jogador_atual) and value < 1:
                    circulo(new_x, new_y, screen, rects_adversario, rects_voce, jogador_atual)
                    enermy = can_capture(jogador_atual, rects_adversario, rects_voce)
                    for rect, _ in enermy.values():
                        if rect.collidepoint(new_x, new_y):
                            value += 1
                else:
                    break

    elif nome_peca.startswith("rei"):
        roque_curto = False
        roque_longo = False
        #define os movimentos basicos da peça
        deltas = [(0, 77), (75, 77), (75, 0), (75, -77),
                        (0, -77), (-75, -77), (-75, 0), (-75, 77)]
        
        #define as condiçoes do roque
        for nome, (rect, _) in rects_adversario.items():
            if not rect.x == x + 75 and rect.y == y and rect.x == x + 150 and rect.y == y:
                print("tem peca em curto")
                roque_curto = True
                break
            elif not rect.x == x - 75 and rect.y == y and rect.x == x - 150 and rect.y == y and rect.x == x - 225 and rect.y == y:
                print("tem peca em longo")
                roque_longo = True
                break
            
        for nome, (rect, _) in rects_voce.items():
            if not rect.x == x + 75 and rect.y == y and rect.x == x + 150 and rect.y == y:
                print("tem peca em curto")
                roque_curto = True
                break
            elif not rect.x == x - 75 and rect.y == y and rect.x == x - 150 and rect.y == y and rect.x == x - 225 and rect.y == y:
                print("tem peca em longo")
                roque_longo = True
                break
            
        for nome in not_moved:
                if nome == nome_peca:
                    print("rei movido")
                    roque_curto = False
                    roque_longo = False
                    break
                elif nome.startswith("torre") and nome.endswith("0"):
                    print("torre movida 0")
                    roque_curto = False
                elif nome.startswith("torre") and nome.endswith("1"):
                    print("torre movida 1")
                    roque_longo = False
                else :
                    print("nada movido")
                    roque_curto = True
                    roque_longo = True

        if roque_curto:
            print("roque curto")
            deltas.append((150, 0))
            nome_id = "O - O"
        elif roque_longo:
            print("roque longo")
            deltas.append((- 150, 0))
            nome_id = "O - O - O"
        else :
            nome_id = "K"

        for dx, dy in deltas:
            circulo(x + dx, y + dy, screen, rects_adversario, rects_voce, jogador_atual)

    pygame.display.update()
    return circulos, nome_id

def remove_circulos(screen, circulos, rects_adversario, rects_voce, jogador_atual):
    for chave, rect_circulo in circulos.items():
        value = 0
        x = rect_circulo.x
        y = rect_circulo.y
        for rect, imagem in rects_adversario.values():
            if rect.collidepoint(x, y):
                i = rect.x
                j = rect.y
                img = pygame.image.load(imagem)  # Carrega a imagem do adversário
                screen.blit(img, (i, j))
                value = 1
                break  # Interrompe o loop assim que uma colisão for encontrada
        for rect, imagem in rects_voce.values():
            if rect.collidepoint(x, y):
                i = rect.x
                j = rect.y
                img = pygame.image.load(imagem)  # Carrega a imagem do jogador atual
                screen.blit(img, (i, j))
                value = 1
                break  # Interrompe o loop assim que uma colisão for encontrada
        if 0 <= x < screen.get_width() and 0 <= y < screen.get_height() and value == 0:
            color = screen.get_at((x + 2, y + 2))
            pygame.draw.rect(screen, color, (x, y, 30, 30))
    circulos.clear()

registro_de_movimentação = []

def move(screen, rect_circulo, rect_peca, imagem, circulos, rects_adversario, rects_voce, jogador_atual, nome_peca, nome_id , font):
    remove_circulos(screen, circulos, rects_adversario, rects_voce, jogador_atual)
    x = rect_peca.x
    y = rect_peca.y
    color = screen.get_at((x + 2 , y + 2))
    pygame.draw.rect(screen, color, (x, y, 75, 77))

    i = rect_circulo.x - 22
    j = rect_circulo.y - 22

    rect_peca.x = i
    rect_peca.y = j

    captura = ""
    enermy = can_capture(jogador_atual, rects_adversario, rects_voce)
    if (nome_peca == "rei_voce" or nome_peca == "rei_adversario") and (nome_id == "O - O - O" or nome_id == "O - O"):
        for nome, (rect , imagem) in jogador_atual.items():
            if nome.startswith("torre") and nome.endswith("0"):
                not_moved.insert(1 ,nome)
                img = pygame.image.load(imagem)
                screen.blit(img, (i + 75, j))
                break
        for nome, (rect , imagem) in jogador_atual.items():
            if nome.startswith("torre") and nome.endswith("1"):
                not_moved.insert(1 ,nome)
                img = pygame.image.load(imagem)
                screen.blit(img, (i - 75, j))
                break

    for nome ,( rect, img ) in enermy.items():
        if rect.collidepoint(i, j):
            running = capture(screen, rect, nome, img, rects_adversario, rects_voce, jogador_atual)
            captura = "X"
            break
        else :
            running = True

    not_moved.insert(1 ,nome_peca)
    img = pygame.image.load(imagem)
    screen.blit(img, (i , j))
    
    for p in range(1):
        if not jogador_atual == rects_voce:
            letra_n = abs(8 - (int(i/75 + 1)) + 1)
            numero_n = (8 - (int(j/77 + 1)) + 1)
        else:
            letra_n = int(i/75 + 1)
            numero_n = int(j/77 + 1)

    if nome_id == "O - O" or nome_id == "O - O - O":
        registro = nome_id + " , "
    else:
        registro = (nome_id + captura + (str(chr(letra_n + 96)) + str(numero_n) + " , "))

    registro_de_movimentação.append(registro)

    BLACK = (0, 0, 0)
    for i, item in enumerate(registro_de_movimentação):
        text_surface = font.render(item, True, BLACK)
        m = 615 + (30 * i)
        n = 100

        if m > 820:
            n += 30
            i -= 7
            m = 615 + (30 * i)

        screen.blit(text_surface,( m, n))
        
    pygame.display.flip()
    return running

pecas_capturadas_adversario = []
pecas_capturadas_voce = []
def capture(screen, rect, nome, img, rects_adversario, rects_voce, jogador_atual):
    if jogador_atual == rects_voce:
        del rects_adversario[nome]
        x = 616 - 50
        pecas_capturadas_voce.append(nome)
        imagem = pygame.image.load(img)
        imagem_redimensionada = pygame.transform.scale(imagem, (40, 40))
        screen.blit(imagem_redimensionada, (600 + 15 * len(pecas_capturadas_voce), x))
    else:
        del rects_voce[nome]
        x = 30
        pecas_capturadas_adversario.append(nome)
        imagem = pygame.image.load(img)
        imagem_redimensionada = pygame.transform.scale(imagem, (40, 40))
        screen.blit(imagem_redimensionada, (600 + 15 * len(pecas_capturadas_adversario), x))

    if "rei_voce" in pecas_capturadas_adversario:
        return False
    elif "rei_adversario" in pecas_capturadas_voce:
        return False
    else:
        return True
    