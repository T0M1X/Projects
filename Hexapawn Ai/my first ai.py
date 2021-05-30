import random
import time
import numpy as np
import sqlite3
global board

board=[[1,1,1],
       [0,0,0],
       [2,2,2]]

winner="maybe"

con=sqlite3.connect("hexapawn.db")
file=open("winners.txt","a+")
c=con.cursor()
c.execute("CREATE TABLE IF NOT EXISTS states(state TEXT, Moves INTEGAR, aw INTEGAR, bw INTEGAR, cw INTEGAR, dw INTEGAR)")


def showBoard():
    for i in range(0,3):
        print(board[i])

def checkMove(piece,kill):
    if board[int(piece[0])][int(piece[1])] == 2:
        if kill == "a":
            if board[int(piece[0])-1][int(piece[1])] == 0:
                board[int(piece[0])-1][int(piece[1])]=2
                board[int(piece[0])][int(piece[1])]=0
            else:
                return False
        elif kill == "b":
            if int(piece[1]) == 2:
                if board[int(piece[0])-1][1] == 1:
                    board[int(piece[0])-1][1]=2
                    board[int(piece[0])][int(piece[1])]=0
                else:
                    return False
            if int(piece[1]) == 1:
                if board[int(piece[0])-1][0] == 1:
                     board[int(piece[0])-1][0]=2
                     board[int(piece[0])][int(piece[1])]=0
                elif board[int(piece[0])-1][2] == 1:
                     board[int(piece[0])-1][2]=2
                     board[int(piece[0])][int(piece[1])]=0
                else:
                    return False
            if int(piece[1]) == 0:
                if board[int(piece[0])-1][1] == 1:
                     board[int(piece[0])-1][1]=2
                     board[int(piece[0])][int(piece[1])]=0
                else:
                    return False
        else:
            return False
    else:
        return False
    return True

def moves():
    possibleMoves=0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == 1:
                if board[i+1][j] == 0:
                    possibleMoves=possibleMoves+1
                if j == 0 or j == 2:
                    if board[i+1][1] == 2:
                        possibleMoves=possibleMoves+1
                if j == 1:
                    if board[i+1][0] == 2:
                        possibleMoves=possibleMoves+1
                    if board[i+1][2] == 2:
                        possibleMoves=possibleMoves+1
    return possibleMoves

def move(possibleMoves):
    global total
    global value
    global aw
    global bw
    global cw
    global dw
    total=0
    value=""
    for i in range(0,3):
        for j in range(0,3):
            value=value+str(board[i][j])
    c.execute("SELECT aw FROM states WHERE state=?",
              (value,))
    if c.fetchall() == []:
        c.execute("INSERT INTO states(state,Moves,aw,bw,cw,dw)VALUES(?,?,0,0,0,0)",
                  (value,possibleMoves))
        aw=0
        bw=0
        cw=0
        dw=0
        con.commit()
    else:
        c.execute("SELECT aw,bw,cw,dw FROM states WHERE state=?",
              (value,))
        weights=c.fetchall()
        aw=weights[0][0]
        bw=weights[0][1]
        cw=weights[0][2]
        dw=weights[0][3]
    if possibleMoves == 1:
        rand=np.random.choice([1], p=[(1+aw)])
    if possibleMoves == 2:
        rand=np.random.choice([1,2], p=[(1+aw)/2,(1+bw)/2])
    if possibleMoves == 3:
        rand=np.random.choice([1,2,3], p=[(1+aw)/3,(1+bw)/3,(1+cw)/3])
    if possibleMoves == 4:
        rand=np.random.choice([1,2,3,4], p=[(1+aw)/4,(1+bw)/4,(1+cw)/4,(1+dw)/4])
    values[0].append(value)
    values[1].append(possibleMoves)
    values[2].append(rand)
    count=0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == 1:
                if i == 2:
                    break
                if board[i+1][j] == 0:
                    count=count+1
                    if count == rand:
                        board[i+1][j]=1
                        board[i][j]=0
                if j == 0 or j == 2:
                    if board[i+1][1] == 2:
                        count=count+1
                        if count == rand:
                            board[i+1][1]=1
                            board[i][j]=0
                if j == 1:
                    if board[i+1][0] == 2:
                        count=count+1
                        if count == rand:
                            board[i+1][0]=1
                            board[i][j]=0
                    if board[i+1][2] == 2:
                        count=count+1
                        if count == rand:
                            board[i+1][2]=1
                            board[i][j]=0


