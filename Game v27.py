import pygame
import random
from easygui import *

#Constants do not change
WIDTH = 540
HEIGHT = 720 #Similar to a mobile screen size
FPS = 60

#define colours
#           R   G   B
GRAY    = (100,100,100)
NAVYBLUE= (60 , 60,100)
WHITE   = (255,255,255)
BRIGHT_GREEN   = (0  ,255,  0)
BLUE    = (0  ,  0,255)
YELLOW  = (255,255,  0)
ORANGE  = (255,182,75)
PURPLE  = (255,0  ,255)
CYAN    = (0  ,255,255)
BLACK   = (0  ,  0,  0)
PINK = (255,192,203)
RED = (200,0,0)
GREEN = (0,200,0)
BRIGHT_RED = (255,0,0)
BG = (222, 235, 247)
FONT = "arial"
Num = random.randrange(1,2) #a random number for the amount of spikes that will spawn up to 2 at a time
HNum= random.randrange(1,3) #random number for harder mode can spawn up to 3 spikes at a time

#load all game graphics

        
class Game:
    #constructor method 
    def __init__(self):
        #initialising pygame and create a window
        pygame.init() 
        pygame.mixer.init()#needed for sound ]
        self.screen =pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dont touch the spikes")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)
        self.score = 0
        self.again = False


    def new(self, mode):
        #start a new game
        self.playerGroup=pygame.sprite.Group() #create group of sprites
        #self.again = False
        self.mobs = pygame.sprite.Group() #new group for the spikes
        self.mode = mode #pass parameters for the difficulty
        if self.mode == "easy": #if easy mode then create group for power ups and create a power up
            self.powerups = pygame.sprite.Group()
            self.pe = Pow()
            self.Nums = Num 
        elif self.mode == "hard": #if hard mode then use the greater range of random numbers
            self.Nums = HNum
        self.spikes = pygame.sprite.Group()#create a group of sprites for the spikes 
        self.bird = Bird() #create a new player object
        self.playerGroup.add(self.bird) #add birds to the group
        self.score = self.bird.score #the score attribute from the bird is the same as the score in the game
        self.m = Mob() #create an instance of the Mob object
        self.count = 0 
        self.mobs.add(self.m) #add the instance to the group
        pos = [0,HEIGHT - 27]#these positions are for the top and bottom spikes
        for count in pos: #there are only 2 positions so this runs twice
            self.w = Walls(count)#creates an instance of the top spikes first then the bottom spikes by passing the y cordinate as a parameter
            self.spikes.add(self.w)
        self.falsehit = False
        self.again = False
        self.newspikes() #function for mob spikes on the left and right
        self.run()
        
    def placepowerup(self):
        self.pe = Pow() #create an instance of power ups
        overlap = pygame.sprite.spritecollide(self.pe, self.mobs, True) #if the power up collides with the spikes then kill the power up
        while overlap: #keep repeating until it does not collide
            self.pe = Pow()
            overlap = pygame.sprite.spritecollide(self.pe, self.mobs, True)
        self.powerups.add(self.pe) #add to group of power ups as there could be more than one power up on the screen
        
    def newspikes(self):
        for i in range(self.Nums):#repeats for the random number that was stored earlier
            self.m = Mob() #an instance of the mob class
            overlap = pygame.sprite.spritecollide(self.m, self.mobs, True) #if it collides with other spikes then kill it
            self.mobs.add(self.m)#add to group of mob spikes
        pygame.display.flip()
        
    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)#keep the loop runnin at the right speed
            self.events()
            if self.mode == "easy": #the game mode changes which way the game updates.
                self.update()
            elif self.mode == "hard":
                self.hardmode()
            self.draw()

    def update(self):
        #Game loop update for easy mode
        falseHit=False #used as a flag for false hit detection
        self.bird.update() #make the bird class run its update method
        self.score = self.bird.score #make the score update as the score from the bird class updates
        if self.bird.refresh: #when the player scores
            #print("score: ",self.score)
            self.newspikes()#create some new spikes
            hit = pygame.sprite.spritecollide(self.bird, self.mobs, False, pygame.sprite.collide_circle) or pygame.sprite.spritecollide(self.bird, self.spikes, False)
            #detects for collisions are returns a boolean expresssion
            if hit: #if there is a collision at the point where the score changes
                falseHit = True #this is considered a false hit because the new spike spawning has collided with the bird
            chance = random.random() #a random float between 0 and 1
            if chance > 0.65: #a 35% chance 
                self.placepowerup()#place power ups
                #print("x,y speed: ",self.bird.speedx, self.bird.speedy)
        boost = pygame.sprite.spritecollide(self.bird, self.powerups, True) #if the bird collides with a power up
        if boost:
            if self.pe.action == "doublescore": #check the action of the power up
                self.bird.score = self.bird.score*2#doubles the score if the double score power up is picked up
            elif self.pe.action == "speedup": #if it picks up a speed up power up
                self.bird.acc = 1.5 #the value of acceleration is 1.5 which will multiiply the speed.
                if self.count < 4: #only for 4 counts
                    self.count = self.count + 1 
                if self.count >= 4:
                    self.bird.acc = 1#after that it will reset the acceleration to 1 so it is normal speed
                    self.count = 0#count goes back to 0
                    boost = False
        if falseHit == False: #while not false hits
            hit = pygame.sprite.spritecollide(self.bird, self.mobs, False, pygame.sprite.collide_circle) or pygame.sprite.spritecollide(self.bird, self.spikes, False) 
            if hit:
               
                self.show_go_screen()#if a collision is detected then show the game over screen



    def hardmode(self): #Update for hard mode just detects collisions between mobs and spikes and updates scores using code from update()
        falseHit=False 
        #Game loop update
        self.bird.update()
        self.score = self.bird.score
        self.bird.acc = 1.25
        if self.bird.refresh:
            #print("score: ",self.score)
            self.newspikes()
            hit = pygame.sprite.spritecollide(self.bird, self.mobs, False, pygame.sprite.collide_circle) or pygame.sprite.spritecollide(self.bird, self.spikes, False)
            if hit:
                falseHit=True
        if falseHit == False:
            hit = pygame.sprite.spritecollide(self.bird, self.mobs, False, pygame.sprite.collide_circle) or pygame.sprite.spritecollide(self.bird, self.spikes, False) 
            if hit:
                
                self.show_go_screen()


    def events(self):
        #Game loop events
        for event in pygame.event.get():
            #check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False#game loop will end
