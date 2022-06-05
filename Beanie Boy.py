import pygame
import time
import sys
import random
import os

pygame.init()
width = 332
height  = 720
display = pygame.display.set_mode((width,height))


#Bilderpfad
bg01 = pygame.image.load(os.path.join("img","background", "lvl1.png"))
bg02 = pygame.image.load(os.path.join("img","background", "lvl2.png"))
bg03 = pygame.image.load(os.path.join("img","background", "lvl3.png"))
bg04= pygame.image.load(os.path.join("img","background", "lvl4.png"))
bg05= pygame.image.load(os.path.join("img","background", "lvl5.png"))
gameover= pygame.transform.scale(pygame.image.load(os.path.join("img","menu", "game_over.png")).convert_alpha(),(250,100))
pause= pygame.transform.scale(pygame.image.load(os.path.join("img","menu", "pause.png")).convert_alpha(),(250,120))
cover02 = pygame.image.load(os.path.join("img","menu", "player2.png")).convert_alpha()
cover01 = pygame.image.load(os.path.join("img","menu", "player1.png")).convert_alpha()
trunk = pygame.image.load(os.path.join("img","trunk", "trunk.png"))
r_enemy= pygame.image.load(os.path.join("img","bird","bird.png"))
x2jump= pygame.image.load(os.path.join("img","bird","x2jump.png"))
l_enemy=pygame.transform.flip(r_enemy, True, False)
stand = pygame.image.load(os.path.join("img","player", "stand.png"))
jump = pygame.image.load(os.path.join("img","player", "jump.png"))
left = [pygame.image.load(os.path.join("img","player", "L1.png")),pygame.image.load(os.path.join("img","player", "L2.png")),pygame.image.load(os.path.join("img","player", "L3.png")),pygame.image.load(os.path.join("img", "player","L4.png"))]
right = [pygame.image.load(os.path.join("img","player", "R1.png")),pygame.image.load(os.path.join("img","player", "R2.png")),pygame.image.load(os.path.join("img","player", "R3.png")),pygame.image.load(os.path.join("img", "player","R4.png"))]
button_exit = pygame.transform.scale(pygame.image.load(os.path.join("img","menu", "exit.png")).convert_alpha(),(245,80))
button_start = pygame.transform.scale(pygame.image.load(os.path.join("img","menu", "play.png")).convert_alpha(),(245,80))
font = pygame.font.SysFont(None,45)

#Bilder pfad 
jump_sound = pygame.mixer.Sound(os.path.join("Sound", "jump.ogg"))
xjump_sound = pygame.mixer.Sound(os.path.join("Sound", "double_jump.ogg"))
walk_sound = pygame.mixer.Sound(os.path.join("Sound", "walking.ogg"))
game_over = pygame.mixer.Sound(os.path.join("Sound", "gameover.ogg"))
bg_music =pygame.mixer.music.load(os.path.join("Sound", "music.mp3"))




#Music pfad
pygame.mixer.Sound.set_volume(jump_sound, 0.9)
pygame.mixer.Sound.set_volume(xjump_sound, 0.9)
pygame.mixer.Sound.set_volume(walk_sound, 0.3)




#Tasten Einstellungen (Beenden und Starten)
buttons_width = 40
buttons_height = 300
button_start_rect = button_start.get_rect()
button_start_rect.topleft = (buttons_width,buttons_height)
button_exit_rect = button_exit.get_rect()
button_exit_rect.topleft = (buttons_width,buttons_height+150)




pygame.display.set_caption("Beanie Boy")
clock = pygame.time.Clock()	
gravity = 0.2
running = True
bg_height = 0
volume = 1





