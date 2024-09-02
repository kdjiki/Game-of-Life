import pygame
import random
import json
import os
import tkinter 
import tkinter.messagebox


pygame. init()

YELLOW = (255, 222, 56)
BLACK = (0,0,0)
BLUE = (64, 92, 255) 
WHITE = (255, 255, 255)
L_BLUE = (128, 183, 255)
GREY = (255, 255, 255, 180) 

WIDTH = 800 
HEIGHT = 800
TILE_SIZE = 20
CONTROL_BAR_HEIGHT = 40
GRID_W = WIDTH // TILE_SIZE
GRID_H = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
music_files = "Martin Roth - An Analog Guy In A Digital World.mp3"

pygame.mixer.music.load(music_files)

def draw_instructions(positions):
    screen.fill(BLUE)
    draw_grid(positions)
    
    overlay_width = WIDTH - 100
    overlay_height = 400
    overlay_x = (WIDTH - overlay_width) // 2
    overlay_y = (HEIGHT - overlay_height) // 2

    overlay = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
    overlay.fill(GREY) 
    
    screen.blit(overlay, (overlay_x, overlay_y))
    pygame.display.set_caption("Game of Life")
    
    font = pygame.font.SysFont(None, 36)
    
    instructions = [
        "Conway's Game of Life Instructions:",
        "",
        "Click on the grid to add/remove cells.",
        "Press 'Space' to start/pause the game.",
        "Press 'C' to clear the grid.",
        "Press 'A' to auto-generate a random grid.",
        "Press 'S' to save the current grid setup.",
        "Press 'L' to load a saved grid setup.",
        "Click 'Mute' to mute/unmute the music.",
        "Click 'Setups' to view and load saved setups.",
        "",
        "Press 'Space' or click to continue..."
    ]
    
    for i, line in enumerate(instructions):
        text = font.render(line, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, overlay_y + 30 + i * 30))
        screen.blit(text, text_rect)
    
    pygame.display.update()

def delete_grid(setup_name, filename="grid_setups.json"):
    
    with open(filename, 'r') as f:
        setups = json.load(f)
        
    if setup_name in setups:
        del setups[setup_name]
        with open(filename, 'w') as f:
            json.dump(setups, f, indent=4)
        print(f"Setup '{setup_name}' deleted successfully.")
    else:
        print(f"Setup '{setup_name}' not found.")

def message(): 
    tkinter.messagebox.showinfo("Error",  "There is no setup with this name! Try again.")

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col*TILE_SIZE, row*TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))
    
    for row in range(GRID_H):
        pygame.draw.line(screen, BLACK, (0, row*TILE_SIZE),(WIDTH, row*TILE_SIZE))
    for col in range(GRID_W):
        pygame.draw.line(screen, BLACK, (col*TILE_SIZE,0),(col*TILE_SIZE, HEIGHT))

def gen(num):
    positions = set()
    while len(positions) < num:
        positions.add((random.randrange(0, GRID_H), random.randrange(0, GRID_W)))
    return positions
    
def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()
    
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)
        
        neighbors = list(filter(lambda x: x in positions, neighbors))
        
        if len(neighbors) == 2 or len(neighbors) == 3:
            new_positions.add(position)
            
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
            
    return new_positions
    
def get_neighbors(pos):
    x,y = pos
    neighbors = []
    for var_x in [-1,0,1]:
        if x + var_x < 0 or x + var_x > GRID_W:
            continue
        for var_y in [-1,0,1]:
            if y + var_y < 0 or y + var_y > GRID_H:
                continue
            if var_x == 0 and var_y == 0:
                continue
            neighbors.append((x+var_x, y+var_y))
    return neighbors

def load_grid(setup_name, filename="grid_setups.json"):
    try:
        with open(filename, 'r') as f:
            setups = json.load(f)
        
        if setup_name in setups:
            positions = set(tuple(pos) for pos in setups[setup_name])
            print(f"Setup '{setup_name}' loaded successfully.")
            return positions
        else:
            print(f"Setup '{setup_name}' not found.")
            message()
            return set()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return set()

