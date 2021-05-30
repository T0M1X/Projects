import pygame
import time
import random
import sqlite3
import hashlib
import uuid
pygame.init()
width=960
height=570
black=(0,0,0)
white=(255,255,255)
green=(0,176,80)
red=(237,28,36)
blue=(63,72,204)
Dgrey=(68,68,68)
Lgrey=(180,180,180)
purple=(148,0,255)
yellow=(255,242,0)
bblue=(153,217,234)
orange=(255,127,39)
pink=(255,0,128)
colours={"black":black,"white":white,"green":green,"red":red,"blue":blue,
         "dark grey":Dgrey,"light grey":Lgrey,"purple":purple,"yellow":yellow,
         "baby blue":bblue,"orange":orange,"pink":pink}
keys={273:"up arrow",274:"down arrow",276:"left arrow",275:"right arrow",
      264:"keypad 8",261:"keypad 5",260:"keypad 4",262:"keypad 6",259:"keypad 3",
      258:"keypad 2",257:"keypad 1",263:"keypad 7",265:"keypad 9"}
munch=pygame.mixer.Sound("munch.wav")
gameWin=pygame.mixer.Sound("win.wav")
loss=pygame.mixer.Sound("game over.wav")
newHigh=pygame.mixer.Sound("highscore.wav")
clickNoise=pygame.mixer.Sound("click.wav")
myFont="Youngsook BTN.ttf"
paused=False
view=pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake With Friends")
rate=pygame.time.Clock()

con=sqlite3.connect("SnakeWithFriends.db")
c=con.cursor()
c.execute("CREATE TABLE IF NOT EXISTS accounts(username TEXT,password TEXT, p1up INTEGAR, p1down INTEGAR, p1left INTEGAR, p1right INTEGAR, p2up INTEGAR, p2down INTEGAR, p2left INTEGAR, p2right INTEGAR, p3up INTEGAR, p3down INTEGAR, p3left INTEGAR, p3right INTEGAR, p4up INTEGAR, p4down INTEGAR, p4left INTEGAR, p4right INTEGAR, p1colour TEXT, p2colour TEXT, p3colour TEXT, p4colour TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS highScores(username TEXT, score INTEGAR)")

def hashy(text):
    salt = uuid.uuid4().hex
    return hashlib.sha512(salt.encode()+text.encode()).hexdigest()+':'+salt
def checkPassword(hashed,newPass):
    password, salt = hashed.split(':')
    if password == hashlib.sha512(salt.encode() + newPass.encode()).hexdigest():
         return True
    else:
        return False

def intro():
    over=True
    midTitle=newText(" nake With Friend ",80,myFont,white,480,200)
    endTitle=newText("S                              S",80,myFont,green,480,200)
    log=button("-Log in",50,myFont,white,405,400,150,70,black,green,logIn)
    reg=button("-Register",50,myFont,white,375,300,210,70,black,blue,createAccount)
    finish=button("Quit",38,myFont,white,886,523,90,50,black,red,quitGame)
    global event
    while over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        midTitle.showJustText()
        endTitle.showJustText()
        log.checkClicked()
        reg.checkClicked()
        finish.checkClicked()
        pygame.display.flip()
    
