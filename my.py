import pygame, random, os, time
pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space war.")

#Load Ships
RED_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("DATA","Red_Ship_Space.png")), (60,60))
GREEN_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("DATA","Green_Ship_Space.png")), (80,80))
YELLOW_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("DATA","Wellow_Ship_Space.png")), (100,100))
PLAYER_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("DATA","White_Ship_Space.png")), (70,70))

#Load Bullets
RED_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("DATA","red_laser.png")), (20,20))
GREEN_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("DATA","green_laser.png")), (40,40))
YELLOW_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("DATA","yellow_laser.png")), (50,50))
PLAYER_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("DATA","player_laser.png")), (35,35))

#Load heart
HEART = pygame.transform.scale(pygame.image.load(os.path.join("DATA","serce.png")), (25,25))

#Load Sounds



#Load Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("DATA", "back.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))

#Classes
class Laser:    

    def __init__(self, x, y, bullet):
        self.x = x
        self.y = y
        self.bullet = bullet
        self.mask = pygame.mask.from_surface(self.bullet)

    def make_bullet(self, window):
        window.blit(self.bullet, (self.x, self.y))

    def move(self, step):
        self.y += step

    def crash(self, obj):
        return collision(self, obj)

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

class Ship():
    COOLDOWN = 25
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0

    def make_ship(self, screen):
        screen.blit(self.ship_image, (self.x, self.y)) 
        for laser in self.lasers:
            laser.make_bullet(screen)

    def move_lasers(self, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(4)
            if laser.off_screen(SCREEN_HEIGHT):
                self.lasers.remove(laser)
            elif laser.crash(obj):
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser1 = Laser(self.x-5, self.y, self.laser_image)
            laser2 = Laser(self.x + 45, self.y, self.laser_image)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.ship_image = PLAYER_SHIP
        self.laser_image = PLAYER_BULLET
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.score = 0
        self.lives = 5

    def move_lasers(self,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-4)
            if laser.off_screen(SCREEN_HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.crash(obj):
                        objs.remove(obj)
                        self.score += 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)        

class Enemy(Ship):
    ENEMY_TYPE = {"yellow":(YELLOW_SHIP, YELLOW_BULLET),"red":(RED_SHIP, RED_BULLET),"green":(GREEN_SHIP, GREEN_BULLET)}

    def __init__(self, x, y, color):
        super().__init__(x,y)
        self.ship_image, self.laser_image = self.ENEMY_TYPE[color]
        self.mask = pygame.mask.from_surface(self.ship_image)
    
    def move(self, step):
        self.y += step

    def shoot(self):
        if self.cool_down_counter == 0:
            laser1 = Laser(self.x-5, self.y, self.laser_image)
            laser2 = Laser(self.x+45, self.y, self.laser_image)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.cool_down_counter = 1
  

def collision(object_1, object_2):
    label_X = object_2.x - object_1.x
    label_y = object_2.y - object_1.y
    return object_1.mask.overlap(object_2.mask, (label_X, label_y)) != None

def menu():
    start_font = pygame.font.Font("arial.ttf", 40)
    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0,0))
        start_label = start_font.render("Start game - press 1", 1, (255,255,255))
        rules_label = start_font.render("Read rules - press 2", 1, (255,255,255))
        stats_label = start_font.render("Show scores - press 3", 1, (255,255,255))
        credits_label = start_font.render("Show credits - press 4", 1, (255,255,255))
        end_label = start_font.render("Quit game - press 5", 1, (255,255,255))

        SCREEN.blit(start_label, (SCREEN_WIDTH/2 - start_label.get_width()/2, 100))
        SCREEN.blit(rules_label, (SCREEN_WIDTH/2 - rules_label.get_width()/2, 200))
        SCREEN.blit(stats_label, (SCREEN_WIDTH/2 - stats_label.get_width()/2, 300))
        SCREEN.blit(credits_label, (SCREEN_WIDTH/2 - credits_label.get_width()/2, 400))
        SCREEN.blit(end_label, (SCREEN_WIDTH/2 - end_label.get_width()/2, 500))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            main()
        if keys[pygame.K_2]:
            rules()
        if keys[pygame.K_3]:
            scores()
        if keys[pygame.K_4]:
            credits()
        if keys[pygame.K_5]:
            running = False
            
    pygame.quit()

def scores():
    start_font = pygame.font.Font("arial.ttf", 30)
    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0,0))
        score_1 = start_font.render("The best scores are:", 1, (255,255,255))
        score_2 = start_font.render("1:", 1, (255,255,255))
        score_3 = start_font.render("2:", 1, (255,255,255))
        score_4 = start_font.render("3:", 1, (255,255,255))
        score_5 = start_font.render("Quit scores - press mouse:", 1, (255,255,255))

        SCREEN.blit(score_1, (SCREEN_WIDTH/2 - score_1.get_width()/2, 100))
        SCREEN.blit(score_2, (SCREEN_WIDTH/2 - score_2.get_width()/2, 200))
        SCREEN.blit(score_3, (SCREEN_WIDTH/2 - score_3.get_width()/2, 300))
        SCREEN.blit(score_4, (SCREEN_WIDTH/2 - score_4.get_width()/2, 400))
        SCREEN.blit(score_5, (SCREEN_WIDTH/2 - score_5.get_width()/2, 500))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu()
    pygame.quit()

