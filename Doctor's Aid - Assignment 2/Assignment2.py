import os 
current_dir_path = os.getcwd()
reading_file_name = "doctors_aid_inputs.txt"
reading_file_path = os.path.join(current_dir_path, reading_file_name)



writing_file_name = "doctors_aid_outputs.txt"
writing_file_path = os.path.join(current_dir_path, writing_file_name)

#it needs to overwrite the output file if exists
with open (writing_file_path , 'w') as f :
    f.write('')


def read(): 
    with open(reading_file_path, "r") as f:
        global data
        data = f.readlines()


def sort_data(sortdata) :
    #getting rid of the commands
    sortdata = str.split(sortdata)
    sortdata.remove(sortdata[0])
    #checking if command is create or not
    if len(sortdata) > 5 :
        #getting rid of the ','s
        sortdata =' '.join(sortdata)
        sortdata = sortdata.split(',')
        #gettin rid of the whitespaces
        for i in range(2,5):
            a = list(sortdata[i])
            a.remove(" ")
            sortdata[i]=''.join(a) 

        #arranging accuracy
        float_accuracy = float(sortdata[1])
        string_accuracy =  str("{0:.2f}".format(float_accuracy*100)) + '%'
        sortdata[1] = string_accuracy  
        #arranging risk
        float_risk = float(sortdata[5])
        string_risk = str(int(float_risk*100)) + '%'
        sortdata[5] = string_risk
        
   
    return sortdata

def write(x,y,z) :
    with open (writing_file_path , 'a') as f :
        x = x + y + z
        f.write(x)
        
def writing_probability(patient) :
    #list to string
    patient = patient[0]
    for i in range(len(list_of_data)) :
        #probability calculations
        if patient in list_of_data[i] :
            a = list(list_of_data[i][1])
            a.remove('%')
            b = ''.join(a)
            accuracy = float(b)

            splitted_incidence = list_of_data[i][3].split('/')
            nominator = float(splitted_incidence[0])
            denominator = float(splitted_incidence[1])
    
            
            TP = (nominator*accuracy)/100 
            FP = (denominator-nominator)*(100-accuracy)/100 
            probability  = (TP/(TP+FP))*100
            probability = str("{0:.4g}".format(probability)) + "%"
            x = "Patient " + list_of_data[i][0] 
            y = " has a probability of " + probability 
            z = " of having " + list_of_data[i][2].lower() +".\n"
            write(x,y,z)
            return
    write("Probability for ", patient , " cannot be calculated due to absence.\n") 

def calculating_probability(patient):
    #for returning recommendatiton
    patient = patient[0]
    for i in range(len(list_of_data)) :
        
        if patient in list_of_data[i] :
            a = list(list_of_data[i][1])
            a.remove('%')
            b = ''.join(a)
            accuracy = float(b)

            splitted_incidence = list_of_data[i][3].split('/')
            nominator = float(splitted_incidence[0])
            denominator = float(splitted_incidence[1])
    

            TP = (nominator*accuracy)/100 
            FP = (denominator-nominator)*(100-accuracy)/100 
            probability  = (TP/(TP+FP))*100

            return probability   

def create(commands) :
    #appending list and checking if there is dublication or not
    global list_of_data
    for i in list_of_data :
        if commands[0] == i[0] :
            write("Patient ", i[0] , " cannot be recorded due to duplication.\n")
            return
    write("Patient ", commands[0] , " is recorded.\n")
    list_of_data.append(commands)
    
def listing() :
    
    text = "Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment\nName\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk\n-------------------------------------------------------------------------\n"
    for i in list_of_data:
        line= ""
        #all of the if statements are written based on the longest word
        if(len(i[0]) < 3) :
            line +=  i[0] + "\t\t"
        else :
            line +=  i[0] + "\t"
        line += i[1] + "\t\t"     
        if (len(i[2]) < 12) :
            line += i[2] +"\t\t"
        else:
           line+= i[2]+ "\t"
        line+=i[3]+"\t"
        if (len(i[4]) < 8) :
           line+=i[4]+"\t\t\t" 
        elif (len(i[4]) < 12) :
           line+=i[4]+"\t\t"
        elif (len(i[4]) < 16) :
           line+=i[4]+"\t" 
 
        else:
            line+=i[4]
        line+= i[5] + "\n"    
        text += line
    write(text,"","")

def removedata(commands) :
    commands= ''.join(commands)
    global list_of_data
    for i in range(len(list_of_data)-1) :
        if commands == list_of_data[i][0] :
            list_of_data.remove(list_of_data[i][: len(list_of_data[i])])
            write("Patient ",commands," is removed.\n")
            return
    write("Patient ",commands," cannot be removed due to absence.\n")        

def recommendation(patient) :
    patient = patient[0]
    for i in range(len(list_of_data)) :
        #calculating the risk and calling probability
        if patient == list_of_data[i][0] :
            a = list(list_of_data[i][5])
            a.remove('%')
            b = ''.join(a)
            risk = float(b)
            probability = calculating_probability([patient])
            if risk > probability :
                write("System suggests " , patient , " NOT to have the treatment.\n")
            else: 
                write("System suggests " , patient , " to have the treatment.\n")
            return
    write("Recommendation for ",patient," cannot be calculated due to absence.\n")

def check_command(commands) :
    commands = commands.split(' ')
    #splits for checking commands and makes it string againg for better sorting
    if commands[0] == 'create' :
        commands = ' '.join(commands)
        commands = sort_data(commands)
        create(commands)
    elif commands[0] =='remove' :
        commands = ' '.join(commands)
        commands = sort_data(commands)
        removedata(commands)
    elif commands[0] == 'recommendation':
        commands = ' '.join(commands)
        commands = sort_data(commands)
        recommendation(commands)
    elif commands[0] == 'probability':
        commands = ' '.join(commands)
        commands = sort_data(commands)
        writing_probability(commands)
    elif commands[0] == 'list\n' or commands[0] == 'list': 
        listing()
  

read()
list_of_data = []
for i in range(len(data)) :    
    check_command(data[i]) 