def logIn():
    global afk
    global account
    account=""
    afk=True
    tempPass=""
    wrong=False
    title=newText("Sign In",70,myFont,green,480,70)
    userN=newText("Enter Your Username",50,myFont,blue,480,160)
    givenUser=textBox("",50,None,black,230,200,500,35,Lgrey,white)
    passW=newText("Enter Your Password",50,myFont,blue,480,360)
    givenPass=textBox("",50,None,black,230,400,500,35,Lgrey,white)
    finish=button("Back",38,myFont,white,0,0,100,50,black,green,back)
    enter=newText("Press Enter To Continue",20,myFont,white,480,550)
    end=button("Quit",38,myFont,white,886,523,90,50,black,red,quitGame)
    wrongUP=newText("Your Username Or Password Is Incorrect",40,myFont,red,480,510)
    global event
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    givenUser.place=False
                    givenPass.place=True
                if givenUser.place == True:
                    if event.key == pygame.K_BACKSPACE:
                        givenUser.text=givenUser.text[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        givenUser.place=False
                        givenPass.place=True
                    elif len(givenUser.text) < 15:
                        givenUser.text=givenUser.text+event.unicode
                if givenPass.place == True:
                    if event.key == pygame.K_RETURN:
                        givenPass.place=False
                        c.execute("SELECT password FROM accounts WHERE username=?",
                                  (givenUser.text,))
                        password=c.fetchall()
                        if password != []:
                            if checkPassword(password[0][0],tempPass) == True: 
                                account=givenUser.text
                                mainMenu()
                        wrong=True
                    elif event.key == pygame.K_BACKSPACE:
                        givenPass.text=givenPass.text[:-1]
                        tempPass=tempPass[:-1]
                    elif event.key == pygame.K_TAB:
                        pass
                    elif len(givenPass.text) < 30:
                        givenPass.text=""
                        tempPass=tempPass+event.unicode
                        for i in range(0,len(tempPass)):
                            givenPass.text=givenPass.text+"*"
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        title.showJustText()
        givenUser.click()
        userN.showJustText()
        passW.showJustText()
        givenPass.click()
        finish.checkClicked()
        enter.showJustText()
        end.checkClicked()
        if wrong == True:
            wrongUP.showJustText()
        pygame.display.flip()
        
def createAccount():
    global afk
    afk=True
    wrong=False
    taken=False
    short=False
    tempPass1=""
    tempPass2=""
    title=newText("Register Account",70,myFont,green,480,70)
    userN=newText("Enter Your Username 3-15 Characters",40,myFont,blue,480,140)
    givenUser=textBox("",50,None,black,230,170,500,35,Lgrey,white)
    passW1=newText("Enter Your Password 5-30 Characters)",40,myFont,blue,480,270)
    givenPass1=textBox("",50,None,black,230,300,500,35,Lgrey,white)
    passW2=newText("Enter Your Password Again 5-30 Characters",40,myFont,blue,480,400)
    givenPass2=textBox("",50,None,black,230,430,500,35,Lgrey,white)
    wrongPass=newText("The Passwords Do Not Match",40,myFont,red,480,510)
    finish=button("Back",38,myFont,white,0,0,100,50,black,green,back)
    userTaken=newText("That Username Is Taken",40,myFont,red,480,510)
    shortUP=newText("Your Username Or Password Is Too Short",40,myFont,red,480,510)
    enter=newText("Press Enter To Continue",20,myFont,white,480,550)
    end=button("Quit",38,myFont,white,886,523,90,50,black,red,quitGame)
    global event
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    givenUser.place=False
                    givenPass1.place=False
                    givenPass2.place=True
                if event.key == pygame.K_TAB:
                    afk=True
                if givenUser.place == True:
                    if event.key == pygame.K_BACKSPACE:
                        givenUser.text=givenUser.text[:-1]
                    elif len(givenUser.text) < 15:
                        givenUser.text=givenUser.text+event.unicode
                if givenPass1.place == True:
                    if event.key == pygame.K_BACKSPACE:
                        givenPass1.text=givenPass1.text[:-1]
                        tempPass1=tempPass1[:-1]
                    elif len(givenPass1.text) < 30:
                        givenPass1.text=givenPass1.text+"*"
                        tempPass1=tempPass1+event.unicode
                if givenPass2.place == True:
                    if event.key == pygame.K_RETURN:
                        givenPass2.place=False
                        taken=False
                        wrong=False
                        short=False
                        if len(givenUser.text) > 2 and len(givenPass1.text) > 4:
                            short=False
                            if tempPass1 == tempPass2:
                                wrong=False
                                c.execute("SELECT username FROM accounts WHERE username=?",
                                          (givenUser.text,))
                                if c.fetchall() == []:
                                    c.execute("INSERT INTO accounts(username,password,p1up,p1down,p1left,p1right,p2up,p2down,p2left,p2right,p3up,p3down,p3left,p3right,p4up,p4down,p4left,p4right,p1colour,p2colour,p3colour,p4colour)VALUES(?,?,273,274,276,275,119,115,97,100,105,107,106,108,264,261,260,262,'green','blue','red','yellow')",
                                              (givenUser.text,hashy(tempPass1)))
                                    con.commit()
                                    logIn()
                                else:
                                    taken=True
                            else:
                                wrong=True
                        else:
                            short=True
                    elif event.key == pygame.K_BACKSPACE:
                        givenPass2.text=givenPass2.text[:-1]
                        tempPass2=tempPass2[:-1]
                    elif event.key == pygame.K_TAB:
                        pass
                    elif len(givenPass1.text) < 30:
                        givenPass2.text=givenPass2.text+"*"
                        tempPass2=tempPass2+event.unicode
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        title.showJustText()
        givenUser.click()
        userN.showJustText()
        passW1.showJustText()
        givenPass1.click()
        passW2.showJustText()
        givenPass2.click()
        enter.showJustText()
        if wrong == True:
            wrongPass.showJustText()
        if taken == True:
            userTaken.showJustText()
        if short == True:
            shortUP.showJustText()
        end.checkClicked()
        finish.checkClicked()
        pygame.display.flip()
    

        
class snake:
    def __init__(self,coordinates,snakew,snakeh,colour,length,direction,up,down,left,right,score):
        self.coordinates=coordinates
        self.snakew=snakew
        self.snakeh=snakeh
        self.colour=colour
        self.length=length
        self.direction=direction
        self.up=up
        self.down=down
        self.left=left
        self.right=right
        self.dead=False
        self.score=score
    def makeSnake(self):
        for i in range(0,len(self.coordinates)):
            pygame.draw.rect(view,self.colour, [self.coordinates[i][0]*20,self.coordinates[i][1]*20,self.snakew,self.snakeh])
    def grow(self):
        pygame.mixer.Sound.play(munch)
        self.coordinates=self.coordinates+[[self.coordinates[len(self.coordinates)-1][0],self.coordinates[len(self.coordinates)-1][1]]]
        self.length=self.length+1
    def changeDir(self,event):
        if event.key == self.right and self.coordinates[0][0] != self.coordinates[1][0]-1:
            self.direction="right"
        elif event.key == self.left and self.coordinates[0][0] != self.coordinates[1][0]+1:
            self.direction="left"
        elif event.key == self.up and self.coordinates[0][1] != self.coordinates[1][1]+1:
            self.direction="up"
        elif event.key == self.down and self.coordinates[0][1] != self.coordinates[1][1]-1:
            self.direction="down"
    def movement(self):
        for i in range(len(self.coordinates)-1,0,-1):
            self.coordinates[i][0]=self.coordinates[i-1][0]
            self.coordinates[i][1]=self.coordinates[i-1][1]
        if self.direction == "right":
            self.coordinates[0][0]=self.coordinates[0][0]+1
        elif self.direction == "left":
            self.coordinates[0][0]=self.coordinates[0][0]-1
        elif self.direction == "up":
            self.coordinates[0][1]=self.coordinates[0][1]-1
        elif self.direction =="down":
            self.coordinates[0][1]=self.coordinates[0][1]+1

class food:
    def __init__(self,x_co,y_co,colour):
        self.x_co=x_co
        self.y_co=y_co
        self.colour=colour
    def createFood(self):
        pygame.draw.rect(view,self.colour, [self.x_co*20,self.y_co*20,20,20])
    def spawn(self):
        self.x_co = random.randint(0,47)
        self.y_co = random.randint(0,25)

class newText:
    def __init__(self,text,size,font,colour,xplace,yplace):
        self.text=text
        self.size=size
        self.font=font
        self.colour=colour
        self.xplace=xplace
        self.yplace=yplace
    def mainText(self,textProp):
        textSquare=textProp.render(self.text,True,self.colour)
        return textSquare,textSquare.get_rect()
    def showJustText(self):
        textType=pygame.font.Font(self.font,self.size)
        textS,textR=self.mainText(textType)
        textR.center=(self.xplace,self.yplace)
        view.blit(textS,textR)
    def addText(self):
        font=pygame.font.Font(self.font,self.size)
        text=font.render(self.text,False,self.colour)
        view.blit(text,(self.xplace,self.yplace))

class textBox(newText):
    def __init__(self,text,size,font,colour,xplace,yplace,width,height,bColour,newColour):
        newText.__init__(self,text,size,font,colour,xplace,yplace)
        self.width=width
        self.height=height
        self.bColour=bColour
        self.newColour=newColour
        self.place=False
    def makeBox(self):
        if self.xplace < mouse[0] < (self.xplace+self.width) and self.yplace < mouse[1] < (self.yplace+self.height) and click[0]==1:
            self.place=True
        if ((self.xplace > mouse[0] or mouse[0] > (self.xplace+self.width)) or (self.yplace > mouse[1] or mouse[1] > (self.yplace+self.height))):
            if click[0]==1:
             self.place=False
    def click(self):
        self.makeBox()
        if self.place == True:
            pygame.draw.rect(view,self.newColour, [self.xplace,self.yplace,self.width,self.height])
        else:
            pygame.draw.rect(view,self.bColour, [self.xplace,self.yplace,self.width,self.height])
        self.addText()

class button(textBox):
    def __init__(self,text,size,font,colour,xplace,yplace,width,height,bColour,newColour,action=None):
        textBox.__init__(self,text,size,font,colour,xplace,yplace,width,height,bColour,newColour)
        self.action=action
    def makeButton(self):
        if self.xplace < mouse[0] < (self.xplace+self.width) and self.yplace < mouse[1] < (self.yplace+self.height):
            pygame.draw.rect(view,self.newColour, [self.xplace,self.yplace,self.width,self.height])
            self.place=True
        else:
            pygame.draw.rect(view,self.bColour, [self.xplace,self.yplace,self.width,self.height])
            self.place=False
        self.addText()
    def checkClicked(self):
        self.makeButton()
        if self.place==True and click[0]==1 and self.action != None:
            pygame.mixer.Sound.play(clickNoise)
            self.action()
    def clicked(self):
        self.makeButton()
        if self.place==True and click[0]==1:
            return True
        else:
            return False

def mainMenu():
    menu=True
    global count
    global waitTime
    global difficulty
    count=0
    waitTime=160
    difficulty="normal"
    midHeading=newText(" nake With Friend ",60,myFont,white,480,100)
    endHeading=newText("S                              S",60,myFont,green,480,100)
    singlemode=button("Single Player",30,myFont,black,61,300,175,45,white,blue,controls)
    multimode=button("MultiPlayer",30,myFont,black,297,300,155,45,white,blue,pickPlayer)
    scores=button("High Score Board",30,myFont,black,513,300,230,45,white,blue,highScoreBoard)
    options=button("Options",30,myFont,black,804,300,95,45,white,blue,option)
    pickAccount=button("Sign Out",38,myFont,white,820,0,140,50,black,blue,intro)
    end=button("Quit",38,myFont,white,886,523,90,50,black,red,quitGame)
    global event
    while menu==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        midHeading.showJustText()
        endHeading.showJustText()
        singlemode.checkClicked()
        multimode.checkClicked()
        scores.checkClicked()
        options.checkClicked()
        end.checkClicked()
        pickAccount.checkClicked()
        pygame.display.flip()

def keyName(asc):
    if asc in keys:
        return keys[asc]
    else:
        return pygame.key.name(asc)

def quitGame():
    con.commit()
    c.close()
    con.close()
    pygame.quit()
    quit()
    
def resume():
    global paused
    paused = False

def pause():
    global paused
    paused=True
    timer=0
    pauseText=newText("Paused",60,myFont,green,480,260)
    cont=button("-Resume",38,myFont,white,400,350,140,50,black,green,resume)
    menu=button("-Main menu",38,myFont,white,400,400,190,50,black,blue,mainMenu)
    end=button("-Quit",38,myFont,white,400,450,90,50,black,red,quitGame)
    while paused==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        pauseText.showJustText()
        cont.checkClicked()
        menu.checkClicked()
        end.checkClicked()
        pygame.display.flip()

def back():
    global afk
    afk = False

def makep1():
    global account
    global p1
    global up1
    global down1
    global left1
    global right1
    global colour1
    c.execute("SELECT p1up, p1down, p1left, p1right, p1colour FROM accounts WHERE username=?",
              (account,))
    p1=c.fetchall()
    up1=keyName(p1[0][0])
    down1=keyName(p1[0][1])
    left1=keyName(p1[0][2])
    right1=keyName(p1[0][3])
    colour1=colours[p1[0][4]]
def makep2():
    global account
    global p2
    global up2
    global down2
    global left2
    global right2
    global colour2
    c.execute("SELECT p2up, p2down, p2left, p2right, p2colour FROM accounts WHERE username=?",
              (account,))
    p2=c.fetchall()
    if p2[0][0] in keys:
        up2=keys[p2[0][0]]
    else:
        up2=pygame.key.name(p2[0][0])
    if p2[0][1] in keys:
        down2=keys[p1[0][1]]
    else:
        down2=pygame.key.name(p2[0][1])
    if p2[0][2] in keys:
        left2=keys[p2[0][2]]
    else:
        left2=pygame.key.name(p2[0][2])
    if p2[0][3] in keys:
        right2=keys[p2[0][3]]
    else:
        right2=pygame.key.name(p2[0][3])
    colour2=colours[p2[0][4]]
def makep3():
    global account
    global p3
    global up3
    global down3
    global left3
    global right3
    global colour3
    c.execute("SELECT p3up, p3down, p3left, p3right, p3colour FROM accounts WHERE username=?",
              (account,))
    p3=c.fetchall()
    if p3[0][0] in keys:
        up3=keys[p3[0][0]]
    else:
        up3=pygame.key.name(p3[0][0])
    if p3[0][1] in keys:
        down3=keys[p3[0][1]]
    else:
        down3=pygame.key.name(p3[0][1])
    if p3[0][2] in keys:
        left3=keys[p3[0][2]]
    else:
        left3=pygame.key.name(p3[0][2])
    if p3[0][3] in keys:
        right3=keys[p3[0][3]]
    else:
        right3=pygame.key.name(p3[0][3])
    colour3=colours[p3[0][4]]
def makep4():
    global account
    global p4
    global up4
    global down4
    global left4
    global right4
    global colour4
    c.execute("SELECT p4up, p4down, p4left, p4right, p4colour FROM accounts WHERE username=?",
              (account,))
    p4=c.fetchall()
    if p4[0][0] in keys:
        up4=keys[p4[0][0]]
    else:
        up4=pygame.key.name(p4[0][0])
    if p4[0][1] in keys:
        down4=keys[p4[0][1]]
    else:
        down4=pygame.key.name(p4[0][1])
    if p4[0][2] in keys:
        left4=keys[p4[0][2]]
    else:
        left4=pygame.key.name(p4[0][2])
    if p4[0][3] in keys:
        right4=keys[p4[0][3]]
    else:
        right4=pygame.key.name(p4[0][3])
    colour4=colours[p4[0][4]]
    
def controls():
    global up1
    global down1
    global left1
    global right1
    global colour1
    makep1()
    upText=newText("Up - "+up1,40,myFont,colour1,480,150)
    downText=newText("Down - "+down1,40,myFont,colour1,480,210)
    leftText=newText("Left - "+left1,40,myFont,colour1,480,270)
    rightText=newText("Right - "+right1,40,myFont,colour1,480,330)
    bigText=newText("Controls",60,myFont,purple,480,40)
    endText=newText("Press space to continue",30,myFont,yellow,480,450)
    Next=button("Next",38,myFont,white, 435,500,90,50,black,blue,singlePlayer)
    finish=button("Back",38,myFont,white,0,0,100,50,black,blue,back)
    global afk
    afk=True
    global event
    while afk == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    afk=False
                    singlePlayer()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        upText.showJustText()
        downText.showJustText()
        leftText.showJustText()
        rightText.showJustText()
        bigText.showJustText()
        endText.showJustText()
        Next.checkClicked()
        finish.checkClicked()
        pygame.display.flip()

def singlePlayer():
    c.execute("SELECT score FROM highScores ORDER BY score DESC LIMIT 1")
    highScore=c.fetchall()
    global player1
    Food=food(random.randint(0,47),random.randint(0,25),red)
    timer=0
    leave=False
    global p1
    global colour1
    player1=snake([[2,15],[1,15],[0,15]],20,20,colour1,3,"right",p1[0][0],p1[0][1],p1[0][2],p1[0][3],0)
    score=newText("Score: "+str((player1.length-3)),40,myFont,white,0,520)
    stop=button("Pause",38,myFont,white,850,523,130,50,black,purple,pause)
    if len(highScore) != 0:
        highScoreText=newText("Highscore: "+str(highScore[0][0]),40,myFont,white,300,520)
    global event
    while leave==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if event.type == pygame.KEYDOWN:
                player1.changeDir(event)
                if event.key == pygame.K_p:
                    paused=True
                    pause()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        player1.makeSnake()
        if player1.coordinates[0][0] == Food.x_co and player1.coordinates[0][1] == Food.y_co:
            player1.grow()
            score.text="Score: "+str(player1.length-3)
            if len(highScore) != 0:
                if player1.length-3 > highScore[0][0]:
                    highScoreText.text="Highscore: "+str(player1.length-3)
                elif player1.length-3 == highScore[0][0]:
                    pygame.mixer.Sound.play(newHigh)
        for i in range(0,len(player1.coordinates)):
            if player1.coordinates[i][0] == Food.x_co and player1.coordinates[i][1] == Food.y_co:
                Food.spawn()
        Food.createFood()
        pygame.draw.rect(view,white, [0,520,960,3])
        score.addText()
        if len(highScore) != 0:
            highScoreText.addText()
        stop.checkClicked()
        pygame.display.flip()
        speed=rate.tick()
        timer=timer+speed
        if timer > waitTime:
            player1.movement()
            timer=0
        if player1.coordinates[0][0] >= 48 or player1.coordinates[0][0] < 0:
            gameOver()
        if player1.coordinates[0][1] >= 26 or player1.coordinates[0][1] < 0:
            gameOver()
        for i in range(2,len(player1.coordinates)):
            if player1.coordinates[0][0] == player1.coordinates[i][0] and player1.coordinates[0][1] == player1.coordinates[i][1]:
                gameOver()

def gameOver():
    pygame.mixer.Sound.play(loss)
    if waitTime == 160:
        c.execute("INSERT INTO highScores(username,score)VALUES(?,?)",
                  (account,player1.length-3))
        con.commit()
    global count
    global difficulty
    over=True
    if player1.length-3 < 20:
        count=count-1
    elif player1.length-3 >= 60:
        count=count+1
    else:
        count=0        
    bigText=newText("Game Over",60,myFont,green,480,260)
    cont=button("-Play again",38,myFont,white,400,350,195,50,black,green,singlePlayer)
    menu=button("-Main menu",38,myFont,white,400,400,190,50,black,blue,mainMenu)
    end=button("-Quit",38,myFont,white,400,450,90,50,black,red,quitGame)
    if count == -3 and difficulty == "normal":
        cont.action=easy
    elif count == 3 and difficulty == "normal":
        cont.action=hard
    if count > 0 and difficulty == "easy":
        cont.action=normal
    if count < 0 and difficulty == "hard":
        cont.action=normal
    global event
    while over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        bigText.showJustText()
        cont.checkClicked()
        menu.checkClicked()
        end.checkClicked()
        pygame.display.flip()

def easy():
    over=True
    bigText=newText("Would you like to play on easy mode?",60,myFont,blue,480,260)
    yes=button("Yes",38,myFont,black,240,400,65,50,white,green,makeEasy)
    no=button("No",38,myFont,black,650,400,50,50,white,red,resetCount)
    while over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        bigText.showJustText()
        yes.checkClicked()
        no.checkClicked()
        pygame.display.flip()
def makeEasy():
    global waitTime
    global difficulty
    global count
    waitTime=200
    difficulty="easy"
    count=0
    singlePlayer()

def normal():
    over=True
    bigText=newText("Would you like to play on normal mode?",60,myFont,blue,480,260)
    yes=button("Yes",38,myFont,black,240,400,65,50,white,green,makeNormal)
    no=button("No",38,myFont,black,650,400,50,50,white,red,resetCount)
    while over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        bigText.showJustText()
        yes.checkClicked()
        no.checkClicked()
        pygame.display.flip()
def makeNormal():
    global waitTime
    global difficulty
    global count
    waitTime=160
    difficulty="normal"
    count=0
    singlePlayer()

def hard():
    over=True
    bigText=newText("Would you like to play on Hard mode?",60,myFont,blue,480,260)
    yes=button("Yes",38,myFont,black,240,400,65,50,white,green,makeHard)
    no=button("No",38,myFont,black,650,400,50,50,white,red,resetCount)
    while over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        bigText.showJustText()
        yes.checkClicked()
        no.checkClicked()
        pygame.display.flip()
def makeHard():
    global waitTime
    global difficulty
    global count
    waitTime=120
    difficulty="hard"
    count=0
    singlePlayer()

def resetCount():
    global count
    count=0
    singlePlayer()

def pickPlayer():
    choice=newText("Choose the number of players",60,myFont,blue,480,100)
    play2=button("2 Players",38,myFont,black,120,345,165,50,white,yellow,players2)
    play3=button("3 Players",38,myFont,black,405,345,155,50,white,bblue,players3)
    play4=button("4 Players",38,myFont,black,680,345,160,50,white,purple,players4)
    finish=button("Back",38,myFont,white,0,0,100,50,black,green,back)
    global numPlayers
    numPlayers=1
    global afk
    afk=True
    global event
    while afk == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        choice.showJustText()
        play2.checkClicked()
        play3.checkClicked()
        play4.checkClicked()
        finish.checkClicked()
        pygame.display.flip()

def players2():
    global numPlayers
    global up1
    global down1
    global left1
    global right1
    global colour1
    makep1()
    global up2
    global down2
    global left2
    global right2
    global colour2
    makep2()
    numPlayers=2
    createPlayers()
    p1Text=newText("Player 1",40,myFont,colour1,240,100)
    p1upText=newText("Up - "+up1,40,myFont,colour1,240,160)
    p1downText=newText("Down - "+down1,40,myFont,colour1,240,220)
    p1leftText=newText("Left - "+left1,40,myFont,colour1,240,280)
    p1rightText=newText("Right - "+right1,40,myFont,colour1,240,340)
    p2Text=newText("Player 2",40,myFont,colour2,720,100)
    p2upText=newText("Up - "+up2,40,myFont,colour2,720,160)
    p2downText=newText("Down - "+down2,40,myFont,colour2,720,220)
    p2leftText=newText("Left - "+left2,40,myFont,colour2,720,280)
    p2rightText=newText("Right - "+right2,40,myFont,colour2,720,340)
    bigText=newText("Controls",50,myFont,purple,480,30)
    endText=newText("Press space to continue",30,myFont,bblue,480,480)
    Next=button("Next",38,myFont,white,435,520,90,50,black,blue,multiPlayer)
    finish=button("Back",38,myFont,white,0,520,100,50,black,green,pickPlayer)
    global afk
    afk=True
    global event
    while afk == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    afk=False
                    multiPlayer()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        p1Text.showJustText()
        p1upText.showJustText()
        p1downText.showJustText()
        p1leftText.showJustText()
        p1rightText.showJustText()
        p2Text.showJustText()
        p2upText.showJustText()
        p2downText.showJustText()
        p2leftText.showJustText()
        p2rightText.showJustText()
        bigText.showJustText()
        endText.showJustText()
        Next.checkClicked()
        finish.checkClicked()
        pygame.display.flip()
def players3():
    global up1
    global down1
    global left1
    global right1
    global colour1
    makep1()
    global up2
    global down2
    global left2
    global right2
    global colour2
    makep2()
    global up3
    global down3
    global left3
    global right3
    global colour3
    makep3()
    global numPlayers
    numPlayers=3
    createPlayers()
    p1Text=newText("Player 1",40,myFont,colour1,200,100)
    p1upText=newText("Up - "+up1,40,myFont,colour1,200,160)
    p1downText=newText("Down - "+down1,40,myFont,colour1,200,220)
    p1leftText=newText("Left - "+left1,40,myFont,colour1,200,280)
    p1rightText=newText("Right - "+right1,40,myFont,colour1,200,340)
    p2Text=newText("Player 2",40,myFont,blue,480,100)
    p2upText=newText("Up - "+up2,40,myFont,colour2,480,160)
    p2downText=newText("Down - "+down2,40,myFont,colour2,480,220)
    p2leftText=newText("Left - "+left2,40,myFont,colour2,480,280)
    p2rightText=newText("Right - "+right2,40,myFont,colour2,480,340)
    p3Text=newText("Player 3",40,myFont,colour3,760,100)
    p3upText=newText("Up - "+up3,40,myFont,colour3,760,160)
    p3downText=newText("Down - "+down3,40,myFont,colour3,760,220)
    p3leftText=newText("Left - "+left3,40,myFont,colour3,760,280)
    p3rightText=newText("Right - "+right3,40,myFont,colour3,760,340)
    bigText=newText("Controls",50,myFont,purple,480,30)
    endText=newText("Press space to continue",30,myFont,bblue,480,480)
    Next=button("Next",38,myFont,white,435,520,90,50,black,blue,multiPlayer)
    finish=button("Back",38,myFont,white,0,520,100,50,black,green,pickPlayer)
    global afk
    afk=True
    global event
    while afk == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    afk=False
                    multiPlayer()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        p1Text.showJustText()
        p1upText.showJustText()
        p1downText.showJustText()
        p1leftText.showJustText()
        p1rightText.showJustText()
        p2Text.showJustText()
        p2upText.showJustText()
        p2downText.showJustText()
        p2leftText.showJustText()
        p2rightText.showJustText()
        p3Text.showJustText()
        p3upText.showJustText()
        p3downText.showJustText()
        p3leftText.showJustText()
        p3rightText.showJustText()
        bigText.showJustText()
        endText.showJustText()
        Next.checkClicked()
        finish.checkClicked()
        pygame.display.flip()
def players4():
    global up1
    global down1
    global left1
    global right1
    global colour1
    makep1()
    global up2
    global down2
    global left2
    global right2
    global colour2
    makep2()
    global up3
    global down3
    global left3
    global right3
    global colour3
    makep3()
    global up4
    global down4
    global left4
    global right4
    global colour4
    makep4()
    global numPlayers
    numPlayers=4
    createPlayers()
    p1Text=newText("Player 1",30,myFont,colour1,160,100)
    p1upText=newText("Up - "+up1,30,myFont,colour1,160,160)
    p1downText=newText("Down - "+down1,30,myFont,colour1,160,220)
    p1leftText=newText("Left - "+left1,30,myFont,colour1,160,280)
    p1rightText=newText("Right - "+right1,30,myFont,colour1,160,340)
    p2Text=newText("Player 2",30,myFont,colour2,400,100)
    p2upText=newText("Up - "+up2,30,myFont,colour2,400,160)
    p2downText=newText("Down - "+down2,30,myFont,colour2,400,220)
    p2leftText=newText("Left - "+left2,30,myFont,colour2,400,280)
    p2rightText=newText("Right - "+right2,30,myFont,colour2,400,340)
    p3Text=newText("Player 3",30,myFont,colour3,600,100)
    p3upText=newText("Up - "+up3,30,myFont,colour3,600,160)
    p3downText=newText("Down - "+down3,30,myFont,colour3,600,220)
    p3leftText=newText("Left - "+left3,30,myFont,colour3,600,280)
    p3rightText=newText("Right - "+right3,30,myFont,colour3,600,340)
    p4Text=newText("Player 4",30,myFont,colour4,820,100)
    p4upText=newText("Up - "+up4,30,myFont,colour4,820,160)
    p4downText=newText("Down - "+down4,30,myFont,colour4,820,220)
    p4leftText=newText("Left - "+left4,30,myFont,colour4,820,280)
    p4rightText=newText("Right - "+right4,30,myFont,colour4,820,340)
    bigText=newText("Controls",50,myFont,purple,480,30)
    endText=newText("Press space to continue",30,myFont,bblue,480,480)
    Next=button("Next",38,myFont,white,435,520,90,50,black,blue,multiPlayer)
    finish=button("Back",38,myFont,white,0,520,100,50,black,green,pickPlayer)
    global afk
    afk=True
    global event
    while afk == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    afk=False
                    multiPlayer()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        p1Text.showJustText()
        p1upText.showJustText()
        p1downText.showJustText()
        p1leftText.showJustText()
        p1rightText.showJustText()
        p2Text.showJustText()
        p2upText.showJustText()
        p2downText.showJustText()
        p2leftText.showJustText()
        p2rightText.showJustText()
        p3Text.showJustText()
        p3upText.showJustText()
        p3downText.showJustText()
        p3leftText.showJustText()
        p3rightText.showJustText()
        p4Text.showJustText()
        p4upText.showJustText()
        p4downText.showJustText()
        p4leftText.showJustText()
        p4rightText.showJustText()
        bigText.showJustText()
        endText.showJustText()
        Next.checkClicked()
        finish.checkClicked()
        pygame.display.flip()

def createPlayers():
    global p1
    global colour1
    global player1
    player1=snake([[0,23],[0,24],[0,25]],20,20,colour1,3,"up",p1[0][0],p1[0][1],p1[0][2],p1[0][3],0)
    global p2
    global colour2
    global player2
    player2=snake([[47,2],[47,1],[47,0]],20,20,colour2,3,"down",p2[0][0],p2[0][1],p2[0][2],p2[0][3],0)
    if numPlayers >= 3:
        global p3
        global colour3
        global player3
        player3=snake([[2,0],[1,0],[0,0]],20,20,colour3,3,"right",p3[0][0],p3[0][1],p3[0][2],p3[0][3],0)
    if numPlayers == 4:
        global p4
        global colour4
        global player4
        player4=snake([[45,25],[46,25],[47,25]],20,20,colour4,3,"left",p4[0][0],p4[0][1],p4[0][2],p4[0][3],0)

def resetPlayers():
    global p1
    global colour1
    global player1
    player1=snake([[0,23],[0,24],[0,25]],20,20,colour1,3,"up",p1[0][0],p1[0][1],p1[0][2],p1[0][3],player1.score)
    global p2
    global colour2
    global player2
    player2=snake([[47,2],[47,1],[47,0]],20,20,colour2,3,"down",p2[0][0],p2[0][1],p2[0][2],p2[0][3],player2.score)
    if numPlayers >= 3:
        global p3
        global colour3
        global player3
        player3=snake([[2,0],[1,0],[0,0]],20,20,colour3,3,"right",p3[0][0],p3[0][1],p3[0][2],p3[0][3],player3.score)
    if numPlayers == 4:
        global p4
        global colour4
        global player4
        player4=snake([[45,25],[46,25],[47,25]],20,20,colour4,3,"left",p4[0][0],p4[0][1],p4[0][2],p4[0][3],player4.score)
    multiPlayer()

def multiPlayer():
    eaten=False
    leave=False
    global colour1
    global colour2
    global colour3
    global colour4
    timer=0
    global winner
    winner=0
    Food=food(random.randint(0,47),random.randint(0,25),purple)
    allPos=["-","-","-","-"]
    stop=button("Pause",38,myFont,white,850,523,130,50,black,purple,pause)
    global alive
    alive=0
    p1score=newText("Player 1 Score: 0",19,myFont,colour1,0,523)
    p2score=newText("Player 2 Score: 0",19,myFont,colour2,200,523)
    if numPlayers >= 3:
        p3score=newText("Player 3 Score: 0",19,myFont,colour3,400,523)
    if numPlayers == 4:
        p4score=newText("Player 4 Score: 0",19,myFont,colour4,600,523)
    global p1wins
    global p2wins
    global p3wins
    global p4wins
    p1wins=newText("Player 1 Wins: "+str(player1.score),19,myFont,colour1,0,546)
    p2wins=newText("Player 2 Wins: "+str(player2.score),19,myFont,colour2,200,546)
    if numPlayers >= 3:
        p3wins=newText("Player 3 Wins: "+str(player3.score),19,myFont,colour3,400,546)
    if numPlayers == 4:
        p4wins=newText("Player 4 Wins: "+str(player4.score),19,myFont,colour4,600,546)
    global event
    while leave==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if event.type == pygame.KEYDOWN:
                player1.changeDir(event)
                player2.changeDir(event)
                if numPlayers >= 3:
                    player3.changeDir(event)
                if numPlayers == 4:
                    player4.changeDir(event)
                if event.key ==pygame.K_p:
                    paused=True
                    pause()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        for i in range(0,numPlayers):
            for j in range(0,len(allPos[i])):
                if allPos[i][0][0] == Food.x_co and allPos[i][0][1] == Food.y_co:
                    if i == 0:
                        player1.grow()
                    if i == 1:
                        player2.grow()
                    if i == 2:
                        player3.grow()
                    if i == 3:
                        player4.grow()
                    eaten=True
                    break
        Food.createFood()
        if eaten == True:
            Food.spawn()
            eaten = False
        for i in range(0,numPlayers):
            for j in range(0,len(allPos[i])):
                if allPos[i][j][0] == Food.x_co and allPos[i][j][1] == Food.y_co:
                    Food.spawn()
        stop.checkClicked()
        p1score.addText()
        p1wins.addText()
        p1score.text="Player 1 Score: "+str(player1.length-3)
        p2score.addText()
        p2wins.addText()
        p2score.text="Player 2 Score: "+str(player2.length-3)
        if numPlayers >= 3:
            p3score.addText()
            p3wins.addText()
            p3score.text="Player 3 Score: "+str(player3.length-3)
        if numPlayers == 4:
            p4score.addText()
            p4wins.addText()
            p4score.text="Player 4 Score: "+str(player4.length-3)
        if player1.dead == False:
            player1.makeSnake()
            allPos[0]=player1.coordinates
        else:
            player1.coordinates=[[100,100],[101,101]]
            allPos[0]=player1.coordinates
        if player2.dead == False:
            player2.makeSnake()
            allPos[1]=player2.coordinates
        else:
            player2.coordinates=[[100,100],[101,101]]
            allPos[1]=player2.coordinates
        if numPlayers >= 3:
            if player3.dead == False:
                player3.makeSnake()
                allPos[2]=player3.coordinates
            else:
                player3.coordinates=[[100,100],[101,101]]
                allPos[2]=player3.coordinates
        if numPlayers == 4:
            if player4.dead == False:
                player4.makeSnake()
                allPos[3]=player4.coordinates
            else:
                player4.coordinates=[[100,100],[101,101]]
                allPos[3]=player4.coordinates
        pygame.draw.rect(view,white, [0,520,960,3])
        alive=0
        for i in range(0,numPlayers):
            if allPos[i] != [[100,100],[101,101]]:
                alive=alive+1
                winner=i
        if alive <= 1:
            multiPlayerEnd()
        pygame.display.update()
        speed=rate.tick()
        timer=timer+speed
        if timer > 160:
            if player1.dead == False:
                player1.movement()
            if player2.dead == False:
                player2.movement()
            if numPlayers >= 3:
                if player3.dead == False:
                    player3.movement()
            if numPlayers == 4:
                if player4.dead == False:
                    player4.movement()
            timer=0
        for i in range(0,numPlayers):
            for j in range(1,len(allPos[i])):
                if i == 0:
                    if allPos[0][0][0] == allPos[0][j][0] and allPos[0][0][1] == allPos[0][j][1]:
                        player1.dead = True
                if i == 1:
                    if allPos[1][0][0] == allPos[1][j][0] and allPos[1][0][1] == allPos[1][j][1]:
                        player2.dead = True
                if i == 2:
                    if allPos[2][0][0] == allPos[2][j][0] and allPos[2][0][1] == allPos[2][j][1]:
                        player3.dead = True
                if i == 3:
                    if allPos[3][0][0] == allPos[3][j][0] and allPos[3][0][1] == allPos[3][j][1]:
                        player4.dead = True
            for j in range(0,len(allPos[i])):
                if allPos[0][0][0] == allPos[1][0][0] and allPos[0][0][1] == allPos[1][0][1]:
                    player1.dead = True
                    player2.dead = True
                if i == 0:
                    if allPos[0][j][0] == allPos[1][0][0] and allPos[0][j][1] == allPos[1][0][1] and player1.dead == False:
                        player2.dead = True
                        for k in range(0,player2.length):
                            player1.grow()
                if i == 1:
                    if allPos[1][j][0] == allPos[0][0][0] and allPos[1][j][1] == allPos[0][0][1] and player2.dead == False:
                        player1.dead = True
                        for k in range(0,player1.length):
                            player2.grow()
                if numPlayers >= 3:
                    if allPos[0][0][0] == allPos[2][0][0] and allPos[0][0][1] == allPos[2][0][1]:
                        player1.dead = True
                        player3.dead = True
                    if allPos[1][0][0] == allPos[2][0][0] and allPos[1][0][1] == allPos[2][0][1]:
                        player2.dead = True
                        player3.dead = True
                    if i == 2:
                        if allPos[2][j][0] == allPos[0][0][0] and allPos[2][j][1] == allPos[0][0][1] and player3.dead == False:
                            player1.dead = True
                            for k in range(0,player1.length):
                                player3.grow()
                        if allPos[2][j][0] == allPos[1][0][0] and allPos[2][j][1] == allPos[1][0][1] and player3.dead == False:
                            player2.dead = True
                            for k in range(0,player2.length):
                                player3.grow()
                    if i == 0:
                        if allPos[0][j][0] == allPos[2][0][0] and allPos[0][j][1] == allPos[2][0][1] and player1.dead == False:
                            player3.dead = True
                            for k in range(0,player3.length):
                                player1.grow()
                    if i == 1:
                        if allPos[1][j][0] == allPos[2][0][0] and allPos[1][j][1] == allPos[2][0][1] and player2.dead == False:
                            player3.dead = True
                            for k in range(0,player3.length):
                                player2.grow()
                if numPlayers == 4:
                    if allPos[0][0][0] == allPos[3][0][0] and allPos[0][0][1] == allPos[3][0][1]:
                        player1.dead = True
                        player4.dead = True
                    if allPos[1][0][0] == allPos[3][0][0] and allPos[1][0][1] == allPos[3][0][1]:
                        player2.dead = True
                        player4.dead = True
                    if allPos[2][0][0] == allPos[3][0][0] and allPos[2][0][1] == allPos[3][0][1]:
                        player3.dead = True
                        player4.dead = True
                    if i == 3:
                        if allPos[3][j][0] == allPos[0][0][0] and allPos[3][j][1] == allPos[0][0][1] and player4.dead == False:
                            player1.dead = True
                            for k in range(0,player1.length):
                                player4.grow()
                        if allPos[3][j][0] == allPos[1][0][0] and allPos[3][j][1] == allPos[1][0][1] and player4.dead == False:
                            player2.dead = True
                            for k in range(0,player2.length):
                                player4.grow()
                        if allPos[3][j][0] == allPos[2][0][0] and allPos[3][j][1] == allPos[2][0][1] and player4.dead == False:
                            player3.dead = True
                            for k in range(0,player3.length):
                                player4.grow()
                    if i == 0:
                        if allPos[0][j][0] == allPos[3][0][0] and allPos[0][j][1] == allPos[3][0][1] and player1.dead == False:
                            player4.dead = True
                            for k in range(0,player4.length):
                                player1.grow()
                    if i == 1:
                        if allPos[1][j][0] == allPos[3][0][0] and allPos[1][j][1] == allPos[3][0][1] and player2.dead == False:
                            player4.dead = True
                            for k in range(0,player4.length):
                                player2.grow()
                    if i == 2:
                        if allPos[2][j][0] == allPos[3][0][0] and allPos[2][j][1] == allPos[3][0][1] and player3.dead == False:
                            player4.dead = True
                            for k in range(0,player4.length):
                                player3.grow()
        for i in range(0,numPlayers):
            if allPos[i][0][0] >= 48 or allPos[i][0][0] < 0:
                if i == 0:
                    player1.dead = True
                elif i == 1:
                    player2.dead = True
                elif i == 2:
                    player3.dead = True
                elif i == 3:
                    player4.dead = True
            if allPos[i][0][1] >= 26 or allPos[i][0][1] < 0:
                if i == 0:
                    player1.dead = True
                elif i == 1:
                    player2.dead = True
                elif i == 2:
                    player3.dead = True
                elif i == 3:
                    player4.dead = True
        rate.tick(5000)

def multiPlayerEnd():
    global winner
    global alive
    over=True
    tie=newText("It's a Tie",60,myFont,green,480,260)
    win=newText("",60,myFont,green,480,260)
    cont=button("-Play again",38 ,myFont,white,400,350,195,50,black,green,resetPlayers)
    menu=button("-Main menu",38,myFont,white,400,400,190,50,black,blue,mainMenu)
    end=button("-Quit",38,myFont,white,400,450,90,50,black,red,quitGame)
    if alive == 1:
        pygame.mixer.Sound.play(gameWin)
        if winner == 0:
            win.text="Player 1 Wins"
            player1.score=player1.score+1
            p1wins.text="Player 1 Wins: "+str(player1.score)
        if winner == 1:
            win.text="Player 2 Wins"
            player2.score=player2.score+1
            p2wins.text="Player 2 Wins: "+str(player2.score)
        if winner == 2:
            win.text="Player 3 Wins"
            player3.score=player3.score+1
            p3wins.text="Player 3 Wins: "+str(player3.score)
        if winner == 3:
            win.text="Player 4 Wins"
            player4.score=player4.score+1
            p4wins.text="Player 4 Wins: "+str(player4.score)
    else:
        pygame.mixer.Sound.play(loss)
    global event
    while over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        if alive == 1:
            win.showJustText()
        if alive == 0:
            tie.showJustText()
        cont.checkClicked()
        menu.checkClicked()
        end.checkClicked()
        pygame.display.flip()

def highScoreBoard():
    global afk
    afk=True
    global event
    x=80
    numScores=0
    allScores=[[],[]]
    c.execute("SELECT * FROM highScores ORDER BY score DESC")
    score=c.fetchall()
    for i in range(0,len(score)):
        if score[i][0] not in allScores[0]:
            allScores[0].append(score[i][0])
            allScores[1].append(score[i][1])
    finish=button("Back",35,myFont,white,0,0,90,45,black,blue,back)
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        if len(allScores[0]) > 19:
            numScores=20
        else:
            numScores=len(allScores[0])
        for i in range(0,numScores):
            if i > 9:
                x=560
                y=i*54+20-540
            else:
                x=100
                y=i*54+20
            font=pygame.font.Font(myFont,35)
            text=font.render((str(i+1)+". Score: "+str(allScores[1][i])+" by "+allScores[0][i]),False,green)
            view.blit(text,(x,y))
        finish.checkClicked()
        pygame.display.flip()

def option():
    global afk
    afk=True
    global account
    global colourz
    c.execute("SELECT p1colour, p2colour, p3colour, p4colour FROM accounts WHERE username=?",
              (account,))
    colourz=c.fetchall()
    finish=button("Back",35,myFont,white,0,0,90,45,black,blue,back)
    col=button("Colour",38,myFont,black,220,345,105,50,white,yellow,changeColour)
    con=button("Controls",38,myFont,black,600,345,135,50,white,purple,changeControls)
    heading=newText("What would you like to change?",60,myFont,green,480,150)
    global event
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        finish.checkClicked()
        col.checkClicked()
        con.checkClicked()
        heading.showJustText()
        if afk==False:
            break
        pygame.display.flip()

def changeColour():
    global account
    global event
    global colourz
    finish=button("Back",38,myFont,white,0,520,100,50,black,green,option)
    heading=newText("Which snake's colour would you like to change?",45,myFont,green,480,150)
    p1col=button("Player 1",30,myFont,white,103,300,105,45,black,colours[colourz[0][0]],p1colu)
    p2col=button("Player 2",30,myFont,white,311,300,115,45,black,colours[colourz[0][1]],p2colu)
    p3col=button("Player 3",30,myFont,white,529,300,110,45,black,colours[colourz[0][2]],p3colu)
    p4col=button("Player 4",30,myFont,white,742,300,115,45,black,colours[colourz[0][3]],p4colu)
    over=True
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        p1col.checkClicked()
        p2col.checkClicked()
        p3col.checkClicked()
        p4col.checkClicked()
        finish.checkClicked()
        heading.showJustText()
        if afk==False:
            break
        pygame.display.flip()

def changeControls():
    global account
    global event
    global colourz
    finish=button("Back",38,myFont,white,0,520,100,50,black,green,option)
    heading=newText("Which snake's controls would you like to change?",45,myFont,green,480,150)
    p1con=button("Player 1",30,myFont,white,103,300,105,45,black,colours[colourz[0][0]],p1cont)
    p2con=button("Player 2",30,myFont,white,311,300,115,45,black,colours[colourz[0][1]],p2cont)
    p3con=button("Player 3",30,myFont,white,529,300,110,45,black,colours[colourz[0][2]],p3cont)
    p4con=button("Player 4",30,myFont,white,742,300,115,45,black,colours[colourz[0][3]],p4cont)
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        finish.checkClicked()
        p1con.checkClicked()
        p2con.checkClicked()
        p3con.checkClicked()
        p4con.checkClicked()
        heading.showJustText()
        if afk==False:
            break
        pygame.display.flip()

def p1cont():
    global player
    player=1
    pcontrols()
def p2cont():
    global player
    player=2
    pcontrols()
def p3cont():
    global player
    player=3
    pcontrols()
def p4cont():
    global player
    player=4
    pcontrols()
    
def pcontrols():
    global account
    global colourz
    global player
    finish=button("Back",35,myFont,white,0,0,90,45,black,blue,changeControls)
    menu=button("Main Menu",38,myFont,white,0,523,180,50,black,green,back)
    chooseControl=newText("Click control you want to bind",45,myFont,green,480,70)
    changeControl=newText("Press the button you want to use",45,myFont,green,480,70)
    upBox=textBox("",50,None,black,355,200,250,35,Lgrey,white)
    downBox=textBox("",50,None,black,355,270,250,35,Lgrey,white)
    leftBox=textBox("",50,None,black,355,340,250,35,Lgrey,white)
    rightBox=textBox("",50,None,black,355,410,250,35,Lgrey,white)
    upCon=newText("Up:",30,myFont,colours[colourz[0][player-1]],305,200)
    downCon=newText("Down:",30,myFont,colours[colourz[0][player-1]],275,270)
    leftCon=newText("Left:",30,myFont,colours[colourz[0][player-1]],280,340)
    rightCon=newText("Right:",30,myFont,colours[colourz[0][player-1]],270,410)
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if upBox.place == True:
                    upBox.text=keyName(event.key)
                    upBox.click()
                    pygame.display.flip()
                    c.execute("UPDATE accounts SET ("+"p"+str(player)+"up"+") = ? WHERE username=?",
                              (event.key,account,))
                    con.commit()
                elif downBox.place == True:
                    downBox.text=keyName(event.key)
                    downBox.click()
                    pygame.display.flip()
                    c.execute("UPDATE accounts SET ("+"p"+str(player)+"down"+") = ? WHERE username=?",
                              (event.key,account,))
                    con.commit()
                elif leftBox.place == True:
                    leftBox.text=keyName(event.key)
                    leftBox.click()
                    pygame.display.flip()
                    c.execute("UPDATE accounts SET ("+"p"+str(player)+"left"+") = ? WHERE username=?",
                              (event.key,account,))
                    con.commit()
                elif rightBox.place == True:
                    rightBox.text=keyName(event.key)
                    rightBox.click()
                    pygame.display.flip()
                    c.execute("UPDATE accounts SET ("+"p"+str(player)+"right"+") = ? WHERE username=?",
                              (event.key,account,))
                    con.commit()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        c.execute("SELECT (%s),(%s),(%s),(%s) FROM accounts WHERE username=?"
                  %("p"+str(player)+"up","p"+str(player)+"down","p"+str(player)+"left","p"+str(player)+"right"),
                  (account,))
        playerCont=c.fetchall()
        upBox.text=keyName(playerCont[0][0])
        downBox.text=keyName(playerCont[0][1])
        leftBox.text=keyName(playerCont[0][2])
        rightBox.text=keyName(playerCont[0][3])
        view.fill(black)
        finish.checkClicked()
        menu.checkClicked()
        if upBox.place == True or downBox.place == True or leftBox.place == True or rightBox.place == True:
            changeControl.showJustText()
        else:
            chooseControl.showJustText()
        upCon.addText()
        downCon.addText()
        leftCon.addText()
        rightCon.addText()
        upBox.click()
        downBox.click()
        leftBox.click()
        rightBox.click()
        if afk==False:
            break
        pygame.display.flip()

def p1colu():
    global player
    player=1
    pcolour()
def p2colu():
    global player
    player=2
    pcolour()
def p3colu():
    global player
    player=3
    pcolour()
def p4colu():
    global player
    player=4
    pcolour()

def pcolour():
    global afk
    global account
    global colourz
    global player
    global currentCol
    global blueb
    global greenb
    global yellowb
    global pinkb
    global purpleb
    global orangeb
    global whiteb
    global menu
    finish=button("Back",35,myFont,white,0,0,90,45,black,blue,changeColour)
    chooseColour=newText("Pick a colour",45,myFont,white,480,50)
    currentCol=button("Current Colour",35,myFont,black,0,80,225,45,colours[colourz[0][player-1]],colours[colourz[0][player-1]],None)
    redb=button("",30,myFont,black,260,200,200,50,red,red,pred)
    blueb=button("",30,myFont,black,500,320,200,50,blue,blue,pblue)
    greenb=button("",30,myFont,black,260,380,200,50,green,green,pgreen)
    yellowb=button("",30,myFont,black,260,320,200,50,yellow,yellow,pyellow)
    pinkb=button("",30,myFont,black,500,200,200,50,pink,pink,ppink)
    purpleb=button("",30,myFont,black,500,260,200,50,purple,purple,ppurple)
    orangeb=button("",30,myFont,black,260,260,200,50,orange,orange,porange)
    whiteb=button("",30,myFont,black,500,380,200,50,white,white,pwhite)
    menu=button("Main Menu",38,myFont,white,0,523,180,50,black,green,back)
    afk=True
    while afk==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        global mouse
        global click
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        view.fill(black)
        c.execute("SELECT p1colour, p2colour, p3colour, p4colour FROM accounts WHERE username=?",
              (account,))
        colourz=c.fetchall()
        currentCol.newColour=colours[colourz[0][player-1]]
        currentCol.bColour=colours[colourz[0][player-1]]
        chooseColour.showJustText()
        finish.checkClicked()
        currentCol.checkClicked()
        redb.checkClicked()
        blueb.checkClicked()
        greenb.checkClicked()
        yellowb.checkClicked()
        pinkb.checkClicked()
        purpleb.checkClicked()
        orangeb.checkClicked()
        whiteb.checkClicked()
        menu.checkClicked()
        if afk==False:
            break
        pygame.display.flip()

def pred():
    currentCol.newColour=red
    currentCol.bColour=red
    currentCol.checkClicked()
    blueb.checkClicked()
    greenb.checkClicked()
    yellowb.checkClicked()
    pinkb.checkClicked()
    purpleb.checkClicked()
    orangeb.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'red' WHERE username=?",
              (account,))
    con.commit()
