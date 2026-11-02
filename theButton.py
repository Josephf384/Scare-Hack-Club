# File Name: theButton.py
# 
# This program serves as the logic for "The Button" game,
# which involves a series of logic orders, which if disobeyed result
# in something scary
#
# Author: Joseph Fong
import pygame #import pygame lib 
pygame.init() #initialize pygame functions

screen = pygame.display.set_mode((800, 600)) #set display to 800by600 pixels
clock = pygame.time.Clock()
pygame.display.set_caption("The Button") #set tab title to "The Button"

label_font = pygame.font.SysFont(None, 30, bold=True)
label_text = label_font.render("PRESS", True, (255, 235, 235))

button_area = pygame.Rect(302, 182, 196, 196)
running = True

while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((18, 18, 28))

    # Button's short metal body
    pygame.draw.rect(
        screen, (65, 70, 82), (350, 310, 100, 115), border_radius=14
    )

    # Wide metal ring mounted over the body
    pygame.draw.circle(screen, (38, 42, 52), (400, 300), 132)
    pygame.draw.circle(screen, (150, 157, 168), (400, 294), 122)
    pygame.draw.circle(screen, (48, 20, 29), (400, 289), 110)

    # Red cap: mostly flat (looks like button not ball)
    pygame.draw.circle(screen, (190, 20, 40), (400, 200), 98)
    pygame.draw.ellipse(screen, (255, 115, 125), (365, 210, 70, 16))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


