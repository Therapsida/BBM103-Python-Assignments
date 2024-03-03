import os
import sys 
#Yunus Emre Uluer 2210356102 

letters = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
letters2 = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
input_txt = sys.argv[1]
current_dir_path = os.getcwd() 
readpath = os.path.join(current_dir_path, input_txt)
writepath = os.path.join(current_dir_path, "output.txt")
categories_dict = dict()
rowsandcolumns_dictionary = dict()
output =''
def CREATECATEGORY(category):
    global output
    rowsandcolumns= category[1].split('x')
    dict_columns_and_rows = dict() #creating the columns and rows as a dictionary
    for i in range(int(rowsandcolumns[1])):
        dict_columns_and_rows[letters[i]] = int(rowsandcolumns[0])*['X']
    
    if not(category[0] in categories_dict) : #creating the dictionary of category 
        categories_dict[category[0]] = dict_columns_and_rows
        output += ("The category '" + category[0] + "' having " + str(int(rowsandcolumns[0])*int(rowsandcolumns[1])) +" seats has been created\n")
    else : 
        output += ("Warning: Cannot create the category for the second time. The stadium has already " + category[0]+".\n")

    rowsandcolumns_dictionary[category[0]] = [int(rowsandcolumns[0]),int(rowsandcolumns[1])] #Storing column and rows for indexing

def SHOWCATEGORY(category):
    global output
    category = category[0]
    string = "Printing category layout of "+category+'\n\n'
    for i in dict(reversed(list(categories_dict[category].items()))) : 
        string += i + " "
        for j in categories_dict[category][i]:
            string += j + " " +" "
        string += '\n'  
    a = 0 
    for i in range(len(categories_dict[category][i])):
        string +=  "%3.d"%(a) #all columns have 2 white spaces so it is fixed.
        a += 1 
    string += '\n'
    output += string



def CANCELTICKET(ticket):
    global output
    category =ticket.pop(0) #after this execution ticket has  elements like A14  B13
    for i in ticket : 
        ticketlist = list(i)              
        ticketrow = ticketlist.pop(0)            # A13 -> ticketrow= A and ticket column=13
        ticketcolumn = int(''.join(ticketlist))
        if rowsandcolumns_dictionary[category][1] < letters2[ticketrow] and rowsandcolumns_dictionary[category][0] < (ticketcolumn+1) : 
            output += "Error: The category '{}' has less column and row than the specified index {}!\n".format(category,i)

        elif rowsandcolumns_dictionary[category][1] < letters2[ticketrow] :
            output += ("Error: The category '{}' has less row than the specified index {}!\n").format(category,i)
    
        elif  rowsandcolumns_dictionary[category][0] < (ticketcolumn+1) :
           output += ("Error: The category '{}' has less column than the specified index {}!\n").format(category,i)

        elif categories_dict[category][ticketrow][ticketcolumn] == 'X' :
            
            output+=("Error: The seat {} at '{}' has already been free! Nothing to cancel\n").format(i,category)
        else : 
            categories_dict[category][ticketrow][ticketcolumn] = 'X'
            
            output += ("Success: The seats {} at '{}' have been canceled and now ready to sell again\n").format(i,category)
            

def SELLTICKET(ticket):
    global output 
    ticketname = ticket.pop(0)          #first 3 parameter of ticket list is name,type,category and seats will remain in ticket list
    tickettype = ticket.pop(0)
    category = ticket.pop(0)
    tickettypedictionary = {"student" : 'S' , "season" : 'T' , "full" : 'F'}

    for i in ticket : 
        if '-' in i : #seats with range(A3-12)
            number = list(i) #we create a list that a is the letter and b is a list that holds 2 numbers(string) (C4-12 : a=C b=[4,12])
            row_letter = number.pop(0)
            number =''.join(number)
            number = number.split('-')
            
            if (rowsandcolumns_dictionary[category][1] < int(number[1]) and rowsandcolumns_dictionary[category][0] < (letters2[row_letter]+1)): #both columns and rows are not on the index
                output +=("Error: The category {} has less column and row than the specified index {}!\n").format(category,i)
            elif (rowsandcolumns_dictionary[category][1] < int(number[1])):   #just column
                output +=("Error: The category {} has less column than the specified index {}!\n").format(category,i)
            elif rowsandcolumns_dictionary[category][0] < (letters2[row_letter]+1) : #just row
                output +=("Error: The category {} has less row than the specified index {}!\n").format(category,i)
                            
            else:   #after the conditions we continue
                condition =True #making a condition for if ticket have been sold it does not sell them.
                for seatnumber in range((int(number[0])),(int(number[1])+1)):
                    
                    if categories_dict[category][row_letter][seatnumber] != 'X':
                        output +=("Error: The seats {} cannot be sold to {} due some of them have already been sold!\n").format(i,ticketname)
                        condition = False
                        break
                if condition :
                    for seatnumber in range(int(number[0]),(int(number[1])+1)):
                            categories_dict[category][row_letter][seatnumber] = tickettypedictionary[tickettype]
                    output +=("Success: {} has bought {} at {}\n").format(ticketname,i,category)

        else: #seats that do not have range
            b = list(i) #A13 splitting
            row_letter = b.pop(0)
            seat_number = int(''.join(b))
            
            if ( rowsandcolumns_dictionary[category][1] < seat_number and rowsandcolumns_dictionary[category][0] < (letters2[row_letter]+1)):  
                    output +=("Error: The category {} has less column and row than the specified index {}!\n").format(category,i)
            elif (rowsandcolumns_dictionary[category][0] < (letters2[row_letter]+1)):
                    output +=("Error: The category {} has less row than the specified index {}!\n").format(category,i)
            elif (rowsandcolumns_dictionary[category][1] < seat_number) : 
                    output +=("Error: The category {} has less column than the specified index {}!\n").format(category,i)
            else:
                if categories_dict[category][row_letter][seat_number] == 'X':
                    categories_dict[category][row_letter][seat_number] = tickettypedictionary[tickettype] #A letter for ticket types
                    output +=("Success: {} has bought {} at {}\n").format(ticketname,i,category)
                else:
                    output +=("The seat {} cannot be sold to {} since it was already sold!\n").format(i, ticketname)



def BALANCE(category) :
    global output  
    category = category[0]
    totalrevenue = 0
    totalfullticket = 0 
    totalstudentticket = 0 
    totalseasonsticket = 0
    for row in categories_dict[category] :  
        for column in categories_dict[category][row] : 
            if column == 'F' :
                totalrevenue += 20
                totalfullticket += 1 
            elif column == 'T' : 
                totalrevenue += 250
                totalseasonsticket += 1
            elif column == 'S' :
                totalrevenue += 10
                totalstudentticket += 1
    string = "Category report of '"+category+"'\n" + len("Category report of '"+category+"'")*"-" +'\n' 
    string +=  ("Sum of students = {}, Sum of full pay = {}, Sum of season ticket = {} , and Revenues = {} Dollars\n").format( str(totalstudentticket),str(totalfullticket),str(totalseasonsticket),str(totalrevenue) )
    output += string



#reading
f = open(readpath , 'r')
data = []
for line in f : 
    line = line.strip('\n')
    line = line.split(" ")
    data += [line]
f.close()
f = open(writepath, 'w')

#main part
for line in data : 
    function_list = [CREATECATEGORY , SHOWCATEGORY , CANCELTICKET , SELLTICKET , BALANCE]
    for function in function_list :
        if line[0] == function.__name__ :
            line.remove(line[0])
            function(line)
print(output)
f.write(output)
f.close()



