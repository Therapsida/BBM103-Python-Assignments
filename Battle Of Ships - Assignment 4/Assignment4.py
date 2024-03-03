import os 
import sys
#Yunus Emre Uluer 2210356102 
curdir = os.getcwd()
outputpath = os.path.join(curdir, "Battleship.out")

with open(outputpath,'w') as f :
    f.write("Battle of Ships Game\n\n")
    print("Battle of Ships Game")
# opens outputpath and writes games name 


def write(string) : 
    with open(outputpath ,'a') as f :
        f.write(f'{string}\n')
        print(string)
#writes and prints outputs 


##################################################################################################################

def findship(char,column, row , size ,list): 
    # This function takes one char's properties(on the board) and finds a pattern regarding the char's ship. 
    
    FoundShip = True
    start = column, row
    for i in range(size-1):    
        try:
            if  char == list[column][row+1]:
                row+= 1  #looks for start index and end index
            else : 
                FoundShip = False 
                break
    
        except IndexError:
            FoundShip = False
            break
    end = column,row
    if FoundShip :
        return True, char,'row',(end[1]-start[1]+1)  #returns True if Ship has found
    else: 
        FoundShip = True
        try:
            for i in range(size-1):
                if  char == list[column+1][row]:
                    column+= 1  
                else : 
                    FoundShip = False
                    break
        except IndexError :
            FoundShip = False
        end = column,row

        if FoundShip :
            return True, char,'column',(end[0]-start[0]+1)
        else :
            
            return False , char,'column',(end[0]-start[0]+1)
   



def sortingboard(list): 
    #returns the list of ships and their locations to the find_locations function finc_locations will sort them one more time.
    list_of_ship= []
    for i in range(10) :
        for j in range(10): 
            if list[i][j] in ['B', 'C', 'D', 'S', 'P'] :
                isShip, char, column_or_row, size  =  findship(list[i][j],i,j ,Shipsdict[list[i][j]],list)
                if isShip :
                    list_of_ship.append([char,(i+1,j+1), column_or_row])
                if column_or_row == 'column':
                    for k in range(size) :
                        list[i+k][j] = ''
                else : 
                    for k in range(size) :
                        list[i][j+k] = ''
    return list_of_ship

def find_locations(list,player):
    #it makes it dictionary and also re-arrange the boards. 
    locations_list = []
    dictionary_list = []
    for  locations in list  :
        char, start , roworcolumn = locations
        shipsort = []
        for  i in   range(Shipsdict[char]):
            
            if roworcolumn == 'column': 
                Playerboard[player][start[0]+i-1][start[1]-1] = char
                shipsort.append((start[0]+i , start[1]))
            else : 
                Playerboard[player][start[0]-1][start[1]+i-1] = char
                shipsort.append((start[0] , start[1]+i))
        dictionary_list.append([char,*shipsort.copy()])
    return dictionary_list


board1 = [10*['-'] for i in range(10)]
board2 = [10*['-'] for i in range(10)]
Playerboard = dict(Player1=board1, Player2= board2)






Remaining_ships_string = {'Player1':{'C':'Carrier\t\t-' ,'B':'Battleship\t- -' ,'D':'Destroyer\t-' ,'S':'Submarine\t-' ,'P':'Patrol Boat\t- - - -'},
'Player2':{'C':'Carrier\t\t-' ,'B':'Battleship\t- -' ,'D':'Destroyer\t-' ,'S':'Submarine\t-' ,'P':'Patrol Boat\t- - - -'}}
Letterdict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10}
ReversedLetterdict = dict(zip(Letterdict.values(),Letterdict.keys()))
ShipsLetters = dict(S="Submarine", C='Carrier', P='Patrol Boat', B="Battleship",D='Destroyer')
##################################################################################################################

moveslist = {'Player1' : [] , 'Player2' : []}

def sortmove(moves,player) :
    #Try except conditions in the moves are handled in this function. Basically splits and looks for the index. 
    condition = True

    while condition:
        try: 
            write(f"Enter your move: {moves[0]}\n")
            if moves[0] in moveslist[player] :
                moves.pop(0)
                raise AssertionError
            else : 
                moveslist[player] += (moves[0])
                # This part is for repeating moves in the program. It raises Assertion Error.

            move = moves.pop(0).split(',')  # because it is a while loop move should be removed from the list.
            
            if move == [""] or len(move) == 1 : 
                output = ("Index Error: No argument given\n")
                raise IndexError

            
            elif move == ["",""]: 
                output = ("Index Error: Missing Arguments(letter and number)")
                raise IndexError
            elif move[0] == "":
                output = ("Index Error: Missing Argument(letter)")
                raise IndexError
            elif move[1] == "":
                output = ("Index Error: Missing Argument(number)")     
                raise IndexError
            else:
                if move[1].isdigit():
                    output = ("ValueError: Second argument must be letter(A-J)")
                    raise ValueError
                elif not(move[0].isdigit()):
                    output = ("ValueError: First argument must be integer(0-9)")
                    raise ValueError
                elif len(move) > 2 : 
                    output = ("ValueError: Three arguments given")
                    raise ValueError
                else:    
                    if int(move[0]) > 10 :
                        raise AssertionError
                    try:
                        
                        return((int(move[0])),Letterdict[move[1]]), player  #returns player and the move (1,C)
                    except KeyError: 
                        raise AssertionError
        except IndexError:
            x = moves[0]
            write(output)
        except ValueError: 
            write(output)
        except AssertionError:
            write("AssertionError: Invalid Operation.")
        else :
            condition = False


