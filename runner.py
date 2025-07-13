import pygame
import sys
import time
import tictactoe as ttt

def minimax_alpha_beta(board, alpha=float('-inf'), beta=float('inf')):
    if ttt.terminal(board):
        return None, ttt.utility(board)

    current_player = ttt.player(board)
    best_move = None

    if current_player == ttt.X:
        max_eval = float('-inf')
        for action in ttt.actions(board):
            _, eval = minimax_alpha_beta(ttt.result(board, action), alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = action
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        for action in ttt.actions(board):
            _, eval = minimax_alpha_beta(ttt.result(board, action), alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = action
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move, min_eval

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 23)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 35)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 50)

# Colors
COLORS = {
    "bg": (62, 196, 230),
    "line": (37, 121, 143),
    "X": (69, 245, 79),
    "O": (232, 34, 135),
    "button": (242, 203, 87),
    "hover": (230, 190, 80),
    "text": (255, 255, 255)
}

# Game state
user = None
board = ttt.initial_state()
ai_turn = False
click_handled = False

def draw_button(rect, text, hover=False):
    color = COLORS["hover"] if hover else COLORS["button"]
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = mediumFont.render(text, True, COLORS["text"])
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_board(board):
    tiles = []
    tile_size = 100
    origin_x = WIDTH / 2 - 1.5 * tile_size
    origin_y = HEIGHT / 2 - 1.5 * tile_size

    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(origin_x + j * tile_size, origin_y + i * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, COLORS["line"], rect, 3, border_radius=5)

            if board[i][j] in (ttt.X, ttt.O):
                move = moveFont.render(board[i][j], True, COLORS[board[i][j]])
                move_rect = move.get_rect(center=rect.center)
                screen.blit(move, move_rect)

            row.append(rect)
        tiles.append(row)

    return tiles

def display_text(text, y):
    render = largeFont.render(text, True, COLORS["text"])
    rect = render.get_rect(center=(WIDTH / 2, y))
    screen.blit(render, rect)

# Main game loop
while True:
    screen.fill(COLORS["bg"])
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if user is None:
        display_text("Play Tic-Tac-Toe", 50)

        btn_x = pygame.Rect(WIDTH / 8, HEIGHT / 2, WIDTH / 4, 50)
        btn_o = pygame.Rect(5 * WIDTH / 8, HEIGHT / 2, WIDTH / 4, 50)

        draw_button(btn_x, "Play as X", btn_x.collidepoint(mouse_pos))
        draw_button(btn_o, "Play as O", btn_o.collidepoint(mouse_pos))

        if click and not click_handled:
            click_handled = True
            if btn_x.collidepoint(mouse_pos):
                user = ttt.X
            elif btn_o.collidepoint(mouse_pos):
                user = ttt.O
        if not click:
            click_handled = False

    else:
        tiles = draw_board(board)
        game_over = ttt.terminal(board)
        current_player = ttt.player(board)

        if game_over:
            result = ttt.winner(board)
            status = "Game Over: Tie." if result is None else f"Game Over: {result} wins."
        else:
            status = f"Your Turn ({user})" if user == current_player else "Computer Thinking..."

        display_text(status, 30)

        if not game_over:
            if user != current_player and ai_turn:
                pygame.display.flip()
                time.sleep(0.3)
                move, _ = minimax_alpha_beta(board)
                board = ttt.result(board, move)
                ai_turn = False
            elif user != current_player:
                ai_turn = True

            if click and not click_handled and user == current_player:
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse_pos):
                            board = ttt.result(board, (i, j))
                            break
                click_handled = True
            if not click:
                click_handled = False

        if game_over:
            again_button = pygame.Rect(WIDTH / 3, HEIGHT - 65, WIDTH / 3, 50)
            draw_button(again_button, "Play Again", again_button.collidepoint(mouse_pos))

            if click and not click_handled and again_button.collidepoint(mouse_pos):
                user = None
                board = ttt.initial_state()
                ai_turn = False
                click_handled = True
            if not click:
                click_handled = False

    pygame.display.flip()
