from cmu_112_graphics import *
import math, copy, random

def appStarted(app):
    app.mode="gameMode"
    app.timerDelay=50
    app.courtImage=app.loadImage("court.gif")
    app.courtImage2=app.courtImage.transpose(Image.FLIP_TOP_BOTTOM)
    app.courtx0,app.courty0,app.courtx1,app.courty1=(159,37,663,490)
    app.courtImage3=app.courtImage2.crop((app.courtx0,app.courty0,app.courtx1,app.courty1))
    app.xMargin,app.yMargin=(app.width-(app.courtx1-app.courtx0))/2,(app.height-(app.courty1-app.courty0))/2
    app.teamScore=app.oppScore=0
    app.ballImage=app.loadImage("basketball-modified.gif")
    app.ballImage2=app.scaleImage(app.ballImage,0.1)
    app.timeCount=0
    app.hoopX,app.hoopY=app.width/2,app.yMargin+45
    app.playerControlled=3
    app.oPlayers=initializeOPlayers(app,"blue")
    app.dPlayers=initializeDPlayers(app,"green")
    app.ballX,app.ballY=app.oPlayers[3].x+30,app.oPlayers[3].y+15
    app.shotClock=24
    app.userTeam="Home"

class Player:
    def __init__(self,x,y,color):
        self.x,self.y,self.color=x,y,color
    
class Offensive(Player):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        self.points=0
        self.assists=0
    def pointsScored(self,points):
        self.points+=points
    def assistMade(self):
        self.assists+=1

def initializeOPlayers(app,color):
    p0=Offensive(app.xMargin+20,app.yMargin+15,color)
    p1=Offensive(app.width-app.xMargin-20,app.yMargin+15,color)
    p2=Offensive((app.width)/2,app.yMargin+15,color)
    p3=Offensive((app.width)/2-50,(app.height)/2+30,color)
    p4=Offensive((app.width)/2+50,(app.height)/2+30,color)
    return [p0,p1,p2,p3,p4]

def initializeDPlayers(app,color):
    p5=Player(app.xMargin+40,app.yMargin+15,color)
    p6=Player(app.width-app.xMargin-40,app.yMargin+15,color)
    p7=Player((app.width)/2+20,app.yMargin+15,color)
    p8=Player((app.width)/2-50,(app.height)/2+10,color)
    p9=Player((app.width)/2+50,(app.height)/2+10,color)
    return [p5,p6,p7,p8,p9]

def gameMode_timerFired(app):
    app.timeCount+=1
    if app.timeCount%20==0:
        app.shotClock-=1
    if app.shotClock==0:
        shotClockViolation(app) #reset app.shotClock to 24

def shotClockViolation(app):
    pass

def gameMode_keyPressed(app,event):
    if event.key=="Space":
        shoot(app)
    elif event.key=="a":
        makePass(app,"left")
    elif event.key=="w":
        makePass(app,"up")
    elif event.key=="d":
        makePass(app,"right")
    elif event.key=="p":
        pauseGame(app)

def shoot(app):
    prob=getShotProbability(app,app.playerControlled)
    samp=random.randint(0,100)/100
    if prob<samp:
        shootBall(app,"miss")
    else:
        shootBall(app,"make")

#minimax algorithm to determine locations of defensive players
#prune nodes that you know will not lead to best outcome to increase efficiency
def moveDefensivePlayers(app):
    pass

def shootBall(app,result):
    if result=="miss":
        pass
    elif result=="make":
        pass

def getShotProbability(player):
    x,y=player.x,player.y
    dist=hoopDist(x,y)
    playerDist=getNearestDPlayer(x,y)
    optimality=(playerDist-dist)/100
    return (3*math.e**(-3*optimality))

def getNearestDPlayer(app,x,y):
    nearestDist=distance(x,app.dPlayers[0].x,y,app.dPlayers[0].y)
    nearestPlayer=0
    for player in range(len(app.dPlayers)):
        deX,deY=app.dPlayers[player].x,app.dPlayers[player].y
        dist=distance(x,deX,y,deY)
        if dist<nearestDist:
            nearestDist=dist
            nearestPlayer=player
    return nearestPlayer

