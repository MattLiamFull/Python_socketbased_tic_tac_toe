# Python_socketbased_tic_tac_toe
Making use of python to create a multiplayer tictactoe client with saves
# Resorces Folder Is TA Supplied and was used as Ref

# Read ME
To run just run use: (python tictacClient.py) while in directory of the file

Can connect to any server or port, just input d if you would like to quickly access the standard tictac server port

use t1-t3 m1-m3 b1-b3 to specify where you would to place your mark, other inputs result in asking again

Score will be saved in a file called scoreXO.txt:
    -if file does not exist it will be created

Load and save can use any file you specify:
    -dont use "errorIsStoredHere.txt" or "scoreXO.txt" as the overrides will cause problems, if you try program ends after telling you why

known bugs:
1)If you manually edit save file to contain LOAD:3,3,36,7,8,2,chair stuff will break essentially values are stored in ints that are
expected to be 0, 1, or 2 antthing else breaks the game
2)If you manually edit the score file to contain non 0, 1, or 2 charecters score will break as it counts the ints
3)If client breaks protocal most of the time it just breaks, sometimes you get an error message, sometimes you dont
if it sends random stuff you probably get an error message
if it sends something that looks like protocal but is not example: LOAD:I LOVE BREAKING PEPOLES CODE it will likely just loop 

NOTES:
assignment dident say if score was to be score per session or saved locally, I saved it locally

to play another round, rerun the program as both score and save are on files i did not make the main menu revisitable (only occured to me now that thats something pepole like)

error codes for connection errors wil the server are stored locally in a file