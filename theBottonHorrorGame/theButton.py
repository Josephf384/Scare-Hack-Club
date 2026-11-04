# File Name: theButton.py
# 
# This program serves as the logic for "The Button" game,
# which involves a series of logic orders, which if disobeyed result
# in something scary
#
# Author: Joseph Fong
import pygame #import pygame lib 
import math #import math module
import random #import random module
pygame.init() #initialize pygame functions

screen = pygame.display.set_mode((800, 600)) #set display to 800by600 pixels
clock = pygame.time.Clock()
pygame.display.set_caption("The Button") #set tab title to "The Button"

label_font = pygame.font.SysFont(None, 30, bold=True)
label_text = label_font.render("PRESS", True, (255, 235, 235))

title_font = pygame.font.SysFont(None, 42, bold=True)
title_text = title_font.render("DON'T PRESS IT", True, (230, 210, 215))

subtitle_font = pygame.font.SysFont(None, 24)
subtitle_text = subtitle_font.render("It is watching.", True, (150, 130, 140))

status_font = pygame.font.SysFont(None, 24, bold=True)
status_text = status_font.render("SYSTEM: STANDBY", True, (150, 160, 150))

order_font = pygame.font.SysFont(None, 26, bold=True)
order_text = order_font.render(
    "ORDER 01: DO NOT PRESS", True, (210, 190, 170)
)
game_state = "playing"
round_length = 10
round_started_at = pygame.time.get_ticks()
timer_font = pygame.font.SysFont(None, 26, bold=True)

memory_number = random.randint(2, 10)
memory_started_at = 0
memory_length = 5

current_command_index = 0
command_clicks = 0
recall_clicks = 0
command_started_at = 0

commands = [
    {"prompt": "CLICK 3 TIMES", "clicks": 3, "rat": False, "seconds": 6},
    {"prompt": "WAIT. DO NOT CLICK", "clicks": 0, "rat": False, "seconds": 2},
    {"prompt": "CLICK ONCE", "clicks": 1, "rat": False, "seconds": 6},
    {"prompt": "CLICK TWICE", "clicks": 2, "rat": False, "seconds": 6},
    {"prompt": "CLICK FOUR TIMES", "clicks": 0, "rat": True, "seconds": 6},
]

button_area = pygame.Rect(302, 192, 196, 196)

button_down = False
press_depth = 0.0

motes = []

for _ in range(24):
    x = random.randint(20, 780)
    y = random.randint(160, 580)
    speed = random.uniform(0.3, 1.0)
    motes.append([x, y, speed])

running = True