again=True
while again == True:
    gameOver=False
    global values
    values=[[],[],[]]
    while gameOver == False:
        showBoard()
        piece=input("Which piece would you like to move: ")
        kill=input("Type a to move forward or b to kill or c to surrender: ")
        if kill == "c":
            winner="Ai"
            gameOver=True
            break
        while checkMove(piece,kill) == False:
            piece=input("Which piece would you like to move: ")
            kill=input("Type a to move forward or b to kill or c to surrender: ")
            if kill == "c":
                winner="Ai"
                gameOver=True
                break
        showBoard()
        if moves()==0:
            gameOver=True
            winner="User"
            break
        for i in range(0,3):
            if board[0][i] == 2:
                winner="User"
                gameOver=True
        pieces=0
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == 1:
                    pieces=pieces+1
        if pieces == 0:
            winner="User"
            gameOver=True
        if gameOver == True:
            break
        time.sleep(1)
        print("-----------------------")
        move(moves())
        pieces=0
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == 2:
                    pieces=pieces+1
        if pieces == 0:
            winner="Ai"
            gameOver=True
            break
        for i in range(0,3):
            if board[0][i] == 2:
                winner="User"
                gameOver=True
            if board[2][i] == 1 and winner == "maybe":
                winner="Ai"
                gameOver=True
    if winner == "Ai":
        showBoard()
    print("Game Over")
    print("Winner Is",winner)
    p=input("Enter 'no' to stop the game: ")
    if p == "no":
        again=False
    board=[[1,1,1],
           [0,0,0],
           [2,2,2]]
    if winner == "Ai":
        file.write("Ai\n")
        for i in range(0,len(values[0])):
            c.execute("SELECT aw,bw,cw,dw FROM states WHERE state=?",
              (values[0][i],))
            weights=c.fetchall()
            aw=weights[0][0]
            bw=weights[0][1]
            cw=weights[0][2]
            dw=weights[0][3]
            if values[1][i]==2:
                if values[2][i] == 1:
                    aw=aw+0.2
                    bw=bw-0.2
                else:
                    aw=aw-0.2
                    bw=bw+0.2
                if aw >= -1 and bw >= -1:
                    c.execute("UPDATE states SET aw=?, bw=? WHERE state=?",
                              (aw,bw,values[0][i]))
                con.commit()
            if values[1][i]==3:
                if values[2][i] == 1:
                    aw=aw+0.4
                    bw=bw-0.2
                    cw=cw-0.2
                elif values[2][i] == 2:
                    aw=aw-0.2
                    bw=bw+0.4
                    cw=cw-0.2
                else:
                    aw=aw-0.2
                    bw=bw-0.2
                    cw=cw+0.4
                if aw >= -1 and bw >= -1 and cw >= -1:
                    c.execute("UPDATE states SET aw=?, bw=?, cw=? WHERE state=?",
                              (aw,bw,cw,values[0][i]))
                con.commit()
            if values[1][i]==4:
                if values[2][i] == 1:
                    aw=aw+0.6
                    bw=bw-0.2
                    cw=cw-0.2
                    dw=dw-0.2
                elif values[2][i] == 2:
                    aw=aw-0.2
                    bw=bw+0.6
                    cw=cw-0.2
                    dw=dw-0.2
                elif values[2][i] == 3:
                    aw=aw-0.2
                    bw=bw-0.2
                    cw=cw+0.6
                    dw=dw-0.2
                else:
                    aw=aw-0.2
                    bw=bw-0.2
                    cw=cw-0.2
                    dw=dw+0.6
                if aw >= -1 and bw >= -1 and cw >= -1 and dw >= -1:
                    c.execute("UPDATE states SET aw=?, bw=?, cw=?, dw=? WHERE state=?",
                          (aw,bw,cw,dw,values[0][i]))
                con.commit()
    else:
        file.write("User\n")
        for i in range(0,len(values[0])):
            c.execute("SELECT aw,bw,cw,dw FROM states WHERE state=?",
              (values[0][i],))
            weights=c.fetchall()
            aw=weights[0][0]
            bw=weights[0][1]
            cw=weights[0][2]
            dw=weights[0][3]
            if values[1][i]==2:
                if values[2][i] == 1:
                    aw=aw-0.2
                    bw=bw+0.2
                else:
                    aw=aw+0.2
                    bw=bw-0.2
                if aw >= -1 and bw >= -1:
                    c.execute("UPDATE states SET aw=?, bw=? WHERE state=?",
                              (aw,bw,values[0][i]))
                con.commit()
            if values[1][i]==3:
                if values[2][i] == 1:
                    aw=aw-0.4
                    bw=bw+0.2
                    cw=cw+0.2
                elif values[2][i] == 2:
                    aw=aw+0.2
                    bw=bw-0.4
                    cw=cw+0.2
                else:
                    aw=aw+0.2
                    bw=bw+0.2
                    cw=cw-0.4
                if aw >= -1 and bw >= -1 and cw >= -1:
                    c.execute("UPDATE states SET aw=?, bw=?, cw=? WHERE state=?",
                              (aw,bw,cw,values[0][i]))
                con.commit()
            if values[1][i]==4:
                if values[2][i] == 1:
                    aw=aw-0.6
                    bw=bw+0.2
                    cw=cw+0.2
                    dw=dw+0.2
                elif values[2][i] == 2:
                    aw=aw+0.2
                    bw=bw-0.6
                    cw=cw+0.2
                    dw=dw+0.2
                elif values[2][i] == 3:
                    aw=aw+0.2
                    bw=bw+0.2
                    cw=cw-0.6
                    dw=dw+0.2
                else:
                    aw=aw+0.2
                    bw=bw+0.2
                    cw=cw+0.2
                    dw=dw-0.6
                if aw >= -1 and bw >= -1 and cw >= -1 and dw >= -1:
                    c.execute("UPDATE states SET aw=?, bw=?, cw=?, dw=? WHERE state=?",
                          (aw,bw,cw,dw,values[0][i]))
                con.commit()
    winner="maybe"
    con.commit()
file.close()
c.close()
con.close()