def save_grid(positions, setup_name, filename="grid_setups.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            setups = json.load(f)
    else:
        setups = {}
        
    setups[setup_name] = list(positions)
    
    with open(filename, 'w') as f:
        json.dump(setups, f, indent=4)

    print(f"Setup '{setup_name}' saved successfully.")
  
def list_saved_setups(filename="grid_setups.json"):
    try:
        with open(filename, 'r') as f:
            setups = json.load(f)
        return list(setups.keys())
    except FileNotFoundError:
        return []

def main():
    running = True
    playing = False
    count = 0
    steps = 0
    update_freq = 58

    positions = set()
    setup_name = ""
    input_active = False
    input_mode = None
    ignore_first_keypress = False
    show_setup_list = False
    
    MUTE_BUTTON_RECT = pygame.Rect(WIDTH - 110, HEIGHT - CONTROL_BAR_HEIGHT + 7, 100, 28)  
    PLAY_BUTTON_RECT = pygame.Rect(WIDTH - WIDTH/2 - 20, HEIGHT - CONTROL_BAR_HEIGHT + 7, 50, 28)
    CLEAR_BUTTON_RECT = pygame.Rect(WIDTH - WIDTH/2 - 90, HEIGHT - CONTROL_BAR_HEIGHT + 7, 50, 28)
    LIST_BUTTON_RECT = pygame.Rect(15, HEIGHT - CONTROL_BAR_HEIGHT + 7, 100, 28)
    INSTRUCTIONS_BUTTON_RECT = pygame.Rect(130, HEIGHT - CONTROL_BAR_HEIGHT + 7, 160, 28)
    mute = False
    
    font = pygame.font.SysFont(None, 36)
    input_font = pygame.font.SysFont(None, 34)
    
    pygame.mixer.music.play(-1)
    
    show_instructions = True

    while running:
        clock.tick(FPS)
          
        if show_instructions:
            draw_instructions(positions)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    show_instructions = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    show_instructions = False
            continue
        
        if playing:
            count +=1
            pygame.mixer.music.unpause()
            if mute:
                pygame.mixer.music.set_volume(0)  
        else:
            music_pos = pygame.mixer.music.get_pos() / 1000.0  
            pygame.mixer.music.pause() 
            
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)
            if playing:
                steps += 1
            
        pygame.display.set_caption("Playing Game of Life" if playing else "Paused") 
            
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN  and not input_active:
                if MUTE_BUTTON_RECT.collidepoint(event.pos):
                    mute = not mute
                    if mute:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(1)
                
                if PLAY_BUTTON_RECT.collidepoint(event.pos):
                    playing = not playing
                    
                if INSTRUCTIONS_BUTTON_RECT.collidepoint(event.pos):
                    show_instructions = True
                    
                if CLEAR_BUTTON_RECT.collidepoint(event.pos):
                    positions = set()
                    playing = False
                    count = 0
                    steps = 0
                    pygame.mixer.music.rewind()
                    
                if LIST_BUTTON_RECT.collidepoint(event.pos):
                    show_setup_list = not show_setup_list
                
                if show_setup_list:
                    setup_list = list_saved_setups()
                    for i, setup in enumerate(setup_list):
                        setup_rect = pygame.Rect(20, 20 + i * 30, 200, 30)
                        if setup_rect.collidepoint(event.pos):
                            positions = load_grid(setup)
                            show_setup_list = False
                            break
                       
                x,y = pygame.mouse.get_pos()
                if y < HEIGHT - CONTROL_BAR_HEIGHT:
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col,row)
                    
                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not input_active:
                    playing = not playing
                    
                if event.key == pygame.K_c and not input_active:
                    positions = set()
                    playing = False
                    count = 0
                    steps = 0
                    pygame.mixer.music.rewind()
                    
                if event.key == pygame.K_a and not input_active:
                    positions = gen(random.randrange(2,8)*GRID_W)
                    steps = 0
                    
                if event.key == pygame.K_s and not input_active:
                    playing = False 
                    input_active = True
                    input_mode = 'save'
                    setup_name = ""
                    ignore_first_keypress = True
                    
                if event.key == pygame.K_l and not input_active:
                    playing = False 
                    input_active = True
                    input_mode = 'load'
                    setup_name = ""
                    
                elif input_active:
                    if ignore_first_keypress:
                        ignore_first_keypress = False
                    else:                        
                        if event.key == pygame.K_RETURN:
                            if input_mode == 'save':
                                save_grid(positions, setup_name)
                            elif input_mode == 'load':
                                positions = load_grid(setup_name)
                                steps = 0
                            input_active = False
                            input_mode = None
                    
                        elif event.key == pygame.K_ESCAPE:
                            input_active = False
                            input_mode = None
                        elif event.key == pygame.K_BACKSPACE:
                            setup_name = setup_name[:-1]
                        elif event.unicode.isprintable() and event.unicode not in ['\r', '\n']: 
                            setup_name += event.unicode
                                       
        screen.fill(BLUE)
        draw_grid(positions)
              
        step_text = font.render(f"Steps: {steps}", True, BLACK)
        
        bg_rect = step_text.get_rect(topleft=(10, 10))
        bg_surface = pygame.Surface((bg_rect.width + 10, bg_rect.height + 10))
        bg_surface.set_alpha(125) 
        bg_surface.fill(WHITE) 
        
        screen.blit(bg_surface, (5, 5)) 
        screen.blit(step_text, (10,10))
        
        pygame.draw.rect(screen, L_BLUE, (0, HEIGHT - CONTROL_BAR_HEIGHT, WIDTH, CONTROL_BAR_HEIGHT))

        mute_text = font.render("Mute" if not mute else "Unmute", True, WHITE)
        pygame.draw.rect(screen, BLUE, MUTE_BUTTON_RECT)
        screen.blit(mute_text, (MUTE_BUTTON_RECT.x + 5, MUTE_BUTTON_RECT.y + 5))
        
        pygame.draw.rect(screen, BLUE, PLAY_BUTTON_RECT)
        if playing:
            pygame.draw.rect(screen, WHITE, (PLAY_BUTTON_RECT.x + 10, PLAY_BUTTON_RECT.y + 5, 10, 18))
            pygame.draw.rect(screen, WHITE, (PLAY_BUTTON_RECT.x + 30, PLAY_BUTTON_RECT.y + 5, 10, 18))
        else:
            pygame.draw.polygon(screen, WHITE, [
                (PLAY_BUTTON_RECT.x + 10, PLAY_BUTTON_RECT.y + 5),
                (PLAY_BUTTON_RECT.x + 10, PLAY_BUTTON_RECT.y + 23),
                (PLAY_BUTTON_RECT.x + 40, PLAY_BUTTON_RECT.y + 14)
            ])
        pygame.draw.rect(screen, BLUE, CLEAR_BUTTON_RECT)
        pygame.draw.rect(screen, WHITE, (CLEAR_BUTTON_RECT.x + 15, PLAY_BUTTON_RECT.y + 5, 18, 18))
        
        list_text = font.render("Load", True, WHITE)
        pygame.draw.rect(screen, BLUE, LIST_BUTTON_RECT)
        screen.blit(list_text, (LIST_BUTTON_RECT.x + 5, LIST_BUTTON_RECT.y + 5))
        
        instructions_text = font.render("Instructions", True, WHITE)
        pygame.draw.rect(screen, BLUE, INSTRUCTIONS_BUTTON_RECT)
        screen.blit(instructions_text, (INSTRUCTIONS_BUTTON_RECT.x + 5, INSTRUCTIONS_BUTTON_RECT.y + 5))

        if show_setup_list:
            
            title_text = input_font.render("SAVED SETUPS", True, BLACK)
            text_rect = title_text.get_rect(center=(WIDTH // 2, 100))
            pygame.draw.rect(screen, L_BLUE, (text_rect.x - 15, text_rect.y - 5, 210, 30))
            screen.blit(title_text, text_rect)

            setup_list = list_saved_setups()
            for i, setup in enumerate(setup_list):
                setup_text = input_font.render(setup, True, BLACK)
                bg_rect = pygame.Rect(WIDTH/2 - 200, 150 + i * 30, 200, setup_text.get_height())
                delete_button_rect = pygame.Rect(WIDTH / 2 + 110, 150 + i * 30, 90, setup_text.get_height())

                pygame.draw.rect(screen, L_BLUE, bg_rect)
                pygame.draw.rect(screen, L_BLUE, delete_button_rect)
                delete_text = input_font.render("Delete", True, WHITE)
                screen.blit(delete_text, (delete_button_rect.x + 5, delete_button_rect.y + 2))
                screen.blit(setup_text, (WIDTH / 2 - 200, 150 + i * 30))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if bg_rect.collidepoint(mouse_pos):
                        positions = load_grid(setup)
                        show_setup_list = False
                        steps = 0
                        break
                    elif delete_button_rect.collidepoint(mouse_pos):
                        delete_grid(setup)
                        setup_list = list_saved_setups()
                        mouse_pos = pygame.mouse.set_pos(mouse_pos)
                        break
                           
        if input_active:
            
            title_text = input_font.render("ENTER NAME:", True, BLACK)
            text_rect = title_text.get_rect(center=(WIDTH // 2, 100))
            pygame.draw.rect(screen, L_BLUE, (text_rect.x - 15, text_rect.y - 5, 210, 30))
            screen.blit(title_text, text_rect)

            
            input_text = input_font.render(setup_name, True, BLACK)
            text_rect = input_text.get_rect(center=(WIDTH // 2, 150))
            bg_rect = pygame.Rect(text_rect)
            bg_rect.inflate_ip(10, 10)
            
            bg_surface = pygame.Surface(bg_rect.size)
            bg_surface.set_alpha(125)
            bg_surface.fill(WHITE)
    
            screen.blit(bg_surface, bg_rect.topleft)
            screen.blit(input_text, text_rect.topleft)
            
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