def getNearestDirPlayer(app,x,y,dir):
    oPlayersX=[app.oPlayers[i].x for i in range(5)]
    oPlayersY=[app.oPlayers[i].y for i in range(5)]
    if dir=="left":
        return getNearestPlayerInDir([x]*5,oPlayersX,[y]*5,oPlayersY)
    elif dir=="right":
        return getNearestPlayerInDir(oPlayersX,[x]*5,[y]*5,oPlayersY)
    elif dir=="up":
        return getNearestPlayerInDir([y]*5,oPlayersY,[x]*5,oPlayersX)

def getNearestPlayerInDir(L,M,N,O):
    topComponent=(L[0]-M[0])/distance(L[0],M[0],N[0],O[0])
    nearestPlayer=0
    for i in range(len(L)):
        component=(L[i]-M[i])/distance(L[i],M[i],N[i],O[i])
        if component>topComponent and component>0:
            topComponent=component
            nearestPlayer=i
    return nearestPlayer

def hoopDist(app,x,y):
    return distance(app.x,x,app.y,y)

def distance(x0,x1,y0,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

def makePass(app,direction):
    pass

def pauseGame(app):
    pass

def gameMode_mousePressed(app,event):
    pass

def gameMode_mouseDragged(app,event):
    player=app.oPlayers[app.playerControlled]
    player.x=.9*player.x+.1*event.x
    player.y=.9*player.y+.1*event.y
    app.ballX=player.x+30
    app.ballY=player.y+15

def drawCourt(app,canvas):
    canvas.create_image((app.width)/2,(app.height)/2,image=ImageTk.PhotoImage(app.courtImage3))

def drawShotClock(app,canvas):
    canvas.create_rectangle(app.width/2-21,app.yMargin-60,app.width/2+21,app.yMargin-20,fill="black")
    canvas.create_text(app.width/2+22,app.yMargin-60,text=f"{app.shotClock}",anchor="ne",fill="red",font="Arial 28")

def drawScoreboard(app,canvas):
    canvas.create_rectangle(3*app.width/5,app.yMargin-60,4*app.width/5,app.yMargin-20)
    canvas.create_rectangle(3*app.width/5,app.yMargin-60,7*app.width/10,app.yMargin-20)
    canvas.create_rectangle(7*app.width/10,app.yMargin-60,4*app.width/5,app.yMargin-20)
    canvas.create_text(13*app.width/20,app.yMargin-60,text=app.userTeam,anchor="n",font="Arial 12")
    canvas.create_text(15*app.width/20,app.yMargin-60,text="Away",anchor="n",font="Arial 12")
    canvas.create_text(13*app.width/20,app.yMargin-40,text=app.teamScore,anchor="n",font="Arial 12")
    canvas.create_text(15*app.width/20,app.yMargin-40,text=app.oppScore,anchor="n",font="Arial 12")

def drawBall(app,canvas):
    canvas.create_image(app.ballX,app.ballY,image=ImageTk.PhotoImage(app.ballImage2))

def drawPlayers(app,canvas):
    for player in app.dPlayers+app.oPlayers:
        x,y,color=player.x,player.y,player.color
        #body
        canvas.create_rectangle(x-10,y-10,x+10,y+10,fill=color)
        #arms
        canvas.create_rectangle(x+10,y-2,x+20,y-4,fill="black")
        canvas.create_rectangle(x-20,y-2,x-10,y-4,fill="black")
        #legs
        canvas.create_rectangle(x-10,y+10,x-5,y+20,fill="black")
        canvas.create_rectangle(x+5,y+10,x+10,y+20,fill="black")
        #head
        canvas.create_oval(x-10,y-25,x+10,y-10,fill="black")

def gameMode_redrawAll(app,canvas):
    drawCourt(app,canvas) #all static elements
    drawShotClock(app,canvas)
    drawScoreboard(app,canvas)
    drawPlayers(app,canvas)
    drawBall(app,canvas)

runApp(width=600,height=600)