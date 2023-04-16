import cv2
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO

# Set up buttons
BUTTONS = [5, 6, 16, 24]  # [Up, Down, Select, Unused]
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((240, 240))

# Load and play the animation
video_capture = cv2.VideoCapture("animation.mp4")
while video_capture.isOpened():
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (240, 240))
        video_texture = pygame.surfarray.make_surface(frame)
        screen.blit(video_texture, (0, 0))
        pygame.display.flip()
    else:
        break
video_capture.release()

# Menu variables
main_menu_items = ["Start", "Settings", "Exit"]
settings_menu_items = ["Dummy Option 1", "Dummy Option 2", "Back"]
menu_items = main_menu_items
selected_item = 0

# Menu states
MAIN_MENU = 0
SETTINGS_MENU = 1
CONFIRM_EXIT = 2
menu_state = MAIN_MENU

font = pygame.font.Font(None, 36)

def draw_menu():
    screen.fill((0, 0, 0))
    for index, item in enumerate(menu_items):
        if index == selected_item:
            color = (255, 255, 255)
        else:
            color = (100, 100, 100)
        text = font.render(item, True, color)
        screen.blit(text, (100, 50 + index * 50))
    pygame.display.flip()

def start_game():
    print("Starting game...")

def show_settings():
    global menu_state, menu_items, selected_item
    menu_state = SETTINGS_MENU
    menu_items = settings_menu_items
    selected_item = 0

def exit_game():
    global menu_state
    menu_state = CONFIRM_EXIT

def confirm_exit():
    print("Exiting game...")
    pygame.quit()

def back_to_main_menu():
    global menu_state, menu_items, selected_item
    menu_state = MAIN_MENU
    menu_items = main_menu_items
    selected_item = 0

def button_pressed(channel):
    global selected_item, menu_state
    if channel == BUTTONS[0]:  # Up
        selected_item -= 1
        if selected_item < 0:
            selected_item = len(menu_items) - 1
    elif channel == BUTTONS[1]:  # Down
        selected_item = (selected_item + 1) % len(menu_items)
    elif channel == BUTTONS[2]:  # Select
        if menu_state == MAIN_MENU:
            if menu_items[selected_item] == "Start":
                start_game()
            elif menu_items[selected_item] == "Settings":
                show_settings()
            elif menu_items[selected_item] == "Exit":
                exit_game()
        elif menu_state == SETTINGS_MENU:
            if menu_items[selected_item] == "Back":
                back_to_main_menu()
        elif menu_state == CONFIRM_EXIT:
            if selected_item == 0:
                confirm_exit()
            else:
                back_to_main_menu()

    draw_menu()

for pin in BUTTONS[:3]:
    GPIO.add_event_detect(pin, GPIO.FALLING, button_pressed, bouncetime=300)

try:
    draw_menu()
    while True:
        if menu_state == CONFIRM_EXIT:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 24)
            text = font.render("Are you sure you want to exit?", True, (255, 255, 255))
            screen.blit(text, (20, 100))
            for index, item in enumerate(["Yes", "No"]):
                if index == selected_item:
                    color = (255, 255, 255)
                else:
                    color = (100, 100, 100)
                text = font.render(item, True, color)
                screen.blit(text, (80 + index * 70, 130))
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                confirm_exit()
                GPIO.cleanup()
                sys.exit()
        pygame.time.wait(100)

except KeyboardInterrupt:
    GPIO.cleanup()
    pygame.quit()