#klasse des Spieles
class Player(pygame.sprite.Sprite):
        image_stand = stand
        image_jump = jump
        image_left = left
        image_right = right
        frame = 0
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = self.image_stand.convert_alpha()
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.jump = 0
                self.highjump = False
                self.gravity = 0
                self.is_on_floor = False
                self.standing = True
                self.left = False
                self.right = False
                self.up = False
                self.face = "down"
                self.anim_speed = 0.6

                
        #Überprüfen Sie, ob der Spieler mit dem Baumstamm kollidiert
        def check_collision(self):
                self.is_on_floor = False
                for trunk in trunk_group:
                        if self.rect.colliderect(trunk.rect):
                                if self.rect.bottom <= trunk.rect.bottom:
                                        if self.jump <= 0:
                                                self.rect.bottom = trunk.rect.top +1
                                                self.is_on_floor = True
                                                self.gravity = 0
        def update(self):
            #Animationseinstellungen links
                if self.left:
                    self.face = "left"
                    self.right = False
                    self.standing = False
                    self.up = False
                    self.image = self.image_left[int(self.frame)].convert_alpha()
                    self.frame += self.anim_speed
                    if int(self.frame) >= len(self.image_left):
                        self.frame = 0
            #Animationseinstellungen rechts      
                elif self.right:
                    self.face = "right"
                    self.left = False
                    self.standing = False
                    self.up = False
                    self.image = self.image_right[int(self.frame)].convert_alpha()
                    self.frame += self.anim_speed
                    if int(self.frame) >= len(self.image_right):
                        self.frame = 0
            #Animationseinstellungen springen
                elif self.up:
                    self.face = "up"
                    self.left = False
                    self.right = False
                    self.standing = False
                    self.image = self.image_jump.convert_alpha()
            #Animationseinstellungen Stand
                elif self.standing:
                    self.face = "down"
                    self.left = False
                    self.right = False
                    self.up = False
            #Animationseinstellungen: 
                    if self.face == "down":
                        self.image = self.image_stand.convert_alpha()
                    elif self.face == "left":
                        self.image = self.image_left[0].convert_alpha()
                    elif self.face == "up":
                        self.image = self.image_jump.convert_alpha()
                    elif self.face == "right":
                        self.image = self.image_right[0].convert_alpha()
                    self.frame = 0.1
                    
                
            #Sprung Einstellungen
                if not self.jump:
                        if not self.is_on_floor:
                                self.rect.y += self.gravity
                                self.gravity += 0.5
                else:
                        self.rect.y -= self.jump
                        self.jump -= 0.5
                        
        def draw(self):
            display.blit(self.image,self.rect)

                

#klasse des Feindes
class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = r_enemy
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.change_x = 2
                
        def draw(self):
                display.blit(self.image,self.rect)

            



                
