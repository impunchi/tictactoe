import pygame 
import numpy as np

# initialize pygame
pygame.init()

# create pygame screen with the size of 340x400
screen = pygame.display.set_mode((340, 400))

# change whole background to rgb(150,0,0) -> red
screen.fill((150,0,0))

# class knows screen variable
class Button:

    # init function initalize the Button class
    def __init__(self, color, x, y, width, height, arrayX, arrayY, fontSize=60):
        self.rgb = color
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.arrayX = arrayX
        self.arrayY = arrayY
        self.fontSize = fontSize
        self.draw()

    def draw(self):
        # draw button -> rect (distance to left border, distance to top border, width, height)
        # the zero at the end stands for no rounded corners
        pygame.draw.rect(screen, self.rgb, (self.x, self.y, self.width, self.height), 0)

    # text function to control what is inside the rectangle
    def change_text(self, string):
            # refresh square (redraw it)
            self.draw()

            # select font, size and color of text
            font = pygame.font.SysFont('comicsans', self.fontSize)
            text = font.render(string, 1, (0,0,0))

            # the double slash is needed so that the solution of the division is a integer 
            # blit function expects a integer value and not a float
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 -text.get_height()//2)))

    # use pygame.mouse.get_pos() to detect if the user hovers over the button
    def detect(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x+self.width:
            if mouse_pos[1] > self.y and mouse_pos[1] < self.y+self.height:
                return True
        
        return False

    def reset(self):
        self.draw()

    def getArrayX(self):
        return self.arrayX

    def getArrayY(self):
        return self.arrayY

# check if this field is empty
def check(field, x, y):

    if field[x][y] == 0:
        return True

    return False

# check if someone has won
def win(field):
    
    # check rows
    for y in range(3):
        if field[y][0] == field[y][1] and field[y][0] == field[y][2] and field[y][0] != 0:
            return True

    # check columns
    for x in range(3):
        if field[0][x] == field[1][x] and field[0][x] == field[2][x] and field[0][x] != 0:
            return True

    # check diagonals
    if field[0][0] == field[1][1] and field[0][0] == field[2][2] and field[0][0] != 0:
        return True
    elif field[0][2] == field[1][1] and field[0][2] == field[2][0] and field[0][2] != 0:
        return True

    return False

# set X or O on the selected field
def set(field, buttons, player1_turn):
    if buttons.detect(pygame.mouse.get_pos()):
        if(check(field, buttons.getArrayX(), buttons.getArrayY())):
            if player1_turn:
                field[buttons.getArrayX()][buttons.getArrayY()] = "X"
                buttons.change_text("X")
                player1_turn = False
            else:
                field[buttons.getArrayX()][buttons.getArrayY()] = "O"
                buttons.change_text("O")
                player1_turn = True
    
    return player1_turn

# check for current gamestate: has somebody won or is it a draw?
def gamestate(field, buttons):
    won = False
    
    if win(field):
        won = True
    else:
        for y in range(3):
            for x in range(3):
                if field[y][x] == 0:
                    return False

    # reset drawn field and array
    for x in range(len(buttons)):
        buttons[x].reset()

    for y in range(3):
        for x in range(3):
            field[y][x] = 0

    return won

# change title
pygame.display.set_caption("Tic Tac Toe")

# change icon
icon = pygame.image.load('tictactoe.png')
pygame.display.set_icon(icon)

# prepare list for button objects
buttons = []

# first row
for x in range(3):
    i = Button((255, 255, 255), 10+x*110, 10, 100, 100, 0, x)
    buttons.append(i)

# second row 
for x in range(3):
    i = Button((255, 255, 255), 10+x*110, 120, 100, 100, 1, x)
    buttons.append(i)

# thrid row
for x in range(3):
    i = Button((255, 255, 255), 10+x*110, 230, 100, 100, 2, x)
    buttons.append(i)

# create score labels
player1 = Button((255, 255, 255), 10, 340, 320, 20, 0, 0, 25)
player2 = Button((255, 255, 255), 10, 370, 320, 20, 0, 0, 25)

# score for both players
player1_score = 0
player2_score = 0

# change labels to equal the player score
player1.change_text("Player 1 ('X'): " + str(player1_score))
player2.change_text("Player 2 ('O'): " + str(player2_score))

# true as long as the game runs
running = True

# playing field
tictactoe = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

player1_turn = True

# infinite game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                for x in range(9):
                    player1_turn = set(tictactoe, buttons[x], player1_turn)

                if gamestate(tictactoe, buttons):
                    # check the player turn and give the right player a point
                    if not player1_turn:
                        player1_score += 1
                        player1.change_text("Player 1 ('X'): " + str(player1_score))
                        player1_turn = True

                    else:
                        player2_score += 1
                        player2.change_text("Player 2 ('O'): " + str(player2_score))
                        player1_turn = True    

        # updates screen: must be called after everything has been drawn
        pygame.display.flip()