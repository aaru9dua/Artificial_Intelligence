# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# Aarushi Dua - aarudua
# Kalyani Malokar - kmalokar
# Sai Teja Burla - saburla
#
# Based on skeleton code by D. Crandall, Oct 2021


import sys
import time
import copy


def board_to_string(board, N):
    
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


# Function to check if a certain board position is valid or not
def valid_index(pos, n, m):
    
        return 0 <= pos[0] < n  and 0 <= pos[1] < m


# Function used to convert a given board in the form of a list to a matrix form
def board_to_matrix(board, N):
    
    board_matrix=[]
    
    for i in range(0, len(board), N):
        board_matrixR=[]
        
        for j in list(board[i:i+N]):
            board_matrixR.append(j)
            
        board_matrix.append(board_matrixR)  
        
    return board_matrix


# Class definition to make all the moves that each player can make in the game
class raichu_board:
    
    def __init__(self,board):
        
        self.board=board
      
        self.dot=[]
        self.white_Pk=[]
        self.white_p=[]

        self.black_Pk=[]
        self.black_p=[]

        self.white_r=[]
        self.black_r=[]

        for i in range(len(self.board)):
            
            for j in range(len(self.board[0])):
                
                if self.board[i][j]==".":
                    self.dot.append((i,j))
                elif self.board[i][j]=="W":
                    self.white_Pk.append((i,j))
                elif self.board[i][j]=="w":
                    self.white_p.append((i,j))
                elif self.board[i][j]=="B":
                    self.black_Pk.append((i,j))
                elif self.board[i][j]=="B":
                    self.black_p.append((i,j))
                elif self.board[i][j]=="@":
                    self.white_r.append((i,j))
                else:
                    self.black_r.append((i,j))
       
    
    # Function to take an input board and calculate all the possible pichu moves for the player playing white
    # Moves include:
    # Moving one step diagonally left or right in the downward direction
    # Moving two steps diagonally left or right by killing a black pichu in the process
    # Moving to the opponents end of the board and becoming raichu '@'
    def white_pichu_move(self):
        
        visited=[self.board]
        succ_board=[]
       
        for (i,j) in self.white_p:
            
            if i< len(self.board)-2:
                
                board2=copy.deepcopy(self.board)
                board1=copy.deepcopy(self.board)
                
                move1=(i+1,j-1)
                
                if valid_index(move1, len(board2), len(board2[0])):
                        
                        if board2[move1[0]][move1[1]] == "b" and valid_index((move1[0]+1,move1[1]-1),len(board2), len(board2[0])) and board2[move1[0]+1][move1[1]-1] ==".": 
                            
                            if i+2 != len(board1)-1:
                                board2[i][j]="."
                                board2[move1[0]+1][move1[1]-1]="w"
                                board2[move1[0]][move1[1]]="."
                                
                            else:
                                board2[i][j]="."
                                board2[move1[0]+1][move1[1]-1]="@"
                                board2[move1[0]][move1[1]]="."

                        elif board2[i+1][j-1] ==".":
                            board2[i][j]="."
                            board2[move1[0]][move1[1]]="w"
                               
                move2=(i+1,j+1)
                
                if valid_index(move2, len(board1), len(board1[0])):
                    
                        if board1[move2[0]][move2[1]] == "b" and valid_index((move2[0]+1,move2[1]+1),len(board1), len(board1[0])) and board1[move2[0]+1][move2[1]+1] =="." :
                            
                            if i+2 != len(board1)-1:
                                board1[i][j]="."
                                board1[move2[0]+1][move2[1]+1]="w"
                                board1[move2[0]][move2[1]]="."
                                
                            else:
                                board1[i][j]="."
                                board1[move2[0]+1][move2[1]+1]="@"
                                board1[move2[0]][move2[1]]="."

                        elif board1[i+1][j+1] ==".":
                            
                            board1[i][j]="."
                            board1[move2[0]][move2[1]]="w"
                   
                if board2 not in visited:
                    succ_board.append(board2)
                    
                if board1 not in visited:
                    succ_board.append(board1)
            
            elif i==len(self.board)-2:
                
                board7=copy.deepcopy(self.board)
                board8=copy.deepcopy(self.board)
                
                move1=(i+1,j-1)
                 
                if valid_index(move1, len(board7), len(board7[0])) and board7[move1[0]][move1[1]]=='.':
                    
                    board7[i][j]='.'
                    board7[move1[0]][move1[1]]='@'
                    succ_board.append(board7)
                    
                move2=(i+1,j+1)
                
                if valid_index(move2, len(board8), len(board8[0])) and board8[move2[0]][move2[1]]=='.':
                    
                    board8[i][j]='.'
                    board8[move2[0]][move2[1]]='@'
                    succ_board.append(board8)

        return succ_board
    
    
    # Function to take an input board and calculate all the possible pichu moves for the player playing black
    # Moves include:
    # Moving one step diagonally left or right in the upward direction
    # Moving two steps diagonally left or right by killing a white pichu in the process
    # Moving to the opponents end of the board and becoming raichu '$'
    def black_pichu_move(self):

        visited=[self.board]
        succ_board=[]
   
        for (i,j) in self.black_p:
            
            if i >1:
                
                board2=copy.deepcopy(self.board)
                board1=copy.deepcopy(self.board)
                
                move1=(i-1,j-1)
                
                if valid_index(move1, len(board2), len(board2[0])):
                    
                        if board2[move1[0]][move1[1]] == "w" and valid_index((move1[0]-1,move1[1]-1),len(board2), len(board2[0])) and board2[move1[0]-1][move1[1]-1] =="." :
                            
                            if i-2 != 0:
                                board2[i][j]="."
                                board2[move1[0]-1][move1[1]-1]="b"
                                board2[move1[0]][move1[1]]="."
                                
                            else:
                                board2[i][j]="."
                                board2[move1[0]-1][move1[1]-1]="$"
                                board2[move1[0]][move1[1]]="."
                            
                        elif board2[i-1][j-1] ==".":
                        
                            board2[i][j]="."
                            board2[move1[0]][move1[1]]="b"
                                
                move2=(i-1,j+1)
                
                if valid_index(move2, len(board1), len(board1[0])):
                        
                        if board1[move2[0]][move2[1]] == "w" and valid_index((move2[0]-1,move2[1]+1),len(board1), len(board1[0])) and board1[move2[0]-1][move2[1]+1] =="." : 
                            
                            if i-2 != 0:
                                board1[i][j]="."
                                board1[move2[0]-1][move2[1]+1]="b"
                                board1[move2[0]][move2[1]]="."
                                
                            else:
                                board1[i][j]="."
                                board1[move2[0]-1][move2[1]+1]="$"
                                board1[move2[0]][move2[1]]="."

                        elif board1[move2[0]][move2[1]] ==".":
                            
                            board1[i][j]="."
                            board1[move2[0]][move2[1]]="b"
                
                if board2 not in visited:
                    succ_board.append(board2)
                    
                if board1 not in visited:
                    succ_board.append(board1)

            elif i==1:
                
                board7=copy.deepcopy(self.board)
                board8=copy.deepcopy(self.board)
                
                move1=(i-1,j-1)
                  
                if valid_index(move1, len(board7), len(board7[0])) and board7[move1[0]][move1[1]]=='.':
                    
                    board7[i][j]='.'
                    board7[move1[0]][move1[1]]='$'
                    succ_board.append(board7)
                    
                move2=(i-1,j+1)
                
                if valid_index(move2, len(board8), len(board8[0])) and board8[move2[0]][move2[1]]=='.':
                    
                    board8[i][j]='.'
                    board8[move2[0]][move2[1]]='$'
                    succ_board.append(board8)

        return succ_board
    
    
    # Helper function to take an input board and calculate all the possible forward pikachu moves for the player playing white
    # Moves include:
    # If a black pikachu is enountered while moving forward and the position after it is dot we move the white pikachu to that dot and remove black pikachu from the board
    # If a black pichu is enountered while moving forward and the position after it is dot we move the white pikachu to that dot and remove black pichu from the board
    def pickachu_move_f(self,i,j,move_f,board1):

        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] == "B" and valid_index((move_f[0]+1,move_f[1]),len(board1), len(board1[0])) and board1[move_f[0]+1][move_f[1]] =="." :
                
                if move_f[0]+1 != len(board1)-1:
                    board1[i][j]="."
                    board1[move_f[0]+1][move_f[1]]="W"
                    board1[move_f[0]][move_f[1]]="."
                    
                else:
                    board1[i][j]="."
                    board1[move_f[0]+1][move_f[1]]="@"
                    board1[move_f[0]][move_f[1]]="."
                
            elif board1[move_f[0]][move_f[1]] == "b" and valid_index((move_f[0]+1,move_f[1]),len(board1), len(board1[0])) and board1[move_f[0]+1][move_f[1]] =="." :
                
                if move_f[0]+1 != len(board1)-1:
                    board1[i][j]="."
                    board1[move_f[0]+1][move_f[1]]="W"
                    board1[move_f[0]][move_f[1]]="."
                   
                else:
                    board1[i][j]="."
                    board1[move_f[0]+1][move_f[1]]="@"
                    board1[move_f[0]][move_f[1]]="."  

            elif board1[move_f[0]][move_f[1]] ==".":
                
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]="W"
            
        return board1
    
    
    # Helper function to take an input board and calculate all the possible right pikachu moves for the player playing white
    # Moves include:
    # If a black pikachu is enountered while moving right and the position after it is dot we move the white pikachu to that dot and remove black pikachu from the board
    # If a black pichu is enountered while moving right and the position after it is dot we move the white pikachu to that dot and remove black pichu from the board
    def pickachu_move_r(self,i,j,move_r,board1):
    
        if valid_index(move_r, len(board1), len(board1[0])):
            
            if board1[move_r[0]][move_r[1]] == "B" and valid_index((move_r[0],move_r[1]+1),len(board1), len(board1[0])) and board1[move_r[0]][move_r[1]+1] =="." :
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]+1]="W"
                board1[move_r[0]][move_r[1]]="."
               

            elif board1[move_r[0]][move_r[1]] == "b" and valid_index((move_r[0],move_r[1]+1),len(board1), len(board1[0])) and board1[move_r[0]][move_r[1]+1] =="." :
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]+1]="W"
                board1[move_r[0]][move_r[1]]="."
          
            elif board1[move_r[0]][move_r[1]] == ".":
                                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]]="W"

        return board1
    
    
    # Helper function to take an input board and calculate all the possible left pikachu moves for the player playing white
    # Moves include:
    # If a black pikachu is enountered while moving left and the position after it is dot we move the white pikachu to that dot and remove black pikachu from the board
    # If a black pichu is enountered while moving left and the position after it is dot we move the white pikachu to that dot and remove black pichu from the board
    def pickachu_move_l(self,i,j,move_r,board1):
    
        if valid_index(move_r, len(board1), len(board1[0])):
            
            if board1[move_r[0]][move_r[1]] == "B" and valid_index((move_r[0],move_r[1]-1),len(board1), len(board1[0])) and board1[move_r[0]][move_r[1]-1] =="." :
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]-1]="W"
                board1[move_r[0]][move_r[1]]="."
               
            elif board1[move_r[0]][move_r[1]] == "b" and valid_index((move_r[0],move_r[1]-1),len(board1), len(board1[0])) and board1[move_r[0]][move_r[1]-1] =="." :
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]-1]="W"
                board1[move_r[0]][move_r[1]]="."
             
            elif board1[move_r[0]][move_r[1]] == ".":
                                                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]]="W"
              
        return board1
    
    
    # Function to take an input board and calculate all the possible pikachu moves for the player playing white
    # Moves include:
    # Moving one step forward, left or right in the downward direction
    # Moving two steps forward, left or right in the downward direction
    # Moving two steps forward, left or right by killing a black pichu or pikachu in the process
    # Moving three steps forward, left or right by killing a black pichu or pikachu in the process
    # Moving to the opponents end of the board and becoming raichu '@'
    def white_pikachu_move(self):

        visited=[self.board]
        succ_board=[]
        
        for (i,j) in self.white_Pk:
                
                board1=copy.deepcopy(self.board)
                board2=copy.deepcopy(self.board)
                board3=copy.deepcopy(self.board)
                board4=copy.deepcopy(self.board)
                board5=copy.deepcopy(self.board)
                board6=copy.deepcopy(self.board)
                
                move_f1=(i+1,j)
                
                if i< len(self.board)-2:
                    
                    board1=self.pickachu_move_f(i,j,move_f1,board1)
                    if board1 not in visited:
                        succ_board.append(board1)

                elif i==len(self.board)-2:
                      
                    if valid_index((move_f1[0],move_f1[1]), len(board1), len(board1[0])) and board1[move_f1[0]][move_f1[1]]=='.':
                        
                        board1[i][j]='.'
                        board1[move_f1[0]][move_f1[1]]='@'
                        succ_board.append(board1)
                    
                move_f2=(i+2,j)

                if i<len(self.board)-3 and board2[move_f2[0]-1][move_f2[1]]=='.':
                
                    board2=self.pickachu_move_f(i,j,move_f2,board2)
                    if board2 not in visited:
                        succ_board.append(board2)
                        
                elif i==len(self.board)- 3 and board2[move_f2[0]-1][move_f2[1]]=='.':
                      
                    if valid_index((move_f2[0],move_f2[1]), len(board2), len(board2[0])) and board2[move_f2[0]][move_f2[1]]=='.':
                        
                        board2[i][j]='.'
                        board2[move_f2[0]][move_f2[1]]='@'
                        succ_board.append(board2)

                move_r1= (i,j+1)
             
                board3=self.pickachu_move_r(i,j,move_r1,board3)
                if board3 not in visited:
                    succ_board.append(board3)

                move_r2= (i,j+2)
                
                if  valid_index((move_r2[0],move_r2[1]-1), len(board2), len(board2[0])) and board4[move_r2[0]][move_r2[1]-1]=='.':
                    
                    board4=self.pickachu_move_r(i,j,move_r2,board4)
                    if board4 not in visited:
                        succ_board.append(board4)

                move_l1= (i,j-1)
                
                board5=self.pickachu_move_l(i,j,move_l1,board5)
                if board5 not in visited:
                    succ_board.append(board5)

                move_l2= (i,j-2)
                
                if valid_index((move_l2[0],move_l2[1]+1), len(board2), len(board2[0])) and board6[move_l2[0]][move_l2[1]+1]=='.':
                    
                    board6=self.pickachu_move_l(i,j,move_l2,board6)
                    if board6 not in visited:
                        succ_board.append(board6)
            
        return succ_board
    
    
    # Helper function to take an input board and calculate all the possible forward pikachu moves for the player playing black
    # Moves include:
    # If a white pikachu is enountered while moving forward and the position after it is dot we move the black pikachu to that dot and remove white pikachu from the board
    # If a white pichu is enountered while moving forward and the position after it is dot we move the black pikachu to that dot and remove white pichu from the board
    def black_pickachu_move_f(self,i,j,move_f,board1):
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] == "W" and valid_index((move_f[0]-1,move_f[1]),len(board1), len(board1[0])) and board1[move_f[0]-1][move_f[1]] =="." :
   
                if move_f[0]-1 !=0:
                    board1[i][j]="."
                    board1[move_f[0]-1][move_f[1]]="B"
                    board1[move_f[0]][move_f[1]]="."
              
                else:
                    board1[i][j]="."
                    board1[move_f[0]-1][move_f[1]]="$"
                    board1[move_f[0]][move_f[1]]="."

            elif board1[move_f[0]][move_f[1]] == "w" and valid_index((move_f[0]-1,move_f[1]),len(board1), len(board1[0])) and board1[move_f[0]-1][move_f[1]] =="." :
                
                if move_f[0]-1 !=0:
                    board1[i][j]="."
                    board1[move_f[0]-1][move_f[1]]="B"
                    board1[move_f[0]][move_f[1]]="."
                
                else:
                    board1[i][j]="."
                    board1[move_f[0]-1][move_f[1]]="$"
                    board1[move_f[0]][move_f[1]]="."

            elif board1[move_f[0]][move_f[1]] ==".":
                
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]="B"
              
        return board1
    
    
    # Helper function to take an input board and calculate all the possible right pikachu moves for the player playing black
    # Moves include:
    # If a white pikachu is enountered while moving right and the position after it is dot we move the black pikachu to that dot and remove white pikachu from the board
    # If a white pichu is enountered while moving right and the position after it is dot we move the black pikachu to that dot and remove white pichu from the board
    def black_pickachu_move_r(self,i,j,move_r,board1):
    
        if valid_index(move_r, len(board1), len(board1[0])):
            
            if board1[move_r[0]][move_r[1]] == "W" and valid_index((move_r[0],move_r[1]+1),len(board1), len(board1[0])) and board1[move_r[0]][move_r[1]+1] =="." :
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]+1]="B"
                board1[move_r[0]][move_r[1]]="."
                

            elif board1[move_r[0]][move_r[1]] == "w" and valid_index((move_r[0],move_r[1]+1),len(board1), len(board1[0])) and board1[move_r[0]][move_r[1]+1] ==".":
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]+1]="B"
                board1[move_r[0]][move_r[1]]="."
               
            elif board1[move_r[0]][move_r[1]] == ".":                               
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]]="B"
            
        return board1
    
    
    # Helper function to take an input board and calculate all the possible left pikachu moves for the player playing black
    # Moves include:
    # If a white pikachu is enountered while moving left and the position after it is dot we move the black pikachu to that dot and remove white pikachu from the board
    # If a white pichu is enountered while moving left and the position after it is dot we move the black pikachu to that dot and remove white pichu from the board
    def black_pickachu_move_l(self,i,j,move_r,board1):
    
        if valid_index(move_r, len(board1), len(board1[0])):
            
            if board1[move_r[0]][move_r[1]] == "W" and board1[move_r[0]][move_r[1]-1] =="." and valid_index((move_r[0],move_r[1]-1),len(board1), len(board1[0])):
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]-1]="B"
                board1[move_r[0]][move_r[1]]="."
              
            elif board1[move_r[0]][move_r[1]] == "w" and board1[move_r[0]][move_r[1]-1] =="." and valid_index((move_r[0],move_r[1]-1),len(board1), len(board1[0])):
                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]-1]="B"
                board1[move_r[0]][move_r[1]]="."
               
            elif board1[move_r[0]][move_r[1]] == ".":
                                                
                board1[i][j]="."
                board1[move_r[0]][move_r[1]]="B"
             
        return board1
    
    
    # Function to take an input board and calculate all the possible pikachu moves for the player playing black
    # Moves include:
    # Moving one step forward, left or right in the upward direction
    # Moving two steps forward, left or right in the upward direction
    # Moving two steps forward, left or right by killing a white pichu or pikachu in the process
    # Moving three steps forward, left or right by killing a white pichu or pikachu in the process
    # Moving to the opponents end of the board and becoming raichu '$'
    def black_pikachu_move(self):
        
        visited=[self.board]
        succ_board=[]
        
        for (i,j) in self.black_Pk:
            
            board1=copy.deepcopy(self.board)
            board2=copy.deepcopy(self.board)
            board3=copy.deepcopy(self.board)
            board4=copy.deepcopy(self.board)
            board5=copy.deepcopy(self.board)
            board6=copy.deepcopy(self.board)

            move_b1=(i-1,j) 
            
            if i>1:
                
                board1=self.black_pickachu_move_f(i,j,move_b1,board1)
                if board1 not in visited:
                    succ_board.append(board1)
                    
            elif i==1:
                 
                if valid_index((move_b1[0],move_b1[1]), len(board1), len(board1[0])) and board1[move_b1[0]][move_b1[1]]=='.':
                    
                    board1[i][j]='.'
                    board1[move_b1[0]][move_b1[1]]='$'
                    succ_board.append(board1)

            move_b2=(i-2,j)
            
            if i>2 and board2[move_b2[0]+1][move_b2[1]]=='.':
                
                board2=self.black_pickachu_move_f(i,j,move_b2,board2)
                if board2 not in visited:
                    succ_board.append(board2)

            elif i==2 and board2[move_b2[0]+1][move_b2[1]]=='.':
                    
                    if valid_index((move_b2[0],move_b2[1]), len(board2), len(board2[0])) and board2[move_b2[0]][move_b2[1]]=='.':
                        
                        board2[i][j]='.'
                        board2[move_b2[0]][move_b2[1]]='$'
                        succ_board.append(board2)
            
            move_r1= (i,j+1)
            
            board3=self.black_pickachu_move_r(i,j,move_r1,board3)
            if board3 not in visited:
                succ_board.append(board3)
            
            move_r2= (i,j+2)
            
            if valid_index((move_r2[0],move_r2[1]-1),len(board4),len(board4[0])) and board4[move_r2[0]][move_r2[1]-1]=='.':
                
                board4=self.black_pickachu_move_r(i,j,move_r2,board4)
                if board4 not in visited:
                    succ_board.append(board4)
            
            move_l1= (i,j-1)
            
            board5=self.black_pickachu_move_l(i,j,move_l1,board5)
            if board5 not in visited:
                succ_board.append(board5)
            
            move_l2= (i,j-2)
            
            if valid_index((move_l2[0],move_l2[1]+1),len(board4),len(board4[0])) and board6[move_l2[0]][move_l2[1]-1]=='.':
                
                board6=self.black_pickachu_move_l(i,j,move_l2,board6)
                if board6 not in visited:
                    succ_board.append(board6)
            
        return succ_board
    
    
    # Helper function to take an input board and calculate all the possible forward raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving forward and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving forward and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving forward and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_f(self,i,j,move_f,board1,player,opponent):
    
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0]-1,move_f[1]),len(board1), len(board1[0])) and board1[move_f[0]-1][move_f[1]] ==".":
                
                board1[i][j]="."
                board1[move_f[0]-1][move_f[1]]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True

            elif board1[move_f[0]][move_f[1]] ==".":
                    
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
            else:
                
                flag=True

        return board1,flag
    
    
    # Helper function to take an input board and calculate all the possible backward raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving backward and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving backward and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving backward and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_b(self,i,j,move_f,board1,player,opponent):
    
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0]+1,move_f[1]),len(board1), len(board1[0])) and board1[move_f[0]+1][move_f[1]] ==".":
            
                board1[i][j]="."
                board1[move_f[0]+1][move_f[1]]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True
            
            elif board1[move_f[0]][move_f[1]] ==".":
        
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
            else:
                
                flag = True
            
        return board1,flag

    
    # Helper function to take an input board and calculate all the possible left raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving left and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving left and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving left and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_l(self,i,j,move_f,board1,player,opponent):
        
            flag=False
            
            if valid_index(move_f, len(board1), len(board1[0])):
                
                if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0],move_f[1]-1),len(board1), len(board1[0])) and board1[move_f[0]][move_f[1]-1] ==".":
                    
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]-1]=player
                    board1[move_f[0]][move_f[1]]="."
                    flag=True
                
                elif board1[move_f[0]][move_f[1]] ==".":
                    
                        board1[i][j]="."
                        board1[move_f[0]][move_f[1]]=player
                        flag=False
                        
                else:
                    
                    flag = True
                
            return board1,flag
        
    
    # Helper function to take an input board and calculate all the possible right raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving right and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving right and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving right and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_r(self,i,j,move_f,board1,player,opponent):
        
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0],move_f[1]+1),len(board1), len(board1[0])) and board1[move_f[0]][move_f[1]+1] ==".":

                board1[i][j]="."
                board1[move_f[0]][move_f[1]+1]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True
            
            elif board1[move_f[0]][move_f[1]] ==".":
                
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
                    
            else:
                
                flag = True
            
        return board1,flag
    
    
    # Helper function to take an input board and calculate all the possible diagonal left upward raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving diagonal left upward and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving diagonal left upward and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving diagonal left upward and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_dig_l_up(self,i,j,move_f,board1,player,opponent):
    
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0]-1,move_f[1]-1),len(board1), len(board1[0])) and board1[move_f[0]-1][move_f[1]-1] ==".":
                
                board1[i][j]="."
                board1[move_f[0]-1][move_f[1]-1]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True
            
            elif board1[move_f[0]][move_f[1]] ==".":
                    
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
                    
            else:
                
                flag=True
            
        return board1,flag
    
    
    # Helper function to take an input board and calculate all the possible diagonal left downward raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving diagonal left downward and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving diagonal left backward and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving diagonal left backward and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_dig_down_l(self,i,j,move_f,board1,player,opponent):
        
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0]+1,move_f[1]-1),len(board1), len(board1[0])) and board1[move_f[0]+1][move_f[1]-1] ==".":
                
                board1[i][j]="."
                board1[move_f[0]+1][move_f[1]-1]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True
            
            elif board1[move_f[0]][move_f[1]] ==".":
                    
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
                    
            else:
                
                flag=True
            
        return board1,flag
    
    
    # Helper function to take an input board and calculate all the possible diagonal right upward raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving diagonal right upward and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving diagonal right upward and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving diagonal right upward and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_dig_up_r(self,i,j,move_f,board1,player,opponent):
    
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0]-1,move_f[1]+1),len(board1), len(board1[0])) and board1[move_f[0]-1][move_f[1]+1] ==".":
                
                board1[i][j]="."
                board1[move_f[0]-1][move_f[1]+1]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True
            
            elif board1[move_f[0]][move_f[1]] ==".":
                    
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
                    
            else:
                
                flag=True
            
        return board1,flag
    
    
    # Helper function to take an input board and calculate all the possible diagonal right downward raichu moves for the player
    # Moves include:
    # If an opponent raichu is enountered while moving diagonal right downward and the position after it is dot we move the raichu to that dot and opponent raichu from the board
    # If an opponent pikachu is enountered while moving diagonal right backward and the position after it is dot we move the raichu to that dot and opponent pikachu from the board
    # If an opponent pichu is enountered while moving diagonal right backward and the position after it is dot we move the raichu to that dot and opponent pichu from the board
    def raichu_move_dig_down_r(self,i,j,move_f,board1,player,opponent):
        
        flag=False
        
        if valid_index(move_f, len(board1), len(board1[0])):
            
            if board1[move_f[0]][move_f[1]] in opponent and valid_index((move_f[0]+1,move_f[1]+1),len(board1), len(board1[0])) and board1[move_f[0]+1][move_f[1]+1] ==".":
                
                board1[i][j]="."
                board1[move_f[0]+1][move_f[1]+1]=player
                board1[move_f[0]][move_f[1]]="."
                flag=True
            
            elif board1[move_f[0]][move_f[1]] ==".":
                    
                    board1[i][j]="."
                    board1[move_f[0]][move_f[1]]=player
                    flag=False
                    
            else:
                
                flag=True
            
        return board1,flag
    
    
    # Function to take an input board and a player as input
    # And calculate all the possible raichu moves for that particular player 
    def raichu_move(self,max_player):
        
        if max_player=='w':
            player='@'
            opponent=['B','b','$']
            
        else:
            player='$'
            opponent=['W','w','@']

        visited=[self.board]
        succ_board=[]
        
        for (r,c) in self.white_r:
            
            # Forward
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r-i,c)
                next_board,flag=self.raichu_move_f(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break
                    
            # Backward
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r+i,c)
                next_board,flag=self.raichu_move_b(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break
            
            # Left
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r,c-i)
                next_board,flag=self.raichu_move_l(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break
            
            # Right
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r,c+i)
                next_board,flag=self.raichu_move_r(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break
                    
            # Diagonal Left Downward
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r+i,c-i)
                next_board,flag=self.raichu_move_dig_down_l(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break
                    
            # Diagonal Left Upward
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r-i,c-i)
                next_board,flag=self.raichu_move_dig_l_up(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break

            # Diagonal Right Downward
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r+i,c+i)
                next_board,flag=self.raichu_move_dig_down_r(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break

            # Diagonal Right Upward
            for i in range(1,len(self.board)):
                board1=copy.deepcopy(self.board)
                move=(r-i,c+i)
                next_board,flag=self.raichu_move_dig_up_r(r,c,move,board1,player,opponent)
                if next_board not in visited:
                    succ_board.append(next_board)
                if flag:
                    break
                        
        return succ_board
    
    
    # Function to get a valid board based on the player
    def get_valid_board(self,player):
        
        curr_board=raichu_board(self.board)
        next_board=[]

        if player=='w':
            
            next_board.extend(curr_board.raichu_move(player))
            next_board.extend(curr_board.white_pikachu_move())
            next_board.extend(curr_board.white_pichu_move())
            
        else:
            
            next_board.extend(curr_board.raichu_move(player))
            next_board.extend(curr_board.black_pikachu_move())
            next_board.extend(curr_board.black_pichu_move())
        
        return next_board
    
    
    # Evaluation function 
    # We are counting both white and black pieces and giving each type of their pieces a certain weight
    # If the max_player is white then maximise the score for the white pieces and that will be positive
    # Else the score will be calculated for black so that will be negative
    def evaluation(self,max_player):	
        e_board=raichu_board(self.board)
        
        score= 10*(len(e_board.white_r)-len(e_board.black_r))+5*(len(e_board.white_Pk)-len(e_board.black_Pk))+(len(e_board.white_p)-len(e_board.black_p))
        
        if (max_player == 'w'):
            return score
        else:
            return -score
        '''
        e_board=raichu_board(self.board)
        
        w_left=len(e_board.white_p)+len(e_board.white_Pk)+len(e_board.white_r)
        b_left=len(e_board.black_p)+len(e_board.black_Pk)+len(e_board.black_r)
        
        board=self.board
        score = 0
        
        weight_dict={'w':10,'W':20,"@":30,'b':-10,'B':-20,'$':-30}
        
        for i in range(len(board)):
            
            for j in range(len(board[0])):
        
                if board[i][j]==".":
                    continue
                    
                elif board[i][j]=="W":
                    score+=weight_dict['W']
                    
                elif board[i][j]=="w":
                    score+=weight_dict['w']
                    
                elif board[i][j]=="B":
                    score+=weight_dict['B']
                
                elif board[i][j]=="b":
                    score+=weight_dict['b']
                
                elif board[i][j]=="@":
                    score+=weight_dict['@']
                
                elif board[i][j]=="$":
                    score+=weight_dict['$']
                    
        score+= 100*(w_left-b_left)
        
        if (max_player == 'w'):
            return score
        
        else:
            return -score
        '''
    
    # Function to check if the game is over or not
    def game_over(self):

        Wleft=self.white_Pk
        wleft=self.white_p

        Bleft=self.black_Pk
        bleft=self.black_p

        WRleft=self.white_r
        BRleft=self.black_r

        if (len(Wleft) + len(wleft)+ len(WRleft)== 0):
            return True, 'Black'
        
        elif (len(Bleft) + len(bleft)+ len(BRleft)== 0):
            return True, 'White'

        return False,""
    
    
    # Function to implement minimax with alpha-beta pruning
    # If max_player is true, it will do a recursive loop and it will change the player 
    # Inorder to get the minimum from the successor board 
    # And the game will end with either depth is 0 or the game is over  
    def minimax(self,depth,alpha,beta,player,max_player):
        
        curr_board=raichu_board(self.board)
        
        if depth ==0 and curr_board.game_over():
            return curr_board.evaluation(player), curr_board.board
        
        if player:
            
            if player=='w':
                change_player='b'
                
            else:
                change_player='w'
            
            max_e=-1e10
            best_move=None
            
            for move in curr_board.get_valid_board(max_player):
                
                next_board=raichu_board(move)
                
                eval1=next_board.minimax(depth-1,alpha,beta,change_player,False)[0]
                
                max_e=max(max_e,eval1)
                alpha = max(alpha, eval1)
                
                if max_e== eval1:
                    best_move=move
                    
                if beta <= alpha:
                    break
                    
            return max_e, best_move
                   
                
        else:
            
            min_e=1e10
            best_move=None
            
            for move in curr_board.get_valid_board(max_player):
                
                next_board=raichu_board(move)
                
                eval1=next_board.minimax(depth-1,alpha,beta,change_player,True)[0]
                
                min_e=min(min_e,eval1)
                beta = min(beta, eval1)
                
                if min_e== eval1:
                    best_move=move 
                    
                if beta <= alpha:
                    break
                
            return min_e, best_move
        

# Function to find and return the best move/board from all the potential moves/boards
def find_best_move(board, N, player, timelimit):
    
    board_matrix=board_to_matrix(board,N)
    board_pos=raichu_board(board_matrix)
    
    alpha=-1e10
    beta=1e10
    max_v=-1e10
    
    next_board=board_pos.get_valid_board(player)


    for i in next_board:
        b=raichu_board(i)
        
        e,best_board=b.minimax(3,alpha,beta,player,True)
        
        if e >= max_v:
            
            max_v = e
            b = [''.join([str(c) for c in lst]) for lst in i]
            b = ''.join(b)
            
            yield b
        

if __name__ == "__main__":
    if len(sys.argv) != 5:
       raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    

    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
  
    for new_board in find_best_move(board, N, player, timelimit):
       
            print(new_board)
    
