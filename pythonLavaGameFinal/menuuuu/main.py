import numpy
import math
import pygame, sys
from button import Button
import os
import random
SCREEN_WIDTH, SCREEN_HEIGHT = 1438, 674
directorr = os.path.dirname(os.path.realpath(__file__))
print(directorr)
if (('c:' in directorr) or ('d:' in directorr) or ('e:' in directorr) or ('f:' in directorr) or ('g:' in directorr) or ('h:' in directorr) or ('C:' in directorr) or ('D:' in directorr) or ('E:' in directorr) or ('F:' in directorr) or ('G:' in directorr) or ('H:' in directorr)) and '\\' in directorr:
    slash = "\x5c"
else :
    slash='/'


pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #,pygame.FULLSCREEN for the noframe add ,pygame.NOFRAME and for the fullscreen add ,pygame.FULLSCREEN (no need to remove the other values)
pygame.display.set_caption("Still no game title")

BG = pygame.image.load(directorr+slash+"assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(directorr+slash+"assets/font.ttf", size)

def outputtheint(textwithname): #this function and the following one will be used for the scoreboard
    outpoot=''
    for i in textwithname:
        try: outpoot+=str(int(i))
        except: 
            if len(outpoot)==0:
                return int(0)
            else:
                return int(outpoot)

def outputthename(textwithint):
    outpoot=''
    fallsss=False
    for i in textwithint:
        if fallsss:
            outpoot+=i
        if i==' ':
            fallsss=True
    return outpoot

def bestscore():
    records=open(directorr+slash+".."+slash+"bestscores.txt", "r").read().splitlines()
    i=0
    for j in records:
        if outputtheint(j)>i:
            i=outputtheint(j)
    return i

def createanddefine(intega):
    if intega==1:
        filee=open(directorr+slash+".."+slash+"audioconf.txt", "w")
        filee.write("on")
    elif intega==2:
        filee=open(directorr+slash+".."+slash+"audioconf.txt", "w")
        filee.write("off")
    return open(directorr+slash+".."+slash+"audioconf.txt", "r").read()

def checkifnewrecord(recc):
    records=fivebestscores()
    for record in records:
        record1=outputtheint(record)
        if recc>record1:
            return True
    return False



def fivebestscores(): # this function outputs a list of STRINGS
    records=open(directorr+slash+".."+slash+"bestscores.txt", "r").read().splitlines()
    output=[]
    outputints=[]
    for i in range(len(records)):
        if len(output)<5:
            output.append(records[i])
            outputints.append(outputtheint(records[i]))
        else:
            a=True
            while a:
                for j in range(len(output)):
                    a=False
                    if outputtheint(records[i])>outputtheint(output[j]) and (outputtheint(records[i]) not in outputints):
                        output.pop(j)
                        output.append(records[i])
                        outputints.pop(j)
                        outputints.append(outputtheint(records[i]))
                        a=True
                        break
    for i in range(len(records)):   #the "while" loop wasn't replacing the smallest values of the list, only the values where records[i]>output[j], and i am too lazy to write so i just fix it by doing the process twice
        if len(output)<5:
            output.append(records[i])
            outputints.append(outputtheint(records[i]))
        else:
            a=True
            while a:
                for j in range(len(output)):
                    a=False
                    if outputtheint(records[i])>outputtheint(output[j]) and (outputtheint(records[i]) not in outputints):
                        output.pop(j)
                        output.append(records[i])
                        outputints.pop(j)
                        outputints.append(outputtheint(records[i]))
                        a=True
                        break
    trooss=True
    while trooss:
        trooss=False
        for i in range(len(output)-1):
            if outputtheint(output[i+1])>outputtheint(output[i]):
                trooss=True
                willbeinsertedin1=output[i]
                output.pop(i)
                output.append(willbeinsertedin1)
                break
    return output



def saving():
    nextletters=''
    while True:
        global BG
        BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        try: audioconf=open(directorr+slash+".."+slash+"audioconf.txt", "r").read()
        except:audioconf=createanddefine(2)
        state=audioconf
        SCREEN.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()



        

        nametext = get_font(80).render("Name:"+nextletters, True, "Cyan")
        namerect = nametext.get_rect(center=((int(pygame.display.Info().current_w/2)), 360))
        SCREEN.blit(nametext, namerect)

        

        OPTIONS_TEXT = get_font(45).render("New record! Save it!", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((int(pygame.display.Info().current_w/2)), 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(1280, 625), 
                            text_input="SAVE", font=get_font(75), base_color="Green", hovering_color="Yellow")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)


        DONTSAVE = Button(image=None, pos=(230, 625), 
                            text_input="IGNORE", font=get_font(75), base_color="Green", hovering_color="Yellow")
                    
        DONTSAVE.changeColor(OPTIONS_MOUSE_POS)
        DONTSAVE.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    if len(nextletters)==0:
                        return "AnonPlayer"
                    return nextletters
                if DONTSAVE.checkForInput(OPTIONS_MOUSE_POS):
                    return "AnonPlayer"
            if event.type == pygame.KEYDOWN:
                if list(event.dict.values())[1]==8:
                    nextletters=nextletters[:-1]
                elif list(event.dict.values())[1]==13:
                    if len(nextletters)==0:
                        return "AnonPlayer"
                    return nextletters
                else:
                    nextletters+=list(event.dict.values())[0]

        pygame.display.update()


def checkbrickinlist(bricky,listy,gap):
    for bricks in listy:
        if (bricky+gap>bricks) and (bricky-gap<bricks):
            return True
    else:
        return False




def scoreboard():
    while True:
        global BG
        BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        try: audioconf=open(directorr+slash+".."+slash+"audioconf.txt", "r").read()
        except:audioconf=createanddefine(2)
        state=audioconf

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        def quickaddtext(alignn,coords1,size,coords2,score,color):
            text = get_font(size).render(score, True, color)
            recttt = text.get_rect(center=(coords1, coords2))
            recttt.left=alignn
            SCREEN.blit(text, recttt)

        text = get_font(45).render("Here are the 5 best scores!", True, "Cyan")
        recttt = text.get_rect(center=((int(pygame.display.Info().current_w/2)), 50))
        SCREEN.blit(text, recttt)


        for i in range(len(fivebestscores())):
            quickaddtext(50,(int(pygame.display.Info().current_w/2)),45,200+i*55,str(outputtheint(fivebestscores()[i])) + " by ","Pink")
            quickaddtext(450,(int(pygame.display.Info().current_w/2)),45,200+i*55,outputthename(fivebestscores()[i]),"Red")

        
        OPTIONS_BACK = Button(image=None, pos=(1280, 625), 
                            text_input="BACK", font=get_font(75), base_color="Green", hovering_color="Yellow")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()



def switchdifficulty():
    filee=open(directorr+slash+".."+slash+"difficulty.txt", "r").readlines()
    if "easy" in filee:
        open(directorr+slash+".."+slash+"difficulty.txt", "w").write('normal')
    elif "normal" in filee:
        open(directorr+slash+".."+slash+"difficulty.txt", "w").write('hard')
    else:
        open(directorr+slash+".."+slash+"difficulty.txt", "w").write('easy')
    print(open(directorr+slash+".."+slash+"difficulty.txt", "r").readlines())
def getdifficulty():
    return("".join(open(directorr+slash+".."+slash+"difficulty.txt", "r").readlines()))

def switchfullscreen():
    filee=open(directorr+slash+".."+slash+"fullscreen.txt", "r").readlines()
    if "on" in filee:
        open(directorr+slash+".."+slash+"fullscreen.txt", "w").write('off')
    else:
        open(directorr+slash+".."+slash+"fullscreen.txt", "w").write('on')
def getiffullscreen():
    return("".join(open(directorr+slash+".."+slash+"fullscreen.txt", "r").readlines()))
    


def randomtip():
    return open(directorr+slash+".."+slash+"tips.txt", "r").read().splitlines()[random.randint(0,len(open(directorr+slash+".."+slash+"tips.txt", "r").readlines())-1)]



def options():
    while True:
        global BG
        BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        try: audioconf=open(directorr+slash+".."+slash+"audioconf.txt", "r").read()
        except:audioconf=createanddefine(2)
        audiostate=audioconf
        difficultyconf=open(directorr+slash+".."+slash+"difficulty.txt", "r").read()
        fullscreenconf=open(directorr+slash+".."+slash+"fullscreen.txt", "r").read()

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(45).render("There's only 1 option atm", True, "White") #maybe add a fullscreen option ?
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((int(pygame.display.Info().current_w/2)), int((60/674)*pygame.display.Info().current_h)))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(int((1280/1438)*pygame.display.Info().current_w), int((625/674)*pygame.display.Info().current_h)), 
                            text_input="BACK", font=get_font(75), base_color="Green", hovering_color="Yellow")
        SOUND_BUTTON = Button(image=None, pos=((int(pygame.display.Info().current_w/2)), int((200/674)*pygame.display.Info().current_h)), 
                            text_input=("SOUND: " + audiostate), font=get_font(45), base_color="Red", hovering_color="Pink")
        SOUND_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        SOUND_BUTTON.update(SCREEN)

        DIFFICULTY_BUTTON = Button(image=None, pos=((int(pygame.display.Info().current_w/2)), int((280/674)*pygame.display.Info().current_h)), 
                            text_input=("DIFFICULTY: " + difficultyconf), font=get_font(45), base_color="Red", hovering_color="Pink")
        DIFFICULTY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        DIFFICULTY_BUTTON.update(SCREEN)
        FULLSCREEN_BUTTON = Button(image=None, pos=((int(pygame.display.Info().current_w/2)), int((360/674)*pygame.display.Info().current_h)), 
                            text_input=("FULLSCREEN: " + fullscreenconf), font=get_font(45), base_color="Red", hovering_color="Pink")
        FULLSCREEN_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        FULLSCREEN_BUTTON.update(SCREEN)
        

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if SOUND_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    if createanddefine(3)=="on":
                        createanddefine(2)
                    elif createanddefine(3)=="off":
                        createanddefine(1)
                if DIFFICULTY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    switchdifficulty()
                if FULLSCREEN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    switchfullscreen()
                    if getiffullscreen()=='on':
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
                    if getiffullscreen()=='off':
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.update()

