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
    app.ballX,app.ballY=app.oPlayers[app.playerControlled].x+30,app.oPlayers[app.playerControlled].y+15
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
    player=app.oPlayers[app.playerControlled]
    if event.key=="w":
        player.y-=4
        app.ballY-=4
    elif event.key=="a":
        player.x-=4
        app.ballX-=4
    elif event.key=="s":
        player.y+=4
        app.ballY+=4
    elif event.key=="d":
        player.x+=4
        app.ballX+=4
    elif event.key=="Space":
        shoot(app)
    elif event.key=="f":
        makePass(app,"left")
    elif event.key=="g":
        makePass(app,"up")
    elif event.key=="h":
        makePass(app,"right")
    elif event.key=="v":
        makePass(app,"down")
    elif event.key=="p":
        pauseGame(app)

def shoot(app):
    x,y=app.oPlayers[app.playerControlled].x,app.oPlayers[app.playerControlled].y
    prob=shotProbability(app,x,y)
    samp=random.randint(0,100)/100
    if prob<samp:
        shootBall(app,"miss")
    else:
        shootBall(app,"make")

#minimax algorithm to determine locations of defensive players
#prune nodes that you know will not lead to best outcome to increase efficiency
def moveDefensivePlayers(app):
    oPlayerX,oPlayerY=app.oPlayers[app.playerControlled].x,app.oPlayers[app.playerControlled].y
    for player in app.dPlayers:
        tree=makeDecisionTree(app,4,player)
        defensivePlayerMinimax(tree,4,1,0,player.x,player.y,oPlayerX,oPlayerY,True)

def shootBall(app,result):
    if result=="miss":
        pass
    elif result=="make":
        pass
        app.teamScore+=addPoints(app)

def addPoints(app):
    x,y=app.oPlayers[app.playerControlled].x,app.oPlayers[app.playerControlled].y
    r=app.width/2-(app.xMargin+50)
    playerDist=distance(x,app.ballX,app.ballY,y)
    if playerDist>r:
        return 3
    else:
        return 2

def shotProbability(app,x,y):
    dist=hoopDist(app,x,y)
    playerDist=getNearestDPlayer(app,x,y)
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

def getNearestDirPlayer(app,playerList,x,y,dir):
    oPlayersX=[playerList[i].x for i in range(5)]
    oPlayersY=[playerList[i].y for i in range(5)]
    if dir=="left":
        return getNearestPlayerInDir(app,[x]*5,oPlayersX,[y]*5,oPlayersY)
    elif dir=="right":
        return getNearestPlayerInDir(app,oPlayersX,[x]*5,[y]*5,oPlayersY)
    elif dir=="up":
        return getNearestPlayerInDir(app,[y]*5,oPlayersY,[x]*5,oPlayersX)
    elif dir=="down":
        return getNearestPlayerInDir(app,oPlayersY,[y]*5,[x]*5,oPlayersX) 

def getNearestPlayerInDir(app,L,M,N,O):
    topComponent=0
    nearestPlayer=app.playerControlled
    for i in range(len(L)):
        if distance(L[i],M[i],N[i],O[i])==0:
            continue
        component=(L[i]-M[i])/distance(L[i],M[i],N[i],O[i])
        print(component)
        if component>topComponent:
            topComponent=component
            nearestPlayer=i
    return nearestPlayer

def hoopDist(app,x,y):
    return distance(app.hoopX,x,app.hoopY,y)

