from random import Random
from typing import Dict, Text
import pygame as p
from pygame import color
import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from pygame.font import Font
from pygame.image import load
import ChessEngine, AI
import sys

pygame.init()
width  = height = 750
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = height
screen = p.display.set_mode((width, height))
DIMENSION = 8 
SQ_Size = height // DIMENSION
MAX_FPS = 15
IMAGES = {}

#load in Images
def loadIMG():
    #initializing pieces 
    pieces = ['wp','bp', 'wR', 'wB','wN','wQ', 'wK','bR','bB', 'bN', 'bQ', 'bK' ]
 

    #for loop for loading images once at start
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_Size, SQ_Size))
    
    

font = pygame.font.SysFont(None, 60)
#main driver for code and user input handler and update the graphics
def drawMainMenuText(text, font, color, surface, y, x):
    textObj = font.render(text, 1, color)
    textrect = textObj.get_rect()
    textrect.midtop = (x,y)
    surface.blit(textObj, textrect)

click = False

   


def Chess():
    clock = p.time.Clock()
    screen = p.display.set_mode((width + MOVE_LOG_PANEL_WIDTH, height))
    screen.fill(p.Color(40,40,40))
    moveLogFont = p.font.SysFont('Arial', 18, True, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False    #flag var for when a move is made
    animate = False #flag for the animation
    global gameOver
    gameOver = False
    playerOne = True #Player
    playerTwo = False #AI = False

    loadIMG()
    running = True
    sqSelected = () #no square selected, keep track of last click of the user (tuple: row , col)
    playerClicks = [] #keep track of player Clicks(two tuples [(6, 4), (4, 4)])
    while running:
            isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                    pygame.quit()
                #if e.type == KEYDOWN:
                    #if e.key == K_ESCAPE:
                        #pygame.quit()
                #handler    
                if e.type == p.MOUSEBUTTONDOWN:
                    if not gameOver and isHumanTurn:
                        location = p.mouse.get_pos() #x and y location of the mouse
                        row = location[0]// SQ_Size
                        col = location[1]// SQ_Size
            
                        if sqSelected == (col, row) or row >= 8 : #if user clicked the same square twice or clicked MoveLog
                            
                            sqSelected = ()
                            playerClicks = [] #clear player clicks
                        else:
                            sqSelected = (col, row)
                            playerClicks.append(sqSelected) #append for first and second click
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = () #reset user clicks
                                    playerClicks = [] 
                            if not moveMade: 
                                playerClicks = [sqSelected]
                #key handler
                elif e.type == p.KEYDOWN:
                    if e.key == K_ESCAPE:
                        pygame.quit()
                    if e.key == p.K_z and p.K_LCTRL: #Undo when Z + LCTRL is pressed     
                        gs.undoMove()
                        moveMade = True
                        animate = False
                    if e.key == p.K_r: #reset board when r is pressed
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        Chess()

            #AI move logic
            if not gameOver and not isHumanTurn:
                AIMove = AI.findBestMove(gs, validMoves)
                if AIMove is None:
                    AIMove = AI.findRandomMove(validMoves)
                    print("Random")
                gs.makeMove(AIMove)
                moveMade = True
                animate = True


            if moveMade:
                if animate:
                    animateMove(gs.moveLog[-1], screen, gs.board, clock)
                validMoves =  gs.getValidMoves()
                moveMade = False


            drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

            if gs.checkMate:
                gameOver = True
                if gs.whiteToMove:
                    r, c = gs.whiteKingLocation
                    s = p.Surface((SQ_Size, SQ_Size))
                    s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
                    s.fill(p.Color('red'))
                    screen.blit(s, (c*SQ_Size, r*SQ_Size))
                    drawEndGameText(screen, "Black wins by Checkmate")
                else:
                    r, c = gs.blackKingLocation
                    s = p.Surface((SQ_Size, SQ_Size))
                    s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
                    s.fill(p.Color('red'))
                    screen.blit(s, (c*SQ_Size, r*SQ_Size))
                    drawEndGameText(screen, "White wins by Checkmate")
                    #if e.type == p.KEYDOWN:
                        #if e.key == p.K_r: #reset board when r is pressed
                            #gs = ChessEngine.GameState()
                            #validMoves = gs.getValidMoves()
                            #sqSelected = ()
                            #playerClicks = []
                            #moveMade = False
                            #animate = False
            elif gs.staleMate:
                gameOver = True
                drawEndGameText(screen, "Stalemate")

            clock.tick(MAX_FPS)
            p.display.flip()

def main():
    click = False
    global menuRunning 
    menuRunning = True
    menuPic = p.transform.scale(p.image.load("images/" + 'Menu' + ".png"), (width, height))
    dest = (0, 0)
    
    while menuRunning:
        mx, my = pygame.mouse.get_pos()
        screen.blit(menuPic, dest)
        drawMainMenuText('Main Menu', font ,('white'), screen, 10, width/2)

        button_1 = pygame.Rect(width/2-100, 100, 200,50)
        
        button_2 = pygame.Rect(width/2-100, 400, 200,50)
        if button_1.collidepoint((mx, my)):
            if click:
                Chess()
                menuRunning = False
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
        pygame.draw.rect(screen, ('white'), button_1)
        button_1 = drawMainMenuText('Play', font ,('black'), screen, 105, width/2)
        pygame.draw.rect(screen, ('white'), button_2)
        button_2 = drawMainMenuText('Exit', font ,('black'), screen, 405, width/2)

        click = False
        for e in p.event.get():
                if e.type == p.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        click = True
        
        pygame.display.update()

   

def blit_screen(self):
    self.screen.blit(p.display)


#Move Highlighting for the piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    color= (246, 255, 0)
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_Size, SQ_Size))
            s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
            s.fill(p.Color(color))
            screen.blit(s, (c*SQ_Size, r*SQ_Size))
            #highlight moves from that square
            s.fill(p.Color('blue'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_Size, move.endRow*SQ_Size))
                if gs.checkMate:
                    gameOver = True
                    if gs.whiteToMove:
                        r, c = gs.whiteKingLocation
                        s = p.Surface((SQ_Size, SQ_Size))
                        s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
                        s.fill(p.Color('red'))
                        screen.blit(s, (c*SQ_Size, r*SQ_Size))



                    #if gs.squareUnderAttack(r, c):
                        #s = p.Surface((SQ_Size, SQ_Size))
                        #s.fill(p.Color('red'))
                        #screen.blit(s, (c*SQ_Size, r*SQ_Size))
                    
        

                

    
    