def credits():
    start_font = pygame.font.Font("arial.ttf", 30)
    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0,0))
        credit_1 = start_font.render("Thanks for playing.", 1, (255,255,255))
        credit_2 = start_font.render("Game created by Filip Lasko.", 1, (255,255,255))
        credit_3 = start_font.render("Quit credits - press mouse.", 1, (255,255,255))
        
        SCREEN.blit(credit_1, (SCREEN_WIDTH/2 - credit_1.get_width()/2, 100))
        SCREEN.blit(credit_2, (SCREEN_WIDTH/2 - credit_2.get_width()/2, 200))
        SCREEN.blit(credit_3, (SCREEN_WIDTH/2 - credit_3.get_width()/2, 300))


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu()
    pygame.quit()

def rules():
    start_font = pygame.font.Font("arial.ttf", 20)
    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0,0))
        rule_1 = start_font.render("You have 5 lives.", 1, (255,255,255))
        rule_2 = start_font.render("You have to kill all enemies, remember to dodge their spells.", 1, (255,255,255))
        rule_3 = start_font.render("If enemy leave the space or touch you  will lose one heart.", 1, (255,255,255))
        rule_4 = start_font.render("Quit rules - press mouse.", 1, (255,255,255))

        SCREEN.blit(rule_1, (SCREEN_WIDTH/2 - rule_1.get_width()/2, 100))
        SCREEN.blit(rule_2, (SCREEN_WIDTH/2 - rule_2.get_width()/2, 200))
        SCREEN.blit(rule_3, (SCREEN_WIDTH/2 - rule_3.get_width()/2, 300))
        SCREEN.blit(rule_4, (SCREEN_WIDTH/2 - rule_4.get_width()/2, 400))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu()
    pygame.quit()

def main():
    player_ship = Player(400,600)
    running = True
    level = 0
    lost = False
    main_font = pygame.font.Font("arial.ttf", 30)
    enemies = []
    timer = 0
    number_of_enemies = 10
    clock = pygame.time.Clock()

    def make_screen():
        SCREEN.blit(BACKGROUND,(0,0))

        score_object = main_font.render(f"Score: {player_ship.score}", 1, (255,255,255))
        level_object = main_font.render(f"Level: {level}", 1, (255,255,255))
        SCREEN.blit(level_object, (10, 10))
        SCREEN.blit(score_object, (10, 50))
        for i in range(player_ship.lives):
            SCREEN.blit(HEART, (650+i*30,10))

        for enemy in enemies:
            enemy.make_ship(SCREEN)

        player_ship.make_ship(SCREEN)
        pygame.display.update()

    while running:
        clock.tick(60)
        
        if player_ship.lives <= 0: 
            lost = True
            timer += 1

        if lost:
            lost_label = main_font.render("End of the game! You will be returned to menu.", 1, (255,255,255))
            score_label = main_font.render(f"Your score:{player_ship.score}! ", 1, (255,255,255)) 
            SCREEN.blit(lost_label, (SCREEN_WIDTH/2 - lost_label.get_width()/2, 400))
            SCREEN.blit(score_label, (SCREEN_WIDTH/2 - score_label.get_width()/2, 450))
            if timer > 100:
               menu()
            else:
                continue

        if len(enemies) == 0:
            level +=1
            player_ship.score += 10
            number_of_enemies += 5
            for i in range(number_of_enemies):
                enemy = Enemy(random.randrange(100, SCREEN_WIDTH - 150), random.randrange(-2000-1000*(level/5), -100), random.choice(["yellow", "red", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_ship.x > 10:
            player_ship.x -= 5
        if keys[pygame.K_d] and player_ship.x + 70 < SCREEN_WIDTH:
            player_ship.x += 5
        if keys[pygame.K_w] and player_ship.y > 10:
            player_ship.y -= 5
        if keys[pygame.K_s] and player_ship.y + 60 < SCREEN_HEIGHT:
            player_ship.y += 5
        if keys[pygame.K_SPACE]:
            player_ship.shoot()
        
        for enemy in enemies[:]:
            enemy.move_lasers(player_ship)
            for laser in enemy.lasers:
                if collision(player_ship, laser):
                    player_ship.lives -= 1
            if level <= 5:
                if random.randrange(0, 100) == 1:
                    enemy.shoot()
                enemy.move(1)
            if level > 5 and level <= 10:
                if random.randrange(0, 75) == 1:
                    enemy.shoot()
                enemy.move(2)
            if level > 10 and level <= 15:
                if random.randrange(0, 50) == 1:
                    enemy.shoot()
                enemy.move(3)
            if level > 10 and level <= 15:
                if random.randrange(0, 25) == 1:
                    enemy.shoot()
                enemy.move(4)
            if collision(enemy, player_ship):
                player_ship.lives -= 1
                enemies.remove(enemy)
            if enemy.y > SCREEN_HEIGHT:
                player_ship.lives -= 1
                enemies.remove(enemy)
                   
        make_screen()    
        player_ship.move_lasers(enemies)
    pygame.quit()
                

if __name__ == "__main__":
    menu()