def pblue():
    currentCol.newColour=blue
    currentCol.bColour=blue
    currentCol.checkClicked()
    greenb.checkClicked()
    yellowb.checkClicked()
    pinkb.checkClicked()
    purpleb.checkClicked()
    orangeb.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'blue' WHERE username=?",
              (account,))
    con.commit()
def pgreen():
    currentCol.newColour=green
    currentCol.bColour=green
    currentCol.checkClicked()
    yellowb.checkClicked()
    pinkb.checkClicked()
    purpleb.checkClicked()
    orangeb.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'green' WHERE username=?",
              (account,))
    con.commit()
def pyellow():
    currentCol.newColour=yellow
    currentCol.bColour=yellow
    currentCol.checkClicked()
    pinkb.checkClicked()
    purpleb.checkClicked()
    orangeb.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'yellow' WHERE username=?",
              (account,))
    con.commit()
def ppink():
    currentCol.newColour=pink
    currentCol.bColour=pink
    currentCol.checkClicked()
    purpleb.checkClicked()
    orangeb.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'pink' WHERE username=?",
              (account,))
    con.commit()
def ppurple():
    currentCol.newColour=purple
    currentCol.bColour=purple
    currentCol.checkClicked()
    orangeb.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'purple' WHERE username=?",
              (account,))
    con.commit()
def porange():
    currentCol.newColour=orange
    currentCol.bColour=orange
    currentCol.checkClicked()
    whiteb.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'orange' WHERE username=?",
              (account,))
    con.commit()
def pwhite():
    currentCol.newColour=white
    currentCol.bColour=white
    currentCol.checkClicked()
    menu.checkClicked()
    pygame.display.flip()
    c.execute("UPDATE accounts SET ("+"p"+str(player)+"colour"+") = 'white' WHERE username=?",
              (account,))
    con.commit()
    
intro()