##        if self.again:
##            self.show_start_screen()
            #pygame.display.update()#
        #he game will always be chedcking for this

    def draw(self):
        #Game loop draw
        self.screen.fill(BG)#fill the screen with the background colour
        #draws everything to the screen
        self.playerGroup.draw(self.screen)
        if self.mode == "easy": #only displays power ups if the game mode is the easy mode.
            self.powerups.draw(self.screen)
        self.spikes.draw(self.screen)
        self.mobs.draw(self.screen)
        self.draw_text(str(self.score), 150, WHITE, WIDTH/2, HEIGHT/2)
        pygame.display.flip() #always do this after drawing everything

    def show_start_screen(self):
 
        #game start screen
        intro = True
        while intro: #while loop so that it can look for the position continuously instead of taking the first mouse position  
            for event in pygame.event.get():
                #print(event)
                 if event.type == pygame.QUIT:
                     pygame.quit()
                     quit() #to allow me the user to quit without with the x button
            self.screen.fill(PINK)
            self.draw_text("Don't touch the spikes!", 48, BLUE, WIDTH/2, HEIGHT/4)#The title of the game
            self.draw_text("Space to jump, collect the power ups and avoid the spikes!", 22, BLUE, WIDTH/2, HEIGHT*7/8)#instructions
            self.button("EASY", 195, HEIGHT*3/8,150,50,BRIGHT_GREEN,GREEN,BLACK,25,"level1") #enter parameters into button function
            self.button("HARD", 195, HEIGHT/2, 150,50, BRIGHT_GREEN, GREEN, BLACK, 25,"level2")
            self.button("LEADERBOARD", 195, HEIGHT*5/8, 155,50, BRIGHT_GREEN, GREEN, BLACK, 25,"view")
            self.button("QUIT", 195, HEIGHT*6/8, 150,50, BRIGHT_RED, RED, BLACK, 25, "quit")
            pygame.display.update()#so that the diplay can change 
                

        
    def show_go_screen(self):
        #game over screen
        show = True
        while show: #forces the screen to show otherwise it would disappear in a second.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if not self.running:
                return #if the user presses quit in the middle of the game, they won't see the game over screen
            self.screen.fill(PINK)
            self.draw_text("Game Over", 48, BLUE, WIDTH/2, HEIGHT/4) 
            self.draw_text("Score: "+str(self.score), 22, BLUE, WIDTH/2, HEIGHT*1/3)
            self.button("Menu", 20, (HEIGHT/2),150,50,BRIGHT_GREEN,GREEN,BLACK,25,"menu") #enter parameters into button function
            self.button("SAVE SCORE", 195, HEIGHT/2, 150,50, BRIGHT_GREEN, GREEN, BLACK, 25,"save") #allow user to save their score
            self.button("QUIT", 370, HEIGHT/2, 150,50, BRIGHT_RED, RED, BLACK, 25, "quit")
            pygame.display.update()

    def savescore(self):
        text_file = open("leaderboard.txt","r") #open text file in read mode
        Username = enterbox("Please enter your username as one word: ")#GUI for user input
        while len(Username.split())>1: #force user to enter one word
            Username = enterbox("Please enter your username as one word: ")
        Leaderboard = [] #empty list
        #reading the textfile and saving the leaderboard
        for line in text_file:
                line = list(line.split()) #split the line up so the name and score are seperate indexes
                name = line[0]#the first item in the line was the names
                score = int(line[1]) #save the scores as integers, they were strings in the textfile
                data = [name, score] #create a list for the username and their score
                Leaderboard.append(data) #add that list to create a 2 dimensional list
                
        add = True #flag
        for position in range (len(Leaderboard)):
            if Username == Leaderboard[position][0]: #if the username is already in the leaderboard
                if int(Leaderboard[position][1]) < self.score: #check if the score in the leaderboard is less than the new score
                    msgbox("Your score has been updated") #change the score and let the user know that they are updating an existing score.
                    Leaderboard[position][1] == self.score
                else:
                    msgbox("You didn't beat your high score") #otherwise, they are in the leaderboard but did not beat their high score.
                add = False #if the username is already in the list, it is dealt with here so the flag stops it being added to the Leaderboard again
        text_file.close()#close it so it can be opened in write mode
        text_file = open("leaderboard.txt","w")
        if add: #if the username was not already in the leaderboard
            #adds the new score to the list
            data = [Username, self.score] 
            Leaderboard.append(data)
            #print(Leaderboard)
        #order the list
        Leaderboard.sort(key = lambda x: x[1], reverse = True) #sort the list in reverse order( highest score to lowest score )
        #print(Leaderboard)
        #cut it to 10 scores only if the list was full
        #print(len(Leaderboard))
        if len(Leaderboard) > 10:
            Leaderboard.pop(len(Leaderboard)-1)
        #saving the score to the text file
        for i in range(0,len(Leaderboard)): #for each item in the list
            name = Leaderboard[i][0] #store them as strings
            score = Leaderboard[i][1]
            score = str(score)
            k = (name+" "+score) #concatenating the data so they are on one line
            text_file.write(k+"\n")#writing to the text file
        text_file.close()
        self.show_start_screen()


    def seeleaders(self): #viewing the leaderboard
        show = True
        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill(PINK)
            text_file = open("leaderboard.txt","r")
            i=1
            self.draw_text("High Scores", 48, BLUE, WIDTH/2, HEIGHT*i/14)
            for line in text_file:
                i = i+1
                line = list(line.split())
                name = line[0]
                score = line[1] #read from the text file
                k = (name+" "+score) #concatenate
                self.draw_text(k, 30, BLUE, WIDTH/2, HEIGHT*i/14) #
            text_file.close()
            self.button("Menu", 195, (HEIGHT-100),150,50,BRIGHT_GREEN,GREEN,BLACK,25,"menu")
            pygame.display.update()
        

        

    def draw_text(self,text,size,colour,x,y):
        #function for displaying text on the screen
        font = pygame.font.Font(self.font_name, size) 
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)

    def button(self,msg,x,y,w,h,light,dark,textcolour,textsize, action = None):
        mouse = pygame.mouse.get_pos()#stores the position of the mouse
        click = pygame.mouse.get_pressed() #stores the position of the clicks
        if x+w > mouse[0] > x and y+h >mouse[1] > y: #if the mouse hovers over the button
            pygame.draw.rect(self.screen, light, (x,y,w,h)) #display the brighter coloured button
            #print("click is",click)
            if click[0] == 1 and action != None: #if mouse is clicked and there is an action
                print(action)
                if action == "level1":
                    self.new("easy") #new game
                if action == "level2":
                    self.new("hard")
                if action == "save":
                    self.savescore()
                if action == "view":
                    self.seeleaders()
                    #print("not yet")
                if action == "menu":
                    print("menu from show screen")
                    #self.again = True
                    self.show_start_screen()
                    #print("menu from show screen")
                if action == "quit":
                    pygame.quit() #end game
                    quit()
                
        else:
            pygame.draw.rect(self.screen, dark, (x,y,w,h)) #when it is not hovering it will display the button in a dark colour
        self.draw_text(msg,textsize,textcolour,x + (w/2),y+(h/2))


