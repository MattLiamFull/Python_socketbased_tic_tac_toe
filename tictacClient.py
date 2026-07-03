#importing socket
import socket

#FUNCTIONS
#__________________________________________________________________
#function to allow a quick swap from protocal value ex: 0 to the charecter to be printed when printing board
def numXOswap(numXO):
    #create return string
    ret = " "
    #if block to fill ret string with right char
    if numXO == 0:
        ret = "X"
    elif numXO == 1:
        ret = "O"
    else:
        ret = " "
    #return
    return ret



#MAIN
#__________________________________________________________________
#the following code follows pal_client.py Code for CPSC 441 tutorials by Janet Leahy 
# IP and port number of the SERVER
HOST = '136.159.5.25'  #csx.cpsc.ucalgary.ca
PORT = 6969
print("what host would you like to connect to ('d' defauls to TIC TAC server ran by Janet Leahy at Ucalgary)")
HOST = input()
if HOST == "d":
    HOST = '136.159.5.25'  #csx.cpsc.ucalgary.ca
    PORT = 6969
else:
    print("what port would you like to connect too")
    PORT = int(input())

#set reciving socket as sock
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #variable used to break loop
    breakloop = False
    #connet with sock
    try:
        sock.connect((HOST, PORT))
        sock.sendall(b"EROR:this wil cause a error")
        justCatchesTheErrorReturned = sock.recv(1024)
        if justCatchesTheErrorReturned == "EROR:UNKNOWN CMD":
            print("connection has no problems")
    except socket.error as e:
        with open ("errorIsStoredHere.txt", "w+") as file:
            #write error to file
            file.write(str(e))
            print("Error connecting to server, error code has been saved to file: errorIsStoredHere.txt\nError Code:" + str(e))
            #close file
            file.close


        breakloop = True
        #write error code to file
    
    #game happening is true whena game is ongoing and will trap program in main game loop
    gameHappening = False

    #GAME VARIABLES
    #the 9 following variables are each of the sectors of the board: t(top) m(middle) b(bottom) followed by a int 1-3 for columb
    t1, t2, t3, m1, m2, m3, b1, b2, b3 = 0, 1, 0, 1, 0, 2, 2, 2, 2
    #the 9 following variables are each of the sectors but stored as a blank, X or O these
    #these are used for printing while the others are used for communication with server
    t1p, t2p, t3p, m1p, m2p, m3p, b1p, b2p, b3p = "X", "O", "X", "O", "X", " ", " ", " ", " "
    

    #loop until proper input is given
    #this loop is for the select menu, if load or new game is selected control will be given to game loop below
    while breakloop == False:
        #print header to give instructions
        print("WELCOME TO TIC TAK TOE:\n1) New game\n2) Load saved game\n3) Show score\n4) Exit")

        #recive input
        input1 = input()
        #depending on input do desired thing
        #newgame
        if input1 == "1":
            #break loop set to true
            breakloop = True
            #this var holds the players symbol X or O
            clientXO = "X"

            #send bit string to get new board
            sock.sendall(b"NEWG")
            #recive the new board into newBoard var
            newBoard = sock.recv(1024)
            #decode newBoard
            newBoard = newBoard.decode()

            #verify a BORD message was sent       
            if newBoard[:4] == "BORD":
                #assign each variable based on new board
                t1, t2, t3, m1, m2, m3, b1, b2, b3 = int(newBoard[5]), int(newBoard[7]), int(newBoard[9]), int(newBoard[11]), int(newBoard[13]), int(newBoard[15]), int(newBoard[17]), int(newBoard[19]), int(newBoard[21])
                
                #checking if server went first
                if (t1 == 0 or t2 == 0 or t3 == 0 or m1 == 0 or m2 == 0 or m3 == 0 or b1 == 0 or b2 == 0 or b3 == 0):
                    clientXO = "O"
                else:
                    clientXO = "X"
                #set game happening to true so game loop will start with the above gamestate
                gameHappening = True
            else:
                #no BORD message sent (AKA something went bad)
                print("Error: BORD msg was not sent in response too NEWG request")

        #load
        elif input1 == "2":
            #ask for input
            print("What is the name of the file where you would like to load (without the .txt: for example save.txt will be \"save\")\n")
            #take input
            input2 = input()
            input2 = input2 + ".txt"
            #the following code heavily uses: https://www.youtube.com/watch?v=gSbEXZvgyBw&ab_channel=Kludgeware
            #the following code heavily uses: https://stackoverflow.com/questions/57007680/how-to-handle-the-exception-when-input-file-does-not-exists-in-python
            #open file
            try:
                #try to open file
                with open (input2, 'r') as file:
                    #read file store in newBoard
                    filer = file.read()
                    #check if LOAD is avalable
                    if filer[:4] == "LOAD":
                        clientXO = filer[5]
                        #send bit string to get new board
                        sock.sendall(filer.encode())
                        #recive the new board into newBoard var
                        newBoard = sock.recv(1024)
                        #decode newBoard
                        newBoard = newBoard.decode()

                        #verify a BORD message was sent       
                        if newBoard[:4] == "BORD":
                            #assign each variable based on new board
                            t1, t2, t3, m1, m2, m3, b1, b2, b3 = int(newBoard[5]), int(newBoard[7]), int(newBoard[9]), int(newBoard[11]), int(newBoard[13]), int(newBoard[15]), int(newBoard[17]), int(newBoard[19]), int(newBoard[21])
                            #flag game as happening
                            gameHappening = True
                        else:
                            #no BORD message sent (AKA something went bad)
                            print("Error: BORD msg was not sent in response too LOAD request")
                    else:
                        print("File does not contain a LOAD: so game cannot load")
                    #close file
                    file.close
            #no file
            except FileNotFoundError:
                #means score is 0-0-0
                print("File does not exist")

            #breakloop (ending program)
            breakloop = True

        #score
        elif input1 == "3":
            #some vars to count score
            drawS = 0
            winS = 0
            loseS = 0 
            #the following code heavily uses: https://www.youtube.com/watch?v=gSbEXZvgyBw&ab_channel=Kludgeware
            #the following code heavily uses: https://stackoverflow.com/questions/57007680/how-to-handle-the-exception-when-input-file-does-not-exists-in-python
            #open score file
            try:
                #try to open score file
                with open ("scoreXO.txt", 'r') as file:
                    #read file store in filer
                    filer = file.read()
                    #count wins and loses and ties
                    for i in range(len(filer)):
                        if filer[i] == "0":
                            drawS = drawS + 1
                        elif filer[i] == "1":
                            winS = winS + 1
                        else:
                            loseS = loseS + 1
                    #print result
                    print("Wins: " + str(winS) + "\nLoses: " + str(loseS) + "\nDraws: " + str(drawS))
                    #close file
                    file.close
            #no file
            except FileNotFoundError:
                #means score is 0-0-0
                print("Wins: 0\nLoses: 0\nDraws: 0")

            #breakloop (ending program)
            breakloop = True

        #4 "Exit" breaks loop and ends connection with server
        elif input1 == "4":
            #break loop set to true
            breakloop = True
            #send bit string CLOS which ends connection according to protocal
            sock.sendall(b"CLOS")
            #gets response
            response = sock.recv(1024)
            #checks for CLOS from server
            if response == b"CLOS":
                print("Connection ended, thanks for playing")
            else:
                print("Connection failed to end according too protocal")

        else:
            #Give an error and have them restart the loop
            print("ERROR: Incorrect input, please enter an integer between 1 and 4\n")



    #MAIN GAME LOOP
    while gameHappening == True:
        #update all print vars as we will be printing a board, using numXOswap function defined above
        t1p, t2p, t3p, m1p, m2p, m3p, b1p, b2p, b3p = numXOswap(t1), numXOswap(t2), numXOswap(t3), numXOswap(m1), numXOswap(m2), numXOswap(m3), numXOswap(b1), numXOswap(b2), numXOswap(b3)
        
        #printing board
        print(t1p + " | " + t2p + " | " + t3p + "\n---------\n" + m1p + " | " + m2p + " | " + m3p + "\n---------\n" + b1p + " | " + b2p + " | " + b3p)
        
        #asking player for thier move
        print("\nWhat would you like to do: to place enter position (t1=top left, m2=middle, b3=bottom right), vb to veiw board, or sq to save and quit\n")
        #var to check if input is valid
        validInput = False
        #var to store server response
        serverRes = ""
        #loop to repeat if player gives invalid input
        while not validInput:
            #take input
            input1 = input()

            #big old if to see what player wants