#def ChessGame():
    
                    


#Responsible for graphics within current gamestate
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen) #Draw squares on Board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

#MoveLog
def drawMoveLog(screen, gs, font):
    color = p.Color(40,40,40)
    moveLogRect = p.Rect(width, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(color), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = moveLog
    padding = 40
    textY = padding
    textX = 150 
    count = 0
    testY = 20

    MoveLogText = "Move Log"

    SubtitleObject = font.render(MoveLogText, True, p.Color('white'))
    SubtitleLocation = moveLogRect.move(80, 0)
    screen.blit(SubtitleObject, SubtitleLocation)

    test = "White_________|__________Black"
    testObject = font.render(test, True, p.Color('white'))
    testLocation = moveLogRect.move(5, testY)
    screen.blit(testObject, testLocation)

    for i in range(len(moveTexts)):
        move =  str(moveTexts[i]) #modify later
        textObject = font.render(move, True, p.Color('white'))
        if i%2 == 0:
            count = count+1   
            textObject = font.render(str(count)+ "    "+move, True, p.Color('white')) 
            textLocation = moveLogRect.move(padding, textY)
            if i/2 > 0: 
                textObject = font.render(str(count)+ "   "+move, True, p.Color('white')) 
                textY = textY+20
                textLocation = moveLogRect.move(padding, textY)
        elif i%2 <= 1:
            textObject = font.render("  "+move, True, p.Color('white')) 
            textLocation = moveLogRect.move(textX, textY)
        
        screen.blit(textObject, textLocation)
        
        




#Draw Board
def drawBoard(screen):
    global colors
    
    colors =[ p.Color(235, 235, 208), p.Color(119, 148, 85)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))


#Draw Pieces
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))
    




#animate a move 

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC=  move.endCol - move.startCol
    framesPerSquare = 10 #frames to move 1 square
    frameCount= (abs(dR)+ abs(dC))* framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR* frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_Size, move.endRow*SQ_Size, SQ_Size, SQ_Size)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rect
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow +1 if move.pieceCaptured[0] == 'b' else move.endRow -1
                endSquare = p.Rect(move.endCol*SQ_Size, enPassantRow*SQ_Size, SQ_Size, SQ_Size)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))
        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
        font = p.font.SysFont('Helvetica', 32, True, False)
        textObject = font.render(text, 0, p.Color('red'))
        textLocation = p.Rect(0, 0, width, height).move(width/2 -textObject.get_width()/2,height/2 -textObject.get_height()/2 )
        screen.blit(textObject, textLocation)

def draw():
    pass


if __name__ == "__main__":
    main()