def main_menu():

    if getiffullscreen()=='on':
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
    if getiffullscreen()=='off':
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    therandomtip=randomtip()
    while True:
        global BG
        BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(int(pygame.display.Info().current_w/2), int((120/674)*pygame.display.Info().current_h)))

        scoretext = get_font(20).render("Actual best score -> "+str(bestscore()), True, "Grey")
        scorerect = scoretext.get_rect(center=(int(pygame.display.Info().current_w/2), int((35/674)*pygame.display.Info().current_h)))



        sometext = get_font(10).render(therandomtip, True, "Grey")
        sometextrect = sometext.get_rect(center=(int(pygame.display.Info().current_w/2), int((654/674)*pygame.display.Info().current_h)))

        PLAY_BUTTON = Button(image=None, pos=(int(pygame.display.Info().current_w/2), int((250/674)*pygame.display.Info().current_h)), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(int(pygame.display.Info().current_w/2), int((350/674)*pygame.display.Info().current_h)), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        SB_BUTTON = Button(image=None, pos=(int(pygame.display.Info().current_w/2), int((450/674)*pygame.display.Info().current_h)), 
                            text_input="LEADERBOARD", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(None, pos=(int(pygame.display.Info().current_w/2), int((550/674)*pygame.display.Info().current_h)), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(sometext, sometextrect)
        SCREEN.blit(scoretext, scorerect)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, SB_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    result=game()
                    resultscore=int(result[0]*1000)
                    if checkifnewrecord(resultscore) and getdifficulty()=="normal":
                        usernam=saving()
                        print('saved')
                        open(directorr+slash+'..'+slash+'bestscores.txt', "a").write(str(resultscore)+" "+usernam+"\n")
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if SB_BUTTON.checkForInput(MENU_MOUSE_POS):
                    scoreboard()
        pygame.display.update()


def game():
    # global random
    # global numpy
    # random.seed(2)
    # numpy.random.seed(2)
    difficulty=getdifficulty()
    if createanddefine(3)=="off":
        Sound="f"
    else:
        Sound=True
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
    BRICK_WIDTH, BRICK_HEIGHT = 80, 20
    PLAYER_SIZE = 40
    LAVA_TOP = SCREEN_HEIGHT - 50
    FPS = 60 # THESE ARE NOT REALLY THE FPS BUT THE TPS (TICKS PER SEC)
    GRAVITY = 0.5
    JUMP_HEIGHT = -10
    screen = SCREEN
    clock = pygame.time.Clock()
    try:
        background_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + '705928d396944cff05417cfe7ea07f2f.gif').convert()
        player_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'PlayerRight.png').convert_alpha()
        player_image2 = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'PlayerLeft.png').convert_alpha()
        brick_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'pixil-frame-0.png').convert_alpha()
    except pygame.error as e:
        print('Unable to load an image:', e)
        raise
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image = pygame.transform.scale(player_image, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
    player_image2 = pygame.transform.scale(player_image2, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
    brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))
    


    class DroppingObject:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.size = 64  # Size of the main object
            self.drop_size = 32  # Size of the dropping objects
            self.dropping_items = []
    
        def spawn_drop(self):
            try:self.stopdropping
            except:self.stopdropping=False
            if self.stopdropping==False:
            # Spawn a smaller object
                drop = {'rect': pygame.Rect(self.x + 16, self.y, self.drop_size, self.drop_size), 'speed': 5}
                self.dropping_items.append(drop)
    
        def update(self):
            # Create new drop periodically
            if random.randint(1, 100) == 1:
                self.spawn_drop()
    
            # Update the position of dropping items
            for item in self.dropping_items:
                item['rect'].y += item['speed']
    
        def draw(self, surface):
            """
            # Draw the main object
            pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.size, self.size))
            # Draw the dropping items
            for item in self.dropping_items:
                pygame.draw.rect(surface, (255, 255, 255), item['rect'])
            """

            try:main_object_image
            except:
                main_object_image=pygame.transform.scale((pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'ufo.png').convert_alpha()), (128, 64))
                drop_image=pygame.transform.scale((pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'bomb.png').convert_alpha()), (32, 32))
            try:self.stopdropping
            except:self.stopdropping=False
            if self.stopdropping==True:
                surface.blit(main_object_image, (0, 0))
            else:
                surface.blit(main_object_image, (self.x-35, self.y))
            # Draw the dropping items using their image
            for item in self.dropping_items:
                surface.blit(drop_image, item['rect'])


















    class DroppingDoubleJump:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.size = 64  # Size of the main object
            self.drop_size = 32  # Size of the dropping objects
            self.dropping_items = []
            self.dropped=0
            self.timefordelay=time_since_start
    
        def spawn_drop(self):
            drop = {'rect': pygame.Rect(self.x + 16, self.y, self.drop_size, self.drop_size), 'speed': 5}
            self.dropping_items.append(drop)
    
        def update(self):
            # Create new drop periodically
            if time_since_start-3>self.timefordelay:
                if self.dropped!=1:
                    self.spawn_drop()
                    self.dropped+=1
    
            # Update the position of dropping items
            for item in self.dropping_items:
                item['rect'].y += item['speed']
    
        def draw(self, surface):
            """
            # Draw the main object
            pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.size, self.size))
            # Draw the dropping items
            for item in self.dropping_items:
                pygame.draw.rect(surface, (255, 255, 255), item['rect'])
            """

            try:main_object_image
            except:
                main_object_image=pygame.transform.scale((pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'ufoboosts.png').convert_alpha()), (128, 64))
                drop_image=pygame.transform.scale((pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'heart32x32.png').convert_alpha()), (40, 40))
            try:self.stopdropping
            except:self.stopdropping=False
            if self.stopdropping==True:
                surface.blit(main_object_image, (0, 0))
            else:
                surface.blit(main_object_image, (self.x-35, self.y))
            # Draw the dropping items using their image
            for item in self.dropping_items:
                surface.blit(drop_image, item['rect'])















    global jumptime
    jumptime=0
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()
            self.image=image
            self.rect = self.image.get_rect(midbottom=(x, y))
            self.velocity = 7
            self.vertical_velocity = 0
            self.doublejump=False
            self.on_ground = False
            self.lastimage='left'
        def update(self):
            player_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'PlayerRight.png').convert_alpha()
            player_image2 = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'PlayerLeft.png').convert_alpha()
            player_image = pygame.transform.scale(player_image, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
            player_image2 = pygame.transform.scale(player_image2, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
            if((time_since_start - (int(time_since_start)))<=0.25):
                player_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'rwalking1.png').convert_alpha()
                player_image2 = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'lwalking1.png').convert_alpha()
                player_image = pygame.transform.scale(player_image, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
                player_image2 = pygame.transform.scale(player_image2, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
            elif((time_since_start - (int(time_since_start)))<=0.5):
                player_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'rwalking2.png').convert_alpha()
                player_image2 = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'lwalking2.png').convert_alpha()
                player_image = pygame.transform.scale(player_image, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
                player_image2 = pygame.transform.scale(player_image2, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
            elif((time_since_start - (int(time_since_start)))<=0.75):
                player_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'rwalking3.png').convert_alpha()
                player_image2 = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'lwalking3.png').convert_alpha()
                player_image = pygame.transform.scale(player_image, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
                player_image2 = pygame.transform.scale(player_image2, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
            else:
                player_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'rwalking4.png').convert_alpha()
                player_image2 = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'walkinganim' + slash + 'lwalking4.png').convert_alpha()
                player_image = pygame.transform.scale(player_image, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))
                player_image2 = pygame.transform.scale(player_image2, (int(PLAYER_SIZE*0.42), PLAYER_SIZE))

                    


            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]:
                self.image=player_image2
                self.lastimage='left'
                self.rect.x -= self.velocity
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.image=player_image
                self.lastimage='right'
                self.rect.x += self.velocity
            global jumptime
            if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_z] or keys[pygame.K_SPACE]) and (self.on_ground or (self.doublejump and time_since_start-0.2>jumptime)):
                if time_since_start-0.2>jumptime and self.on_ground==False:
                    self.vertical_velocity = JUMP_HEIGHT
                    self.doublejump=False
                elif self.on_ground==True:
                    
                    if Sound==True:
                        file = './images/jumpsound.mp3'
                        pygame.mixer.music.load(file)
                        pygame.mixer.music.play()
                    self.vertical_velocity = JUMP_HEIGHT
                    self.on_ground = False
                    jumptime=time_since_start
            if (keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_LCTRL]):
                GRAVITY=2
            else:
                GRAVITY=0.5
            if(self.lastimage=='left'):
                self.image=player_image2
            else:
                self.image=player_image
            # Apply gravity and move vertically
            self.vertical_velocity += GRAVITY
            self.rect.y += self.vertical_velocity
            self.on_ground = False  # This will be set to True in check_collision if on a brick
        def check_collision(self, bricks):
            for brick in bricks:
                if pygame.sprite.collide_rect(self, brick):
                    if self.vertical_velocity > 0 and self.rect.bottom-10 <= brick.rect.centery:
                        if self.on_ground==False:
                            self.rect.bottom = brick.rect.top
                            self.vertical_velocity = 0
                            self.on_ground = True
                            # Make the player follow the brick's motion
                            self.rect.x += 2*brick.velocity_x
                            if self.rect.bottom<39:
                                self.rect.x += 2*brick.velocity_x
                            
        def fall_into_lava(self):
            return self.rect.bottom >= LAVA_TOP
    class Brick(pygame.sprite.Sprite):
        def __init__(self, x, y, image, velocity_x):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect(center=(x, y))
            self.velocity_x = velocity_x
        def update(self):
            self.rect.x += self.velocity_x
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()
    all_sprites = pygame.sprite.Group()
    bricks_group = pygame.sprite.Group()
    player_start_x = SCREEN_WIDTH // 2
    player_start_y = SCREEN_HEIGHT // 2
    player = Player(player_start_x, player_start_y - PLAYER_SIZE, player_image)
    all_sprites.add(player)
    initial_brick = Brick(player_start_x, player_start_y, brick_image, 0)
    all_sprites.add(initial_brick)
    bricks_group.add(initial_brick)
    start_ticks = pygame.time.get_ticks()
    running = True

    droppers=[]
    dropperstimes=[]

    droppersboosts=[]
    droppersbooststimes=[]


    DoubleJump=False
    while running:
        time_since_start = (pygame.time.get_ticks() - start_ticks) / 1000  # time in seconds
        if SCREEN_WIDTH!=pygame.display.Info().current_w or SCREEN_HEIGHT!=pygame.display.Info().current_h:
            print('RESIZED WINDOW')
            SCREEN_WIDTH, SCREEN_HEIGHT = (pygame.display.Info().current_w), (pygame.display.Info().current_h)
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        #if time_since_start>=5:
        #    background_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'icelevel.png').convert()
        #    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        try:
            frame
        except:
            frame=1
        try: lastsec
        except: lastsec=time_since_start
        if ((time_since_start-lastsec)>=0.5):       #execs every 0.5 secs
            lastsec=time_since_start
            if frame!=4:
                frame+=1
            else:
                frame=1
            background_image = pygame.image.load(directorr + slash + '..' + slash + 'images' + slash + 'background'+str(frame)+'.png').convert()
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))



        try: secbutbrickslast
        except: secbutbrickslast=time_since_start


        try:
            maxdependingondifficulty
        except:
            if getdifficulty()=='easy':
                maxdependingondifficulty=0
            if getdifficulty()=='normal':
                maxdependingondifficulty=6
            if getdifficulty()=='hard':
                maxdependingondifficulty=10
        
        if ((time_since_start-secbutbrickslast)>=5):
            secbutbrickslast=time_since_start
            if len(droppers)<maxdependingondifficulty:                     
                droppers.append(DroppingObject(random.randint(100,(pygame.display.Info().current_w-100)), 1))
                dropperstimes.append(time_since_start)
                broke=True
                while broke==True:
                    for i in range(len(dropperstimes)):
                        broke=True
                        if time_since_start-6>dropperstimes[i]:         #After 6 secs, the ufo stop dropping and disappears, but the already spawned objects keep falling
                            droppers[i].stopdropping=True
                            dropperstimes.pop(i)
                            break
                        broke=False
            else:
                try: droppers.pop(0)
                except: ()


        try: timeforboosts
        except: timeforboosts=time_since_start
        if ((time_since_start-timeforboosts)>=5):
            timeforboosts=time_since_start
            if len(droppersboosts)<1:                     
                droppersboosts.append(DroppingDoubleJump(random.randint(100,(pygame.display.Info().current_w-100)), 1))
                droppersbooststimes.append(time_since_start)
                broke=True
                while broke==True:
                    for i in range(len(droppersbooststimes)):
                        broke=True
                        if time_since_start-6>droppersbooststimes[i]:         #the ufo stop dropping double jumps and disappears, but the already spawned objects keep falling
                            droppersbooststimes.pop(i)
                            break
                        broke=False
            else:
                droppersboosts.pop(0)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        bricks_group.update()  # Always update bricks
        if time_since_start > 6 and initial_brick in all_sprites:  # Remove the initial brick after 3 seconds
            initial_brick.kill()
        player.check_collision(bricks_group)
        if player.fall_into_lava():
            
            if Sound==True:

                file = './images/deathsound.mp3'
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()



            running = False  # End the game if the player has fallen into the lava
        screen.blit(background_image, (0, 0))
        
        all_sprites.draw(screen)
        bricks_group.draw(screen)
        try: listofys=listofys
        except: listofys=[]
        try: listoftimes=listoftimes
        except: listoftimes=[]
        try: listoftimes2=listoftimes2
        except: listoftimes2=[]
        try: listofys2=listofys2
        except: listofys2=[]
        try:difficultyfactor
        except:difficultyfactor=time_since_start
        if difficulty=="easy":
            difficultyfactor=(math.exp((-1*(time_since_start*0.05))))
        if difficulty=="normal":
            difficultyfactor=math.exp((-1*(time_since_start*0.1)))
        if difficulty=="hard":
            difficultyfactor=(math.exp((-1*(time_since_start*0.2))))
        try:lastbrickx
        except:lastbrickx='left'
        if True: #there was a condition but i removed it and im too lazy to indent
            if random.randint(0, 100) < 8:
                if lastbrickx=='left':
                    new_brick_x = SCREEN_WIDTH - BRICK_WIDTH
                    lastbrickx='right'
                else:
                    new_brick_x=0
                    lastbrickx='left'
                if random.randint(0,100)<=-6:      #-1 AND NOT 3 BECAUSE TESTING THE GAP FEATURE this part makes the bricks spawn where the player is at

                    for i in range(len(listoftimes2)):
                        if time_since_start-4>listoftimes2[i]:
                            listoftimes2.pop(i)
                            listofys2.pop(i)



                    if len(listofys2)>6:
                        ()
                    else:
                        new_brick_y_offset = random.randint(-10, 10)  # Random offset within -10 to 10 pixels
                        new_brick_y = player.rect.y + new_brick_y_offset
                        listofys2.append(new_brick_y)
                        listoftimes2.append(time_since_start)


                    #Ensure the new brick's Y position does not go beyond the screen limits or into the lava
                    new_brick_y = max(PLAYER_SIZE, min(new_brick_y, LAVA_TOP - BRICK_HEIGHT))
                else:

                    # print(player.rect.y) 100 -100
                    if player.rect.y>200 and player.rect.y<LAVA_TOP - BRICK_HEIGHT-102:
                        ranges = [(PLAYER_SIZE, player.rect.y-101), (player.rect.y-100, player.rect.y+100), (player.rect.y+101, LAVA_TOP - BRICK_HEIGHT)]
                        probabilities = [0.35, 0.30, 0.35]  
                        selected_range = numpy.random.choice(len(ranges), p=probabilities)
                        # Generate a random number within the selected range
                        start, end = ranges[selected_range]
                        new_brick_y=numpy.random.randint(start, end + 1)
                    else:
                        new_brick_y = random.randint(PLAYER_SIZE, LAVA_TOP - BRICK_HEIGHT)

                    tross=checkbrickinlist(new_brick_y,listofys,30)
                    secondfact=0
                    while (tross==True and secondfact<1000):
                        if player.rect.y>200 and player.rect.y<LAVA_TOP - BRICK_HEIGHT-102:
                            ranges = [(PLAYER_SIZE, player.rect.y-101), (player.rect.y-100, player.rect.y+100), (player.rect.y+101, LAVA_TOP - BRICK_HEIGHT)]
                            probabilities = [0.35, 0.30, 0.35] 
                            selected_range = numpy.random.choice(len(ranges), p=probabilities)
                            # Generate a random number within the selected range
                            start, end = ranges[selected_range]
                            new_brick_y=numpy.random.randint(start, end + 1)
                        else:
                            new_brick_y = random.randint(PLAYER_SIZE, LAVA_TOP - BRICK_HEIGHT)
                        ranges = [(PLAYER_SIZE, player.rect.y-101), (player.rect.y-100, player.rect.y+100), (player.rect.y+101, LAVA_TOP - BRICK_HEIGHT)]
                        tross=checkbrickinlist(new_brick_y,listofys,30)
                        secondfact+=1
                    if secondfact==1000:
                        new_brick_y=-100
                difficultyfactor2=2-difficultyfactor
                if new_brick_x>300:
                    new_brick_velocity_x = int(-2*difficultyfactor2)
                else:
                    new_brick_velocity_x = int(2*difficultyfactor2)
                new_brick = Brick(new_brick_x, new_brick_y, brick_image, new_brick_velocity_x)
                listofys.append(new_brick_y)
                listoftimes.append(time_since_start)
                something=True
                while something==True:
                    for time in range(len(listoftimes)):
                        if time_since_start-((5*difficultyfactor)+1)>listoftimes[time]:
                            listoftimes.pop(time)
                            listofys.pop(time)
                            something=True
                            break
                        else:
                            something=False


                all_sprites.add(new_brick)
                bricks_group.add(new_brick)
                if new_brick_y==-100:
                    all_sprites.remove(new_brick)
                    bricks_group.remove(new_brick)
        for i in range(len(droppers)):
            droppers[i].update()  # Update object states
            droppers[i].draw(screen)


        for i in range(len(droppersboosts)):
            droppersboosts[i].update()  # Update object states
            droppersboosts[i].draw(screen)

        for i in range(len(droppers)):
            for dropping in droppers[i].dropping_items:
                # print(dropping['rect'].y)
                if ((player.rect.x+30>dropping['rect'].x) and (player.rect.x-30<dropping['rect'].x)) and ((player.rect.y+PLAYER_SIZE>dropping['rect'].y) and (player.rect.y-PLAYER_SIZE<dropping['rect'].y)):
                    print('COLLISION')
                    running=False

        if DoubleJump==True and player.on_ground==True:
            player.doublejump=True
            if time_since_start-10 > TimeOfDoubleJump:
                DoubleJump=False
                player.doublejump=False


        for i in range(len(droppersboosts)):
            for dropping in droppersboosts[i].dropping_items:
                # print(dropping['rect'].y)
                if ((player.rect.x+30>dropping['rect'].x) and (player.rect.x-30<dropping['rect'].x)) and ((player.rect.y+PLAYER_SIZE>dropping['rect'].y) and (player.rect.y-PLAYER_SIZE<dropping['rect'].y)):
                    print('BOOST ACTIVATED')
                    DoubleJump=True
                    player.doublejump=True
                    TimeOfDoubleJump=time_since_start
                    droppersboosts.pop(i)
                    break
        if DoubleJump==True and (10-(time_since_start-TimeOfDoubleJump))>=0:
            text = get_font(20).render('Double Jump:' + str(round(10-(time_since_start-TimeOfDoubleJump),2)), True, "White")
            recttt = text.get_rect(center=(10, 23))
            recttt.left=0
            screen.blit(text, recttt)



                

        def displaytext(text,x,y,size):
            # font = pygame.font.Font(directorr + slash + 'assets' + slash + 'font.ttf', size)
            # text = font.render(text, False, (255, 255, 255))
            # textRect = text.get_rect()
            # textRect.right=1
            # textRect.center = (x,y)
            # screen.blit(text, textRect)

            text = get_font(size).render(text, True, "White")
            recttt = text.get_rect(center=(x, y))
            recttt.left=x-110
            SCREEN.blit(text, recttt)

        displaytext(str(time_since_start),1390,20,32)                                       # Display the time since start
        # displaytext('X:'+str(player.rect.x)+',Y:'+str(player.rect.bottom),1330,50,20)     # Display the coords
        pygame.display.flip()
        clock.tick(FPS)
    running=False
    return [time_since_start]


main_menu()



# Credits to baraltech on youtube for the menu design
# Credits to Luis Zuno on Dribble for the background
# Credits to Emmn Ironsmith on Pinterest for the character