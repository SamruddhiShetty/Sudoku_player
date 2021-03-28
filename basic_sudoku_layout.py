import pygame
#module use to execute get and post request
import requests

#initialising the width and the background of the board displayed
WIDTH=550
background_color=(251,247,245)
#just to distinct the original numbers
original_grid_num_color=(52, 31, 151)
buffer=5

#getting the values from an API suGOku
response=requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid=response.json()['board'] #this is the api part
#crearting another grid with same value just to compare
grid_original=[[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]



def insert(win, position):
    i, j=position[1], position[0]#flipping the values
    myFont=pygame.font.SysFont('Comic Sans MS', 35)
    
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return
            if event.type==pygame.KEYDOWN:
                
                #1 tries to edit the original file
                if grid_original[i-1][j-1]!=0:# -1 to have 0 indexed
                    return 
                
                #2 edit the value entered
                if (event.key==48):#checking with zero-ascii 48
                    #eraing the vlaue when zero entered
                    grid[i-1][j-1]=event.key-48
                    #making the screen blank by suoerimposing blank block
                    pygame.draw.rect(win, background_color, (position[0]*50+buffer, position[1]*50+buffer, 50-2*buffer, 50-2*buffer))
                    pygame.display.update()
                    return
                #3 adding the digit of ur choise
                if (0<event.key-48<10):#checking for valid input
                    pygame.draw.rect(win, background_color, (position[0]*50+buffer, position[1]*50+buffer, 50-2*buffer, 50-2*buffer))
                    value=myFont.render(str(event.key-48), True, (0,0,0))
                    win.blit(value, (position[0]*50+15, position[1]*50))
                    grid[i-1][j-1]=event.key-48#assigning the value
                    pygame.display.update()
                    return
            
                return     
                    

    

def main():
#initialising pygame
    pygame.init()
    #setting the window/display
    win=pygame.display.set_mode((WIDTH, WIDTH))
    #setting the caption
    pygame.display.set_caption("Sudoku")
    #filling the window with the background-color
    win.fill(background_color)
    #font of the numbers
    myFont=pygame.font.SysFont('Comic Sans MS', 35)
    
    #setting the grid
    for i in range(0, 10):
        if (i%3)==0:
            #every 3rd line should be a bold line to separate boxes
            pygame.draw.line(win, (0, 0, 0), (50+50*i, 50), (50+50*i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50+50*i), (500, 50+50*i), 4)
            
        #line_drawing(window, black, starting_cordinate, ending_cor, line_width)
        pygame.draw.line(win, (0, 0, 0), (50+50*i, 50), (50+50*i, 500), 2)#vertical
        pygame.draw.line(win, (0, 0, 0), (50, 50+50*i), (500, 50+50*i), 2)#horizontal
    pygame.display.update()
    
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if (0<grid[i][j]<10):
                value=myFont.render(str(grid[i][j]), True, original_grid_num_color)
                win.blit(value, ((j+1)*50+15, (i+1)*50))
                #here x cordinate has to move horizontally-hence 'j'
                #y should move vertically hence i
                #+15 is the buffer value/ offset
                # +1 cz index starts from 0
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                pos=pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            #quitting the window
            if event.type==pygame.QUIT:
                pygame.quit()
                return
            
            

main()    
