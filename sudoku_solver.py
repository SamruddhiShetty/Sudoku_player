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
 

def isEmpty(num):#checks whether position supplied is empty or not
    if (num==0):
        return True
    return False

def isValid(position, num):#checks number chosen is valid or not
    #constraints-row, col, box
    
    #checking row
    for i in range(0, len(grid[0])):
        if grid[position[0]][i]==num:
            return False
        
    #checking column
    for i in range(0, len(grid[0])):
        if grid[i][position[1]]==num:
            return False
        
    #checking the box
    #getting the block number
    x=position[0]//3*3
    y=position[1]//3*3
    
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[x+i][y+j]==num:
                return False
    return True
            
        
solved=0
def sudoku_solver(win):#main algo
    myFont=pygame.font.SysFont('Comic Sans MS', 35)
    #travering the grid recurcively
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if (isEmpty(grid[i][j])):
                for k in range(1, 10):
                    if isValid((i, j), k):
                        grid[i][j]=k
                        #pygame.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                        value=myFont.render(str(k), True, (0,0,0))
                        win.blit(value, (((j+1)*50+15, (i+1)*50)))
                        pygame.display.update()
                        pygame.time.delay(15)
                        
                        
                        sudoku_solver(win)
                        
                        global solved
                        if (solved==1):
                            return
                        
                        #if we arrive at a position where we realise k is invalid we replace it
                        grid[i][j]=0
                        pygame.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                        pygame.display.update()
                        
                return
    solved=1


    

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
   
    sudoku_solver(win)
    while True:
        for event in pygame.event.get():
            
            #quitting the window
            if event.type==pygame.QUIT:
                pygame.quit()
                return
            
            

main()    
