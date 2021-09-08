import pygame
import random
import json

#Colors:
yellow = (255, 255, 0)
grey = (128, 128, 128)
white = (255, 255, 255)

#Variables for the game window size:
gw_width = 800
gw_height = 500

#Initializes pygame, and creates the game windouw:
pygame.init()
game_window = pygame.display.set_mode((gw_width, gw_height))
pygame.display.set_caption("The Ultimate Snake Game!")

#Global variables:
snake_size = 20
snake_speed = 11

clock = pygame.time.Clock()


def game_over_screen(score):
    '''This function renders the game over screen'''
    main_font = pygame.font.SysFont("calibri", 25)

    game_window.fill(grey)
    game_over = main_font.render("GAME OVER LOSER! PRESS SPACE TO PLAY AGAIN OR ESC TO EXIT", True, yellow)
    game_window.blit(game_over, [70, 125])

    points = main_font.render("YOUR SCORE WAS: " + str(score), True, yellow)
    game_window.blit(points, [300, 200])


def is_game_over(snake_body, snake_location_x, snake_location_y):
    '''This function returns True or False based on if statements that checks if player loses game'''
    #Game over if snake hits wall:
    if snake_location_x >= gw_width or snake_location_x < 0 or snake_location_y >= gw_height or snake_location_y < 0:
        return True

    #Game over if snake crashes into itself:
    elif (snake_location_x, snake_location_y) in snake_body[:-1]:
        return True

    #If none of above return False and continue game:
    else: 
        return False


def save_score(score):
    '''This function saves your score to a JSON-file'''
    try: 
        with open("scoreboard.json", "a") as file:
            scoreboard = {}
            
            scoreboard["score"] = score

            json.dump(scoreboard, file)
            file.write("\n")
            
    except FileNotFoundError:
        print("This file could not be found, check the placement in your file path")


def run_game():
    '''This function holds the variables and main loop that makes the game run'''
    #Game states:
    snake_body = []
    
    snake_location_x = 400
    snake_location_y = 240

    move_snake_x = 0
    move_snake_y = 0

    #Variables to spawn food at random cells in game window:
    food_x = round(random.randrange(0, gw_width - snake_size) / snake_size) * snake_size
    food_y = round(random.randrange(0, gw_height - snake_size) / snake_size) * snake_size

    #Variable to check in loop if player has lost:
    game_over = False

    #Variable that makes the game close if False, otherwise runs in an infinite loop while True:
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: #If player presses an arrow key move snake:
                    move_snake_x = -snake_size
                    move_snake_y = 0
                elif event.key == pygame.K_UP:
                    move_snake_y = -snake_size
                    move_snake_x = 0
                elif event.key == pygame.K_RIGHT:
                    move_snake_x = snake_size
                    move_snake_y = 0
                elif event.key == pygame.K_DOWN:
                    move_snake_y = snake_size
                    move_snake_x = 0
                elif event.key == pygame.K_SPACE: #If player wants to play again, press spacebar
                    #Repetiton of code, read report on why:
                    snake_body = []
    
                    snake_location_x = 400
                    snake_location_y = 240

                    move_snake_x = 0
                    move_snake_y = 0

                    game_over = False
                elif event.key == pygame.K_ESCAPE: #If player wants to exit the game press ESC button
                    running = False

        #Continue the loop if player choses to play game again after a loss:
        if game_over == True:
            continue

        #Everything that shows in the game window:
        snake_location_x += move_snake_x
        snake_location_y += move_snake_y
        game_window.fill(grey) 

        #Draw food and snake head, and set snake speed to match clock:
        draw_food = pygame.draw.rect(game_window, white, [food_x, food_y, snake_size, snake_size]) 
        draw_snake_head = pygame.draw.rect(game_window, yellow, [snake_location_x, snake_location_y, snake_size, snake_size])
        clock.tick(snake_speed)

        #Grow snake body:
        snake_body.append((snake_location_x, snake_location_y))   
        for body in snake_body:
            draw_snake_body = pygame.draw.rect(game_window, yellow, [*body, snake_size, snake_size])

        #Save score to a variable:
        score = len(snake_body) - 1

        #If player loses, call function is_game_over to check, and if True, call function to show game_over_screen:
        game_over = is_game_over(snake_body, snake_location_x, snake_location_y)
        if game_over: 
            game_over_screen(score)

        #If snake eats food, spawn another food at random cell in game window:
        if snake_location_x == food_x and snake_location_y == food_y: 
            food_x = round(random.randrange(0, gw_width - snake_size) / snake_size) * snake_size
            food_y = round(random.randrange(0, gw_height - snake_size) / snake_size) * snake_size
        else:
            del snake_body[0] #Stops snake from growing if it has not eaten food

        pygame.display.update()

    save_score(score)

run_game()