def distance(x0,x1,y0,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

def makeDecisionTree(app,depth,dPlayer):
    playerList=copy.copy(app.oPlayers)
    oPlayer=playerList[app.playerControlled]
    x,y=makeDecisionTreeHelper(playerList,depth,{},dPlayer.x,dPlayer.y,oPlayer.x,oPlayer.y)
    app.dPlayerX,app.dPlayerY=x,y

def makeDecisionTreeHelper(playerList,depth,tree,dPlayerX,dPlayerY,oPlayerX,oPlayerY):
    if depth==0:
        for leaf in tree:
            tree["right"]={shotProbability(oPlayerX+5,oPlayerY),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX+5,oPlayerY)}
            tree["left"]={shotProbability(oPlayerX-5,oPlayerY),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX-5,oPlayerY)}
            tree["up"]={shotProbability(oPlayerX,oPlayerY-5),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX,oPlayerY-5)}
            tree["down"]={shotProbability(oPlayerY,oPlayerY+5),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX,oPlayerY+5)}
            ploPlayerX,ploPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"left")
            tree["passleft"]={shotProbability(ploPlayerX,ploPlayerY),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,ploPlayerX,ploPlayerY)}
            proPlayerX,proPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"right")
            tree["passright"]={shotProbability(proPlayerX,proPlayerY),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,proPlayerX,proPlayerY)}
            puoPlayerX,puoPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"up")
            tree["passup"]={shotProbability(puoPlayerX,puoPlayerY),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,puoPlayerX,puoPlayerY)}
            pudPlayerX,pudPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"down")            
            tree["passdown"]={shotProbability(puoPlayerX,puoPlayerY),makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,pudPlayerX,pudPlayerY)}
        return tree
    #oPlayer node
    elif depth%2==1:
        for leaf in tree:
            tree["right"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX+5,oPlayerY)}
            tree["left"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX-5,oPlayerY)}
            tree["up"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX,oPlayerY-5)}
            tree["down"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX,oPlayerY+5)}
            ploPlayerX,ploPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"left")
            tree["passleft"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,ploPlayerX,ploPlayerY)}
            proPlayerX,proPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"right")
            tree["passright"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,proPlayerX,proPlayerY)}
            puoPlayerX,puoPlayerY=getNearestDirPlayer(playerList,oPlayerX,oPlayerY,"up")
            tree["passup"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,puoPlayerX,puoPlayerY)}
    #dPlayer node 
    else:
        for leaf in tree:
            tree["right"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX+5,oPlayerY)}
            tree["left"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX-5,oPlayerY)}
            tree["up"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX,oPlayerY-5)}
            tree["down"]={makeDecisionTreeHelper(depth-1,tree[leaf],dPlayerX,dPlayerY,oPlayerX,oPlayerY+5)}

def defensivePlayerMinimax(tree,depth,alpha,beta,dPLayerX,dPLayerY,oPlayerX,oPlayerY,maximizingPlayer):
    if depth==0:
        return shotProbability(oPlayerX,oPlayerY),tree
    #oPlayer node
    if maximizingPlayer:
        maxEval=0
        for child in tree:
            evaluation=defensivePlayerMinimax(tree[child],depth-1,alpha,beta,dPLayerX,dPLayerY,oPlayerX,oPlayerY,False)[0]
            maxEval=max(maxEval,evaluation)
            alpha=max(alpha,evaluation)
            if beta<=alpha:
                break
        return maxEval,tree
    #dPlayer node
    else:
        minEval=1
        for child in tree:
            evaluation=defensivePlayerMinimax(tree[child],depth-1,alpha,beta,dPLayerX,dPLayerY,oPlayerX,oPlayerY,True)[0]
            minEval=min(minEval,evaluation)
            beta=min(beta,evaluation)
            if beta<=alpha:
                break
        return minEval,tree

def makePass(app,direction):
    x,y=app.oPlayers[app.playerControlled].x,app.oPlayers[app.playerControlled].y
    app.playerControlled=getNearestDirPlayer(app,app.oPlayers,x,y,direction)
    app.ballX,app.ballY=app.oPlayers[app.playerControlled].x+30,app.oPlayers[app.playerControlled].y+15

def pauseGame(app):
    pass

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

#citations:
#images:
    #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.seekpng.com%2Fipng%2Fu2q8t4r5i1r5o0y3_basketball-court-diagram%2F&psig=AOvVaw2anG58zeLOyP4aYNO5ZpE3&ust=1650224700803000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCKi065qsmfcCFQAAAAAdAAAAABAE
    #https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F7%2F72%2FBasketball_Clipart.svg%2F1200px-Basketball_Clipart.svg.png&imgrefurl=https%3A%2F%2Fen.m.wikipedia.org%2Fwiki%2FFile%3ABasketball_Clipart.svg&tbnid=QOhGPRX2HRwPPM&vet=12ahUKEwioq83BrJn3AhUOMM0KHTNqA3oQMygEegUIARCwAQ..i&docid=vnA-OMyRBHFJqM&w=1200&h=1200&q=basketball&ved=2ahUKEwioq83BrJn3AhUOMM0KHTNqA3oQMygEegUIARCwAQ
#resources:
    #https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=MITOpenCourseWare