#klasse des Baumstammes
class Trunk(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = trunk
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.fall = 0
                
        def draw(self):
                display.blit(self.image,self.rect)




trunk_collision_group = pygame.sprite.Group()
trunk_group = [Trunk(150,550)]
trunk_collision_group.add(trunk_group[0])

enemy_collision_group = pygame.sprite.Group()
enemy_group = []
enemy_y = 300

score = 0
high_scores = []


def text(msg,color,x,y):
    text = font.render(msg,True,color)
    display.blit(text,[x,y])

#Um einen Ordner Highscore zu öffnen
with open("highscore.txt","r") as file:
    saved_scores = file.readlines()
    for line in saved_scores:

        line = line.rstrip('\n')
        high_scores.append(line)
#Um das neue Punktzahl in einem Ordner Highscore zu speichern      
def save_score(mode,score):
    saved = open("highscore.txt", "r",1)
    list_of_lines = saved.readlines()
    
    if score > int(list_of_lines[mode]):
        list_of_lines[mode] = str(score) + "\n"
    saved = open("highscore.txt", "w")
    saved.writelines(list_of_lines)
    high_scores.clear()
    for line in list_of_lines:
        line = line.rstrip("\n")
        high_scores.append(line)
    saved.close()


#Pause Einstellungen
def Pause():
        paused = True
        while paused:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                        paused = False
                                elif event.key == pygame.K_q:
                                        pygame.quit()
                                        sys.exit()
                display.blit(pause,(40,100))
                display.blit(cover02,(2,300))
                display.blit(cover01,(240,220))
                text("Press 'p' to continue",(178,34,0),16,450)
                text("or 'q' to quit ",(178,34,0),70,485)
                text("Score:",(0,0,0),95,345)
                text(str(score),(0,0,0),190,345)
                pygame.display.update()
                
                
                



#Hauptschnittstelleneinstellungen
#Start- und Endeinstellungen mit der Maus
def main_menu():
    pygame.mouse.set_visible(True)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
                sys.exit(0)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            clicked = False
            
            display.fill((111, 143, 175))
            display.blit(button_start,(buttons_width,buttons_height))
            display.blit(button_exit,(buttons_width,buttons_height+150))
            display.blit(cover02,(25,127))
            display.blit(cover01,(228,124))
            text("Beanie Boy",(199, 0, 57),80,175)
            text("High Score: ",(0,0,0),40,600)
            text(str(high_scores[0]),(0,0,0),220,600)
            buttons = [button_start_rect,button_exit_rect]
            for button in buttons:
                if button[0] < mouse[0] < button[0] + button[2]:
                    if button[1] < mouse[1] < button[1] +button[3]:

                        if click[0] == 1:
                            clicked = True
                            if button[1] == button_start_rect[1]: main()
                            if button[1] == button_exit_rect[1]: pygame.quit(); sys.exit(0);
                        
            clock.tick(60)
            pygame.display.update()

#letzten Schnittstelleneinstellungen
def end_screen():
    global trunk_group


    enemy_collision_group.empty()
    enemy_group.clear()
    trunk_group.clear()
    trunk_group = [Trunk(150,550)]

    while True:
        display.fill((111, 143, 175))
        display.blit(button_start,(buttons_width,buttons_height))
        display.blit(button_exit,(buttons_width,buttons_height+150))
        display.blit(gameover,(40,100))
        text("High Score:",(0,0,0),50,220)
        text(str(high_scores[0]),(0,0,0),220,220)
        text("Score:",(0,0,0),95,250)
        text(str(score),(0,0,0),190,250)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
                sys.exit(0)
            
    
        #Start- und Endeinstellungen mit der Maus
        buttons = [button_start_rect,button_exit_rect]
        for button in buttons:
            if button[0] < mouse[0] < button[0] + button[2]:
                if button[1] < mouse[1] < button[1] +button[3]:

                    if click[0] == 1:
                        if button[1] == button_start_rect[1]: main()
                        if button[1] == button_exit_rect[1]: pygame.quit(); sys.exit(0);
        
        clock.tick(60)
        pygame.display.update()




def main():
        global score, volume 
        score = 0
        keyjump = 0
        enemy_y = 300
        player = Player(150,450)
        platform = 550
        pygame.mixer.music.play(-1)
        clock.tick(60)
        



                


        #Vögel hinzufügen
        for i in range(0,165):
            enemy_group.append(Enemy(random.randint(37,295),enemy_y))
            enemy_y -= 300
        for enemy in enemy_group:
            enemy_collision_group.add(enemy) 


        #Baumstamm hinzufügen 
        for i in range(0,500):
            platform -= 100
            trunk_group.append(Trunk(random.randint(37,295),platform))
        for trunk in trunk_group:
                trunk_collision_group.add(trunk)

        #Das Bild ändert sich bei der angegebener Punktzahl
        global running
        while running:
                if score > 2000:
                        bga= bg05
                elif score > 1500:
                        bga= bg04
                elif score > 800:
                        bga=bg03
                elif score > 400:
                        bga=bg02
                elif score < 400:
                        bga=bg01
                display.blit(bga,(0,0))


                #Die Bewegung von Vögeln und Baumstamm, wenn der Bildschirm nach oben geht 
                if player.rect.centery <= height/2:
                        for trunk in trunk_group:
                                trunk.rect.top += 3       
                        for enemy in enemy_group:
                                enemy.rect.top += 3

                        
                pygame.mixer.music.set_volume(volume)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()
                                sys.exit()
                                        
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:    
                                        running = False
                                        pygame.quit()
                                        sys.exit()
                                elif event.key == pygame.K_x:
                                        running = False
                                        pygame.quit()
                                        sys.exit()
                                elif event.key == pygame.K_p:
                                        Pause()
                                #Schalten Sie die Musik im Spiel stumm
                                elif event.key == pygame.K_m:
                                        if volume >0:
                                                volume = 0
                                        else:
                                                volume = 1

                ##Tasten Bewegungssteuerung                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                        player.left = True
                        player.right= False
                        player.up = False
                        player.standing = False
                        player.rect.centerx -= 5
                        i += 1
                        if i % 10 == 1:
                            pygame.mixer.Sound.play(walk_sound)


                elif keys[pygame.K_RIGHT]:
                        player.left = False
                        player.up = False
                        player.right= True
                        player.standing = False
                        player.rect.centerx += 5
                        i += 1
                        if i % 10 == 1:
                            pygame.mixer.Sound.play(walk_sound)

                else:
                        i = 0
                        player.standing = True
                        player.left = False
                        player.right = False
                        player.up = False
                        
                if keys[pygame.K_SPACE]:
                        player.up = True
                        
                        #Überprüfen Sie, ob der Spieler springen darf
                        if player.is_on_floor: 
                            player.jump = 10
                            player.is_on_floor = False
                            pygame.mixer.Sound.play(jump_sound)

                
       
                if keys[pygame.K_v]:
                        if keyjump > 0:
                                player.up = True
                                player.jump = 12
                                keyjump -= 1
                                pygame.mixer.Sound.play(xjump_sound)
                

                #Einen starken Sprung geben, wenn der Spieler die angegebene Punktzahl erreicht
                if score == 2000 and player.highjump == False:
                        keyjump += 1
                        player.highjump = True
                elif score == 1500 and player.highjump == True:
                        keyjump += 1
                        player.highjump = False
                elif score == 800 and player.highjump == False:
                        keyjump += 1
                        player.highjump = True
                elif score == 400 and player.highjump == True:
                        keyjump += 1
                        player.highjump = False
                
                elif score == 40 and player.highjump == False:
                        keyjump += 1
                        player.highjump = True
                        


                            
     
               
                player.check_collision()
                player.update()
                player.draw()
                


                #Kollision mit Fenster(Spieler)
                if player.rect.left > width:
                    player.rect.right = 0
                elif player.rect.right < 0:
                    player.rect.left = width 
                if player.rect.bottom >= height:
                    save_score(0,score)
                    pygame.mixer.Sound.play(game_over)
                    end_screen()


                #Kollision mit Fenster(Feind)    
                for enemy in enemy_collision_group:
                        enemy.draw()
                        if len(enemy_collision_group) <= 0:
                            enemy_collision_group.empty()
                        enemy.rect.centerx += enemy.change_x
                        if enemy.rect.left <= 0:
                                enemy.change_x = 2
                                enemy.image=r_enemy
                                #Vögel erhöhen ihre Geschwindigkeit bei einer bestimmter Punktzahl
                                if score > 800:
                                        if enemy.rect.right >= width:
                                                enemy.change_x = 3
                                                enemy.image=l_enemy
                                if score > 1500:
                                        if enemy.rect.right >= width:
                                                enemy.change_x = 7
                                                enemy.image=l_enemy
                                        
                        if enemy.rect.right >= width:
                                enemy.change_x = -2
                                enemy.image=l_enemy
                                #Vögel erhöhen ihre Geschwindigkeit bei einer bestimmter Punktzahl
                                if score > 400:
                                        if enemy.rect.right >= width:
                                                enemy.change_x = -3
                                                enemy.image=l_enemy
                                if score > 2000:
                                        if enemy.rect.right >= width:
                                                enemy.change_x = -7
                                                enemy.image=l_enemy

                        
                collided = pygame.sprite.spritecollide(player,enemy_collision_group,False)
                if collided:
                        pygame.mixer.Sound.play(game_over)
                        save_score(0,score)
                        end_screen()

                
                #Baumstamm ziehen und entfernen
                for trunk in trunk_group:
                        trunk.draw()
                        if trunk.rect.top >= height:
                                trunk_group.remove(trunk)
                                score += 10
                text("Score: ",(25, 7, 11),10,height - 719)
                text(str(score),(25, 7, 11),110,height - 719)
                display.blit(x2jump,(310,5))
                text(str(keyjump),(25, 7, 11),285,height - 718)

                
                
                
                
                                


                clock.tick(60)
                pygame.display.update()
main_menu()