#-------------------------------START OF CHECKING EVERY POSITIONAL INPUT--------------------------
            if input1 == "t1":
                #checks if t1 is blank
                if t1 == 2:
                    sock.sendall(b"MOVE:0,0")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            elif input1 == "t2":
                #checks if t2 is blank
                if t2 == 2:
                    sock.sendall(b"MOVE:0,1")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            elif input1 == "t3":
                #checks if t3 is blank
                if t3 == 2:
                    sock.sendall(b"MOVE:0,2")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            #
            #
            #some much needed breaks for orginization: above is top below is middle
            #
            #
            elif input1 == "m1":
                #checks if m1 is blank
                if m1 == 2:
                    sock.sendall(b"MOVE:1,0")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            elif input1 == "m2":
                #checks if m2 is blank
                if m2 == 2:
                    sock.sendall(b"MOVE:1,1")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            elif input1 == "m3":
                #checks if m3 is blank
                if m3 == 2:
                    sock.sendall(b"MOVE:1,2")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            #
            #
            #some much needed breaks for orginization: above is middle below is bottom
            #
            #
            elif input1 == "b1":
                #checks if b1 is blank
                if b1 == 2:
                    sock.sendall(b"MOVE:2,0")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            elif input1 == "b2":
                #checks if b2 is blank
                if b2 == 2:
                    sock.sendall(b"MOVE:2,1")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")
            elif input1 == "b3":
                #checks if b3 is blank
                if b3 == 2:
                    sock.sendall(b"MOVE:2,2")
                    #recive the response into serverRes var
                    serverRes = sock.recv(1024)
                    #decode serverRes
                    serverRes = serverRes.decode()
                    #make valid input true: as input is valid
                    validInput = True
                else:
                    #error for full space
                    print("space is not empty you cannot place there, try a dif input:\n")