while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_area.collidepoint(event.pos):
                if game_state == "playing":
                    button_down = True
                    game_state = "broken"
                    order_text = order_font.render(
                        "ORDER BROKEN", True, (255, 60, 70)
                    )
                    status_text = status_font.render(
                        "SYSTEM: SIGNAL RECEIVED", True, (255, 90, 110)
                    )
                    label_text = label_font.render(
                        "CLICKED!", True, (255, 235, 255)
                    )
                    print("Button Clicked")

                elif game_state == "commands":
                    button_down = True
                    command_clicks += 1
                elif game_state == "recall":
                    button_down = True
                    recall_clicks += 1
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            button_down = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if game_state == "recall":
                if recall_clicks == memory_number:
                    game_state = "complete"
                    order_text = order_font.render(
                        "MEMORY MATCH", True, (160, 230, 170)
                    )
                    status_text = status_font.render(
                        "SYSTEM: CORRECT", True, (160, 230, 170)
                    )
                    label_text = label_font.render(
                        "SAFE", True, (200, 255, 200)
                    )
                else:
                    game_state = "broken"
                    order_text = order_font.render(
                        "MEMORY WRONG", True, (255, 60, 70)
                    )
                    status_text = status_font.render(
                        "SYSTEM: SIGNAL RECEIVED", True, (255, 90, 110)
                    )
                    label_text = label_font.render(
                        "FAILED", True, (255, 100, 110)
                    )
    elapsed_seconds = (
        pygame.time.get_ticks() - round_started_at
    ) // 1000
    seconds_left = max(0, round_length - elapsed_seconds)

    if game_state == "playing" and seconds_left == 0:
        game_state = "memorize"
        subtitle_text = subtitle_font.render(
            "RAT = IGNORE CLICK ORDERS", True, (255, 220, 160)
        )

        memory_started_at = pygame.time.get_ticks()
        order_text = order_font.render(
            f"MEMORIZE: {memory_number}", True, (255, 220, 160)
        )
        status_text = status_font.render(
            "SYSTEM: MEMORY TEST", True, (255, 220, 160)
        )
        label_text = label_font.render(
            "LOOK", True, (255, 235, 255)
        )

    if game_state == "memorize":
        memory_elapsed = pygame.time.get_ticks() - memory_started_at

        if memory_elapsed >= memory_length * 1000:
            game_state = "commands"
            subtitle_text = subtitle_font.render(
                "It is watching.", True, (150, 130, 140)
            )
            command_started_at = pygame.time.get_ticks()
            command_clicks = 0
            order_text = order_font.render(
                commands[current_command_index]["prompt"],
                True, 
                (210, 190, 170)
            )
            status_text = status_font.render(
                f"COMMAND {current_command_index + 1} OF {len(commands)}",
                True,
                (210, 190, 170)
            )
            label_text = label_font.render(
                "READY", True, (255, 235, 255)
            )
    if game_state == "commands":
        active_command = commands[current_command_index]
        command_elapsed = (
            pygame.time.get_ticks() - command_started_at
        ) // 1000

        if command_elapsed >= active_command["seconds"]:
            if command_clicks == active_command["clicks"]:
                current_command_index += 1

                if current_command_index < len(commands):
                    command_clicks = 0
                    command_started_at = pygame.time.get_ticks()
                    order_text = order_font.render(
                        commands[current_command_index]["prompt"],
                        True,
                        (210, 190, 170)
                    )
                    status_text = status_font.render(
                        f"COMMAND {current_command_index + 1} OF {len(commands)}",
                        True,
                        (210, 190, 170)
                    )
                else:
                    game_state = "recall"
                    recall_clicks = 0
                    order_text = order_font.render(
                        "CLICK YOUR NUMBER, THEN ENTER",
                        True,
                        (255, 220, 160)
                    )
                    status_text = status_font.render(
                        "PRESS ENTER TO SUBMIT",
                        True,
                        (255, 220, 160)
                    )
            else:
                game_state = "broken"
                order_text = order_font.render(
                    "ORDER BROKEN", True, (255, 60, 70)
                )
                status_text = status_font.render(
                    "SYSTEM: SIGNAL RECEIVED", True, (255, 90, 110)
                )
                label_text = label_font.render(
                    "FAILED", True, (255, 100, 110)
                )

    if game_state == "playing":
        timer_message = f"TIME LEFT: {seconds_left}"
        timer_color = (210, 190, 170)
    elif game_state == "broken":
        timer_message = "ORDER BROKEN"
        timer_color = (255, 80, 90)
    elif game_state == "memorize":
        timer_message = "REMEMBER IT"
        timer_color = (255, 220, 160)
    elif game_state == "commands":
        command_elapsed = (
            pygame.time.get_ticks() - command_started_at
        ) // 1000
        command_seconds_left = max(
            0, commands[current_command_index]["seconds"] - command_elapsed
        )
        timer_message = (
            f"TIME: {command_seconds_left} CLICKS: {command_clicks}"
        )
        timer_color = (210, 190, 170)
    elif game_state == "recall":
        timer_message = f"CLICKS ENTERED: {recall_clicks}"
        timer_color = (255, 220, 160)
    else:
        timer_message = "ORDER COMPLETE"
        timer_color = (160, 230, 170)

    timer_text = timer_font.render(timer_message, True, timer_color)

    target_depth = 7 if button_down else 0
    press_depth += (target_depth - press_depth) * 0.3
    press_offset = round(press_depth)

    time_seconds = pygame.time.get_ticks() / 1000
    pulse = (math.sin(time_seconds * 1.5) + 1) / 2
    background_color = (
        14 + round(pulse * 7),
        12, 
        23 + round(pulse * 10)
    )
    screen.fill(background_color)

    for mote in motes:
        mote[1] -= mote[2]

        if mote[1] < 160:
            mote[0] = random.randint(20, 780)
            mote[1] = 580

        pygame.draw.circle(
            screen,
            (115, 110, 125),
            (round(mote[0]), round(mote[1])),
            2
        )

    title_y = 100 + round(math.sin(time_seconds * 2) * 4)

    title_rect = title_text.get_rect(center=(400, title_y))
    subtitle_rect = subtitle_text.get_rect(center=(400, 140))

    screen.blit(title_text, title_rect)
    screen.blit(subtitle_text, subtitle_rect)

    hovering = button_area.collidepoint(pygame.mouse.get_pos())

    if hovering:
        cap_color = (245, 45, 65)
        pygame.draw.circle(screen, (255, 95, 110), (400, 290 + press_offset), 104, 5)
    else:
        cap_color = (190, 20, 40)

    # Button's short metal body
    pygame.draw.rect(
        screen, (65, 70, 82), (350, 310, 100, 115), border_radius=14
    )

    # Wide metal ring mounted over the body
    pygame.draw.circle(screen, (38, 42, 52), (400, 300), 132)
    pygame.draw.circle(screen, (150, 157, 168), (400, 294), 122)
    pygame.draw.circle(screen, (48, 20, 29), (400, 289), 110)

    # Red cap: mostly flat (looks like button not ball)
    pygame.draw.circle(screen, cap_color, (400, 290 + press_offset), 98)
    pygame.draw.ellipse(screen, (255, 115, 125), (365, 210 + press_offset, 70, 16))

    label_rect = label_text.get_rect(center=(400, 280 + press_offset))
    screen.blit(label_text, label_rect)

    if game_state == "commands" and commands[current_command_index]["rat"]:
        pygame.draw.ellipse(screen, (115, 115, 125), (575, 300, 70, 40))
        pygame.draw.circle(screen, (130, 130, 140), (640, 300), 23)
        pygame.draw.circle(screen, (155, 155, 165), (630, 280), 10)
        pygame.draw.circle(screen, (155, 155, 165), (650, 280), 10)
        pygame.draw.circle(screen, (20, 20, 20), (646, 294), 3)
        pygame.draw.circle(screen, (230, 100, 120), (661, 302), 4)

    order_rect = order_text.get_rect(center=(400, 462))
    screen.blit(order_text, order_rect)

    timer_rect = timer_text.get_rect(center=(400, 490))
    screen.blit(timer_text, timer_rect)

    pygame.draw.rect(
        screen, (28, 25, 34), (245, 500, 310, 44), border_radius=8
    )
    pygame.draw.rect(
        screen, (95, 72, 82), (245, 500, 310, 44),
        width=2, border_radius=8
    )

    status_rect = status_text.get_rect(center=(400, 522))
    screen.blit(status_text, status_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