def board(isfinal):     
    
    #prints the board. isfinal stands for final information and keeps the boards hidden.
    output=(f'  A B C D E F G H I J\t\t  A B C D E F G H I J\n')
    for i in range(10) :
        if i+1 != 10:
            output += str(i+1) + " "
        else :
            output += str(i+1)
        for l in board1[i] :
            if (l not in ['-', 'X' , 'O']) and isfinal:
                output += '-' + " "
            else :
                output += l + " "
        output = output.rstrip(' ')
        if i+1 != 10 :
            output += '\t\t' + str(i+1) + " "
        else :
            output += '\t\t' + str(i+1)
        for l in board2[i] :
            if (l  not in ['-', 'X' , 'O']) and isfinal:
                output += '-' + " "
            else :
                output += l + " "
        output = output.rstrip(' ')
        output += '\n' 
    output += '\n'    
    return output


def showboard(player,turn) :
    output = ""
    output+=(f"{player}'s Move\n\nRound : {turn}\t\t\t\t\tGrid Size: 10x10\n\n")
    output+=(f"Player1's Hidden Board\t\tPlayer2's Hidden Board\n")
    output+= board(True)
    output += situation()
    write(output)

def situation(): 
    output = f"{Remaining_ships_string['Player1']['C']}\t\t\t\t{Remaining_ships_string['Player2']['C']}\n"
    output += f"{Remaining_ships_string['Player1']['B']}\t\t\t\t{Remaining_ships_string['Player2']['B']}\n"
    output += f"{Remaining_ships_string['Player1']['D']}\t\t\t\t{Remaining_ships_string['Player2']['D']}\n"
    output += f"{Remaining_ships_string['Player1']['S']}\t\t\t\t{Remaining_ships_string['Player2']['S']}\n"
    output += f"{Remaining_ships_string['Player1']['P']}\t\t\t{Remaining_ships_string['Player2']['P']}\n"
    return output


def move(move,player,turn,otherplayer): 
    #Remaining_ships_string has '-'s in it. You replace when ships list has 1 lenght which is their letter(B).  
    global Remaining_ships_string
    if Playerboard[player][move[0]-1][move[1]-1] != '-' :  
        Playerboard[player][move[0]-1][move[1]-1] = 'X'
        for i in range(len(Boards[player])): 
            for j in Boards[player][i]:
                if move == j :
                    Boards[player][i].remove(move)
                    if len(Boards[player][i]) == 1 : 
                        
                        char = Boards[player][i][0]
                        Remaining_ships_string[player][char] = Remaining_ships_string[player][char].replace('-','X', 1)
        return
                        
                           
    else :
        Playerboard[player][move[0]-1][move[1]-1] = 'O'        
        return

def checkwin():
    #Remaining_ships_string contains '-'s. If it does not have '-' in it, it means that game is over.
     
    player1wincondition, player2windcondition = False , False
    for values in Remaining_ships_string['Player1'].values():
        if '-' in values :
            player1wincondition = True 
    for values in Remaining_ships_string['Player2'].values():
        if '-' in values : 
            player2windcondition = True
    if player1wincondition and not(player2windcondition):
        write('Player1 Wins!\n')
        return False
    elif player2windcondition and not(player1wincondition):
        write('Player2 Wins!\n')
        return False
    elif not(player1wincondition and player2windcondition):
        write("It's a draw\n")
        return False
    else :
        return True




Boards = dict()
Shipsdict= dict(B=4,C=5,D=3,S=3,P=2)
try: 
    #IO / Index error handling
    txtfiles_list= [player1board_txt, player2board_txt, player1moves_in, player2moves_in]  = sys.argv[1:5]
    txtfiles_paths = [os.path.join(curdir, file) for file in txtfiles_list ]
    txtdict= dict(zip(txtfiles_paths,txtfiles_list))
    IOErrorstring = ""

    for path in txtfiles_paths : 
        try :
            with open(path, 'r') as f :
                f.read()
        except IOError: 
            IOErrorstring += (txtdict[path]) + " "
    if IOErrorstring != "": 
        write(f"IOError: inputfile(s) {IOErrorstring}is/are not reachable.")
        raise IOError
except IOError : 
    pass
except IndexError :
    write('kaBOOM: run for your life!')
else:     
    try:
        with open(txtfiles_paths[0], 'r') as f: 
            x = [lines.strip('\t').split(';') for lines in f.read().splitlines()]
            Boards['Player1']  = find_locations(sortingboard(x.copy()),'Player1') 

        with open(txtfiles_paths[1], 'r') as f: 
            x = [lines.strip('\t').split(';') for lines in f.read().splitlines()]
            Boards['Player2']  = find_locations(sortingboard(x.copy()),'Player2') 
        
        if len(Boards['Player1']) != 9 or len(Boards['Player2']) != 9 :
            raise IndexError
        with open(txtfiles_paths[2], 'r') as f :
            player1moves = f.read().split(';')
        with open(txtfiles_paths[3], 'r') as f :
            player2moves = f.read().split(';')
        

        condition = True
        i = 0
        while condition : 
            try :    
                i += 1 
                showboard('Player1',i)
                move(*sortmove(player1moves, 'Player2'),i,'Player1')
                showboard('Player2',i)
                move(*sortmove(player2moves,'Player1'),i,'Player2')
                
                condition = checkwin()
            
            except IndexError:
                write("Out of turn, It's a draw\n")
                condition = False
                
        lastinformation = f"Final Information\n\nPlayer1's Board\t\t\t\tPlayer2's Board\n"
        lastinformation+= board(False) + situation()
        write(lastinformation.rstrip('\n\n\n'))
    except IndexError : # Overlapped ships and missing characters in the Players.txt files raises an Index Error. 
        write('kaBOOM: run for your life!')