#-------------------------------END OF CHECKING EVERY POSITIONAL INPUT--------------------------

            #now for the other posible inputs (sq/save and quit) and any other option
            elif input1 == "vb":
                #printing board
                print(t1p + " | " + t2p + " | " + t3p + "\n---------\n" + m1p + " | " + m2p + " | " + m3p + "\n---------\n" + b1p + " | " + b2p + " | " + b3p)
        
            elif input1 == "sq":
                print("What is the name of the file where you would like to save (without the .txt: for example save.txt will be \"save\")\n")
                input2 = input()
                #error handelling for pepole trying to save over score
                if input2 != "scoreXO" and input2 != "errorIsStoredHere":
                    input2 = input2 + ".txt"
                    #the following code heavily uses: https://www.youtube.com/watch?v=gSbEXZvgyBw&ab_channel=Kludgeware
                    #just append winner into file (which is just a long list of winners)
                    with open (input2, "w+") as file:
                        #write board state in form of a load statment
                        file.write("LOAD:" + clientXO + "," + str(t1) + "," + str(t2) + "," + str(t3) + "," + str(m1) + "," + str(m2) + "," + str(m3) + "," + str(b1) + "," + str(b2) + "," + str(b3))
                        #close file
                        file.close

                    print("thanks for saving\n")

                    #send bit string CLOS which ends connection according to protocal
                    sock.sendall(b"CLOS")
                    #gets response
                    serverRes = sock.recv(1024)

                    #mark valid input
                    validInput = True
                else:
                    #telling pepole not to save over score
                    print("you cant save too the file scoreXO.txt or errorIsStoredHere.txt those are important: the game will close now")
                    
                    #send bit string CLOS which ends connection according to protocal
                    sock.sendall(b"CLOS")
                    #gets response
                    response = sock.recv(1024)
                    #checks for CLOS from server
                    if response != b"CLOS":
                        print("Connection failed to end according too protocal")
                    
                    #set input valid to break loop
                    validInput = True
                    #set server response to close to simulate a CLOS response
                    serverRes = b"CLOS"
            else:
                #print error
                print("error not a valid input")
                #asking player for thier move
                print("\nWhat would you like to do: to place enter position (t1=top left, m2=middle, b3=bottom right) or sq to save and quit\n")
        #we have now recived input

        #check what serer sent as response
        #EROR
        if serverRes[:4] == "EROR":
            #UNKNOWN COMMAND ERROR
            if serverRes[5] == "U":
                print("Server recived UNKNOWN COMMAND error: make sure a MOVE command was sent")
                gameHappening = False
            #UNKNOWN COMMAND ERROR
            elif serverRes[5] == "N":
                print("Server recived NO GAME error: trace the game happening variable")
                gameHappening = False
            #UNKNOWN COMMAND ERROR
            elif serverRes[5] == "B":
                print("Server recived BAD MOVE error: check local error checking and MOVE: commands")
                gameHappening = False

        #BORD
        elif serverRes[:4] == "BORD":
            #assign each variable based on new board
            t1, t2, t3, m1, m2, m3, b1, b2, b3 = int(serverRes[5]), int(serverRes[7]), int(serverRes[9]), int(serverRes[11]), int(serverRes[13]), int(serverRes[15]), int(serverRes[17]), int(serverRes[19]), int(serverRes[21])

        #OVER
        elif serverRes[:4] == "OVER":
            #int stores 1 for win, 2 for lose, 0 for tie
            winlose = 0
            if serverRes[5] == "C":
                print("You win good job")
                winlose = 1
            elif serverRes[5] == "S":
                print("You lost")
                winlose = 2
            else:
                print("TIE GAME")
            print("\nfinal board state:")
            #update vars
            t1, t2, t3, m1, m2, m3, b1, b2, b3 = int(serverRes[7]), int(serverRes[9]), int(serverRes[11]), int(serverRes[13]), int(serverRes[15]), int(serverRes[17]), int(serverRes[19]), int(serverRes[21]), int(serverRes[23])
            #update all print vars as we will be printing a board, using numXOswap function defined above
            t1p, t2p, t3p, m1p, m2p, m3p, b1p, b2p, b3p = numXOswap(t1), numXOswap(t2), numXOswap(t3), numXOswap(m1), numXOswap(m2), numXOswap(m3), numXOswap(b1), numXOswap(b2), numXOswap(b3)
        
            #printing board
            print(t1p + " | " + t2p + " | " + t3p + "\n---------\n" + m1p + " | " + m2p + " | " + m3p + "\n---------\n" + b1p + " | " + b2p + " | " + b3p)

            #gameHappening false
            gameHappening = False


            #the following code heavily uses: https://www.youtube.com/watch?v=gSbEXZvgyBw&ab_channel=Kludgeware
            #just append winner into file (which is just a long list of winners)
            with open ("scoreXO.txt", "a+") as file:
                #append winner
                file.write(str(winlose))
                #close file
                file.close




        #checks for CLOS from server
        elif serverRes == b"CLOS":
            print("Connection ended, thanks for playing")
            gameHappening = False

        #error chek
        else:
            print("Server sent something unexpected in response to MOVE:")
            gameHappening = False
        