class Bird(pygame.sprite.Sprite): #Define class for the bird (sprite for player)

    def __init__(self):
        self.score = 0
        pygame.sprite.Sprite.__init__(self)#required line 
        self.image = pygame.image.load('R1.png')#what the sprite looks like
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center =(WIDTH/2, HEIGHT/2)#set where the player starts
        self.speedx = 3 #set the speed of the bird
        self.speedy = 0
        self.acc = 1
        self.left = False #flags for the direction that the bird is moving
        self.right = False
        #Lists of the images that need to be loaded
        self.walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png')]
        self.walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png')]
        self.walkcount = 0
    
    def update(self):
        self.speedy = 2*self.acc #multiply the speed by the acceleration, so if the acceleration changes it will speed up or slow down accordingly
        self.rect.x += self.speedx #move the bird at the rate of the speed
        self.refresh = False 
        if self.rect.right >= WIDTH: #change direction
            self.speedx = -3*self.acc 
            self.right = False
            self.left = True #facing left so the animation is like its bouncing in the other direction
            self.score += 1 #score increases by one
            self.refresh = True #this will affect the game update loop
            
        elif self.rect.left <= 0:
            self.speedx = 3*self.acc
            self.right = True
            self.left = False
            self.score += 1
            self.refresh = True
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT #stop it going below or above the screen
        if self.rect.top < 0:
            self.rect.top = 0
        
        keystate = pygame.key.get_pressed() #check for keys pressed
        if keystate[pygame.K_SPACE]:#spacebar used to jump
            self.speedy = -4*self.acc #jump
            if self.speedx == 3*self.acc:
                self.right = True
                self.left = False #keep facing the right direction when the user presses jump
            elif self.speedx == -3*self.acc: 
                self.right = False
                self.left = True 
        self.rect.y += self.speedy #otherwise constantly falling

        if self.walkcount + 1>= 48: #to make each frame be 6 seconds 6*8(items in the list) = 48
            self.walkcount = 0 #make it loop through the list again
        if self.left: #if facing left
            self.image = self.walkLeft[self.walkcount//6] #iterate through the list facing left
            self.walkcount += 1
        elif self.right:
            self.image = self.walkRight[self.walkcount//6]
            self.walkcount += 1
        else:
            self.image = pygame.image.load('R1.png')
        
        



        

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#required
        self.image = pygame.image.load('spikes.png')#what the sprite looks like
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.8 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.choice([0, WIDTH - self.rect.width])
        self.rect.y = random.randrange(60,HEIGHT-60)
        #if statement here for left and right spikes
        if self.rect.x == (WIDTH - self.rect.width):
            self.image = pygame.image.load('spikes_right.png')

class Walls(pygame.sprite.Sprite): #class for the walls on the top and bottom
    def __init__(self,yposition): #takes y position as a parameter
        pygame.sprite.Sprite.__init__(self)#required
        self.image = pygame.image.load('topspike.png')#what the sprite looks like
        self.rect = self.image.get_rect()        
        self.rect.x = 0
        self.rect.y = yposition
        if self.rect.y == HEIGHT - self.rect.height:
            self.image = pygame.image.load("bottomspike.png") #different spikes for the top and bottom

class Pow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#required
        self.name = random.choice(["speed up", "double score"]) #random power up
        #self.name = random.choice(["speed up"])
        if self.name == "speed up": 
            self.image = pygame.image.load("Speed.png") #load picture for the chosen power up
            self.rect = self.image.get_rect() 
            self.action = "speedup"
        elif self.name == "double score":
            self.image = pygame.image.load("Double_score.png")
            self.rect = self.image.get_rect()
            self.action = "doublescore"
##        elif self.name == "disappearing spikes":
##            self.image = pygame.image.load("disappearing.png")
##            self.rect = self.image.get_rect()
##            self.action = "nospikes"
        self.rect.x = random.choice([10, WIDTH - self.rect.width-10])
        self.rect.y = random.randrange(60, HEIGHT-60)

    
    


game = Game() #create an instance of the game class
game.show_start_screen()
##while game.
##if game.again:
##    game.show_start_screen()
##    pygame.display.update()
##    print("out side")

pygame.quit()
