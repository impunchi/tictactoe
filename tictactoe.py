import pygame 

# initialize pygame
pygame.init()

# create pygame screen with the size of 500x250
screen = pygame.display.set_mode((340, 340))

# change whole background to rgb(0,0,0) -> white
screen.fill((150,0,0))

# class knows screen variable
class Button:

    # init function initalize the Button class
    def __init__(self, color, x, y, width, height, arrayX, arrayY, text=''):
        self.rgb = color
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.text = text
        self.arrayX = arrayX
        self.arrayY = arrayY

    def draw(self):
        # draw button -> rect (distance to left border, distance to top border, width, height)
        # the zero at the end stands for no rounded corners
        pygame.draw.rect(screen, self.rgb, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':

            # select font, size and color of text
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))

            # the double slash is needed so that the solution of the division is a integer 
            # blit function expects a integer value and not a float
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 -text.get_height()//2)))

    # text function to control what is inside the rectangle
    def change_text(self, string):
            # refresh square (redraw it)
            self.draw()

            # select font, size and color of text
            font = pygame.font.SysFont('comicsans', 60)
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
        print(self.arrayX)
        return self.arrayX

    def getArrayY(self):
        print(self.arrayY)
        return self.arrayY

# change title
pygame.display.set_caption("Tic Tac Toe")

# change icon
icon = pygame.image.load('tictactoe.png')
pygame.display.set_icon(icon)


#reimplent a lot of things with this kind of list...
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

# draw all buttons
for x in range(9):
    buttons[x].draw()

# true as long as the game runs
running = True

def check(field, x, y):
    # check if the field is still empty
    if field[x][y] == 0:
        return True
    return False

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
                    if buttons[x].detect(pygame.mouse.get_pos()):
                        if(check(tictactoe, buttons[x].getArrayY(), buttons[x].getArrayX())):
                            if player1_turn:
                                print(x)
                                tictactoe[buttons[x].getArrayY()][buttons[x].getArrayX()] = "X"
                                print(tictactoe)
                                buttons[x].change_text("X")
                                player1_turn = False
                            else:
                                tictactoe[buttons[x].getArrayY()][buttons[x].getArrayX()] = "O"
                                buttons[x].change_text("O")
                                player1_turn = True
                    

                            if win(tictactoe):
                                #reset field
                                for x in range(len(buttons)):
                                    buttons[x].reset()

                                player1_turn = True

                                for y in range(3):
                                    for x in range(3):
                                        tictactoe[y][x] = 0
                                        
        # updates screen: must be called after everything has been drawn
        pygame.display.flip()