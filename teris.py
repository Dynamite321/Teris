# teris.py
# A module for game teris.
# By programmer FYJ

from Tkinter import *
from time import sleep
from random import *
from tkMessageBox import *


class Teris:
    def __init__(self):
        self.color = ['red','orange','yellow','purple','blue','green','pink']
        # Set a core squre and any shape can be drawn by the relative location.
        self.shapeDict = {1:[(0,0),(0,-1),(0,-2),(0,1)], # shape I
                           2:[(0,0),(0,-1),(1,-1),(1,0)], # shape O
                           3:[(0,0),(-1,0),(0,-1),(1,0)], # shape T
                           4:[(0,0),(0,-1),(1,0),(2,0)], # shape J
                           5:[(0,0),(0,-1),(-1,0),(-2,0)], # shape L
                           6:[(0,0),(0,-1),(-1,-1),(1,0)], # shape Z
                           7:[(0,0),(-1,0),(0,-1),(1,-1)]} # shape S
        # Change the relative location to make the block rotate.
        self.rotateDict = {(0,0):(0,0),(0,1):(-1,0),(0,2):(-2,0),(0,-1):(1,0),
                           (0,-2):(2,0),(1,0):(0,1),(2,0):(0,2),(-1,0):(0,-1),
                           (-2,0):(0,-2),(1,1):(-1,1),(-1,1):(-1,-1),
                           (-1,-1):(1,-1),(1,-1):(1,1)}
        # The location of the core square.
        self.coreLocation = [4,-2]
        self.height,self.width = 20,10
        self.size = 32
        # Map can record the location of every square.
        self.map = {}
        for i in range(self.width):
            for j in range(-4,self.height):
                self.map[(i,j)] = 0
        for i in range(-4,self.width+4):
            self.map[(i,self.height)] = 1
        for j in range(-4,self.height+4):
            for i in range(-4,0):
                self.map[(i,j)] = 1
        for j in range(-4,self.height+4):
            for i in range(self.width,self.width+4):
                self.map[(i,j)] = 1

        # the score gained by players
        self.score = 0
        self.isFaster = False
        # Draw the GUI interface
        self.root = Tk()
        self.root.title("Teris")
        self.root.geometry("500x645")
        self.area = Canvas(self.root,width=320,height=640,bg='white')
        self.area.grid(row=2)
        self.pauseBut = Button(self.root,text="Pause",height=2,width=13,font=(18),command=self.isPause)
        self.pauseBut.place(x=340,y=100)
        self.startBut = Button(self.root,text="Start",height=2,width=13,font=(18),command=self.play)
        self.startBut.place(x=340,y=20)
        self.restartBut = Button(self.root,text="Restart",height=2,width=13,font=(18),command=self.isRestart)
        self.restartBut.place(x=340,y=180)
        self.quitBut = Button(self.root,text="Quit",height=2,width=13,font=(18),command=self.isQuit)
        self.quitBut.place(x=340,y=260)
        self.scoreLabel1 = Label(self.root,text="Score:",font=(24))
        self.scoreLabel1.place(x=340,y=600)
        self.scoreLabel2 = Label(self.root,text="0",fg='red',font=(24))
        self.scoreLabel2.place(x=410,y=600)
        self.area.bind("<Up>",self.rotate)
        self.area.bind("<Left>",self.moveLeft)
        self.area.bind("<Right>",self.moveRight)
        self.area.bind("<Down>",self.moveFaster)
        self.area.bind("<Key-w>",self.rotate)
        self.area.bind("<Key-a>",self.moveLeft)
        self.area.bind("<Key-d>",self.moveRight)
        self.area.bind("<Key-s>",self.moveFaster)
        self.area.focus_set()
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.startMenu = Menu(self.menu)
        self.menu.add_cascade(label='Start',menu=self.startMenu)
        self.startMenu.add_command(label='New Game',command=self.isRestart)
        self.startMenu.add_separator()
        self.startMenu.add_command(label='Continue',command=self.play)
        self.exitMenu = Menu(self.menu)
        self.menu.add_cascade(label='Exit',command=self.isQuit)
        self.helpMenu = Menu(self.root)
        self.menu.add_cascade(label='Help',menu=self.helpMenu)
        self.helpMenu.add_command(label='How to play',command=self.rule)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='About...',command=self.about)

    # get the location in the map of the new square
    def getLocation(self):
        map[(core[0],core[1])] = 1
        for i in range(4):
            map[((core[0]+getNew[i][0]),
                 (core[1]+getNew[i][1]))]=1

    # judge whether the square can move down
    def canMove(self):
        for i in range(4):
            if map[(core[0]+getNew[i][0]),(core[1]+1+getNew[i][1])] == 1:
                return False
        return True

    # draw the new square that can move
    def drawNew(self):
        global next
        global getNew
        global core
        next = randrange(1,8)
        self.getNew = self.shapeDict[next]
        getNew = self.getNew
        core = [4,-2]
        time = 0.2
        while self.canMove():
            if isPause:
                core[1] += 1
                self.drawSquare()
                if self.isFaster:
                    sleep(time-0.15)
                else:
                    sleep(time+0.22)
                self.isFaster = False    
            else:
                self.drawSquare()
                sleep(time)
        self.getLocation()

    # Draw the current square
    def drawSquare(self):
        self.area.delete("new")
        for i in range(4):
            self.area.create_rectangle((core[0]+self.getNew[i][0])*self.size,
                                       (core[1]+self.getNew[i][1])*self.size,
                                       (core[0]+self.getNew[i][0]+1)*self.size,
                                       (core[1]+self.getNew[i][1]+1)*self.size,
                                       fill=self.color[next-1],tags="new")
        self.area.update()
        

    # draw the square reach the bottom
    def drawBottom(self):
        for j in range(self.height):
            self.area.delete('bottom'+str(j))
            for i in range(self.width):
                if map[(i,j)] == 1:
                    self.area.create_rectangle(self.size*i,self.size*j,self.size*(i+1),
                                               self.size*(j+1),fill='grey',tags='bottom'+str(j))        
            self.area.update()
                
    # judge if the if a line is filled by squares
    def isFill(self):
        for j in range(self.height):
            t = 0
            for i in range(self.width):
                if map[(i,j)] == 1:
                    t = t + 1
            if t == self.width:
                self.getScore()
                self.deleteLine(j)

    # when the line is filled, add the score
    def getScore(self):
        scoreValue = eval(self.scoreLabel2['text'])
        scoreValue += 10
        self.scoreLabel2.config(text=str(scoreValue))

    # delete the line when it's filled
    def deleteLine(self,j):
        for t in range(j,2,-1):
            for i in range(self.width):
                map[(i,t)] = map[(i,t-1)]
        for i in range(self.width):
            map[(i,0)] = 0
        self.drawBottom()
                

    # judge if game is over
    def isOver(self):
        t = 0
        for j in range(self.height):
            for i in range(self.width):
                if self.map[(i,j)] == 1:
                    t += 1
                    break
        if t >= self.height:
            return False
        else:
            return True

    # judge if the square can rotate
    def canRotate(self):
        for i in range(4):
            map[((core[0]+getNew[i][0]),
                (core[1]+getNew[i][1]))] = 0
        for i in range(4):
            if map[((core[0]+self.rotateDict[getNew[i]][0]),
                    (core[1]+self.rotateDict[getNew[i]][1]))] == 1:
                return False
        return True

    # when the key 'Up' or 'w' is pressed, rotate the square
    def rotate(self,event):
        if next != 2:
            if self.canRotate():
                for i in range(4):
                    getNew[i] = self.rotateDict[getNew[i]]
                self.drawSquare()        
        if not self.canMove():
            for i in range(4):
                map[((core[0]+getNew[i][0]),(core[1]+getNew[i][1]))] = 1

    # judge if the square can move left
    def canLeft(self):
        coreNow = core
        for i in range(4):
            map[((coreNow[0]+getNew[i][0]),(coreNow[1]+getNew[i][1]))] = 0
        for i in range(4):
            if map[((coreNow[0]+getNew[i][0]-1),(coreNow[1]+getNew[i][1]))] == 1:
                return False
        return True

    # when the key 'Left' or 'a' is pressed, move the square left
    def moveLeft(self,event):
        if self.canLeft():
            core[0] -= 1
            self.drawSquare()
            self.drawBottom()
        if not self.canMove():
            for i in range(4):
                map[((core[0]+getNew[i][0]),(core[1]+getNew[i][1]))] = 1

             
    # judge if the square can move right
    def canRight(self):
        for i in range(4):
            map[((core[0]+getNew[i][0]),(core[1]+getNew[i][1]))] = 0
        for i in range(4):
            if map[((core[0]+getNew[i][0]+1),(core[1]+getNew[i][1]))] == 1:
                return False
        return True

    # when the key 'Right' or 'd' is pressed, move the square Right
    def moveRight(self,event):
        if self.canRight():
            core[0] += 1
            self.drawSquare()
            self.drawBottom()
        if not self.canMove():
            for i in range(4):
                map[((core[0]+getNew[i][0]),(core[1]+getNew[i][1]))] = 1

            
    # when the key 'Down' or 's' is pressed, move the square down fastlier
    def moveFaster(self,event):
        self.isFaster = True
        if not self.canMove():
            for i in range(4):
                map[((core[0]+getNew[i][0]),(core[1]+getNew[i][1]))] = 1
        
    # run the programe
    def run(self):
        self.isFill()
        self.drawNew()
        self.drawBottom()

    # play the game    
    def play(self):
        self.startBut.config(state=DISABLED)
        global isPause
        isPause = True
        global map
        map = self.map
        while True:
            if self.isOver():
                self.run()
            else:
                break
        self.over()    

    # restart the game       
    def restart(self):
        self.core = [4,-2]
        self.map = {}
        for i in range(self.width):
            for j in range(-4,self.height):
                self.map[(i,j)] = 0
        for i in range(-1,self.width):
            self.map[(i,self.height)] = 1
        for j in range(-4,self.height+1):
            self.map[(-1,j)] = 1
            self.map[(self.width,j)] = 1       
        self.score = 0
        self.t = 0.07
        for j in range(self.height):
            self.area.delete('bottom'+str(j))
        self.play()

    # tell the player he/she loses, and ask if he/she want to restart
    def over(self):
        feedback = askquestion("You Lose!","You Lose!\nDo you want to restart?")
        if feedback == 'yes':
            self.restart()
        else:
            self.root.destroy()

    # Quit when the quit button is pressed
    def isQuit(self):
        askQuit = askquestion("Quit","Are you sure to quit?")
        if askQuit == 'yes':
            self.root.destroy()
            exit()

    # Restart the game when the restart button is pressed
    def isRestart(self):
        askRestart = askquestion("Restart","Are you sure to restart?")
        if askRestart == 'yes':
            self.restart()
        else:
            return

    # Stop the game when the pause button is pressed
    def isPause(self):
        global isPause
        isPause=not isPause
        if not isPause:
            self.pauseBut["text"]="Resume"
        else:
            self.pauseBut["text"]="Pause"
        
    # Provide help to player
    def rule(self):
        ruleTop = Toplevel()
        ruleTop.title('Help')
        ruleTop.geometry('800x400')
        rule ="Start: Press the start button or choose the option 'Continue' to start the game.\n%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s"%("Restart: Press the restart button or choose the option 'New Game' to resatrt the game.\n",
                                                                                                                                               "Pause: Press the pause button to make the game stop for now\n",
                                                                                                                                               "Keyboard Operation:\n",
                                                                                                                                               "                   Press the key<'Up'> or <'w'> to rotate the square for 90 degree.\n",
                                                                                                                                               "                   Press the key<'Left'> or <'a'> to make the square move left.\n",
                                                                                                                                               "                   Press the key<'Right'> or <'d'> to make the square move right.\n",
                                                                                                                                               "                   Press the key<'Down'> or <'s'> to make the square move quicklier.\n",
                                                                                                                                               "                                                                                     \n",
                                                                                                                                               "You can change the location or direction of the square to make a line filled by squares.\n",
                                                                                                                                               "If a line is filled, this line will be deleted, and your score will add 1 point.\n",
                                                                                                                                               "When the square reach the top off the game area, game over.\n",
                                                                                                                                               "Then you can choose if you restart the game.\n",
                                                                                                                                               "Try to make your scores higher.\n",
                                                                                                                                               "Enjoy the Teris game! Have fun!")
        ruleLabel = Label(ruleTop,text=rule,fg='blue',font=(18))
        ruleLabel.place(x=50,y=50)

    # Show the information about this game, including progarmmer's information
    def about(self):
        aboutTop = Toplevel()
        aboutTop.title('About')
        aboutTop.geometry('300x150')
        about = "Teris.py\n\
By Programmer FYJ\n\
All Rights Reserved."
        aboutLabel = Label(aboutTop,font=('Curier',20),fg='darkblue',text=about)
        aboutLabel.pack()                

    # Get into mainloop
    def mainloop(self):
        self.root.mainloop()

            
        

        
        

            
        
        
        
                
        
            
                    
                
                


        
                
                

                

            
                                                                      
        
        
        
                
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
