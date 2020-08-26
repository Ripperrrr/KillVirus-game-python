import pygame
import random
import math

# initial player location
playerX = 400  # x axis
playerY = 500  # y axis
playerStep = 0  # move speed
# create score
score = 0
# create lives
life = 1
# control the mask appear once
check1 = 0
# initial number of virus
ini_num_virus = 6
# save all virus
virus = []
# save mask
mask = []
# save needles
needles = []

# main loop
def main():
    global screen
    # initial of pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # size
    # create BGM
    pygame.mixer.music.load('./materials/BGM.mp3')
    pygame.mixer.music.play(-1)

    while True:
        running()
        show_finish()
        print("finish")

# show finish screen
def show_finish():
    global life, score, ini_num_virus, playerX, playerY, check1
    # end interface materials
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    res_font = pygame.font.Font('freesansbold.ttf', 24)
    text = "Final Score"
    txt_score = f"{score}"
    txt_restart = "Press R to restart"
    render = over_font.render(text, True, (0, 0, 255))
    scr_render = over_font.render(txt_score, True, (0, 0, 255))
    res_render = res_font.render(txt_restart, True, (0, 0, 255))
    end_surface = pygame.image.load('./materials/bg2.jpg')

    screen.blit(end_surface, (0, 0))
    screen.blit(render, (220, 250))
    screen.blit(scr_render, (375, 340))
    screen.blit(res_render, (300, 550))
    pygame.display.update()
    while True:

        restart = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True
                    playerX = 400
                    playerY = 500
                    check1 = 0
                    life = 1
                    score = 0
                    mask.clear()
                    needles.clear()
                    ini_num_virus = 6
        if restart:
            return

# main loop of game
def running():
    global playerStep, life, score, font, heart
    clock = pygame.time.Clock()  # controlling screen refresh
    pygame.display.set_caption('ERADICATION OF COVID-19')  # name
    icon = pygame.image.load('./materials/icon_doctor.png')  # icon
    pygame.display.set_icon(icon)
    bgImg = pygame.image.load('./materials/bg3.jpg')  # bgpicture
    heart = pygame.image.load('./materials/heart.png')
    # shoot sound
    shoot_sound = pygame.mixer.Sound('./materials/needlesshoot.wav')

    # create player
    playerImg = pygame.image.load('./materials/doctor.png')  # player picture

    font = pygame.font.Font('freesansbold.ttf', 32)

    # add virus
    for i in range(ini_num_virus):
        virus.append(Virus())

    while True:
        clock.tick(60)
        screen.blit(bgImg, (0, 0))
        show_info()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # control movement of player
            if event.type == pygame.KEYDOWN:  # type keyboard to move
                if event.key == pygame.K_RIGHT:
                    playerStep = 5
                elif event.key == pygame.K_LEFT:
                    playerStep = -5
                elif event.key == pygame.K_SPACE:
                    # create a bullet
                    shoot_sound.play()
                    needles.append(Needles())

            if event.type != pygame.KEYDOWN:
                playerStep = 0
        screen.blit(playerImg, (playerX, playerY))
        player_move()
        show_virus()
        show_needles()
        if life > 0:
            show_mask()
        else:
            virus.clear()
            return
        pygame.display.update()

# distance method
def distance(bx,by,ex,ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a * a + b * b)

# virus class
class Virus():
    def __init__(self):
        self.img = pygame.image.load('./materials/virus.png')
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
        self.step = random.randint(2, 6) #enemy

    def reset(self):
        self.x = random.randint(200,600)
        self.y = random.randint(50,200)

# show virus on screen
def show_virus():
    global life
    for v in virus:
        screen.blit(v.img, (v.x, v.y))
        v.x += v.step
        if(v.x > 736 or v.x < 0):
            v.step *= -1
            v.y += 40
            if v.y > 450:
                life -= 1
                v.reset()

# needles
class Needles():
    def __init__(self):
        self.img = pygame.image.load('./materials/needles2.png')
        self.x = playerX + 16  # (64-32)/2
        self.y = playerY + 10
        self.step = 10
        self.hit_sound = pygame.mixer.Sound('./materials/hit.wav')
        self.reward_soud = pygame.mixer.Sound('./materials/reward.wav')

    # hit virus function
    def hit(self):
        global score
        for v in virus:
            if(distance(self.x, self.y, v.x, v.y) < 30):
                if self != None:
                    needles.remove(self)
                self.hit_sound.play()
                v.reset()
                score += 1

    # touch mask function
    def touch(self):
        global life
        for m in mask:
            if(distance(self.x, self.y, m.x, m.y) < 30):
                if self != None:
                    needles.remove(self)
                self.reward_soud.play()
                mask.remove(m)
                life +=1

# show and move needles
def show_needles():
    for n in needles:
        screen.blit(n.img, (n.x, n.y))
        n.hit()
        n.touch()
        n.y -= n.step
        if n.y < 0:
            needles.remove(n)

# mask class
class Mask():
    def __init__(self):
        self.img = pygame.image.load('./materials/mask.png')
        self.x = random.randint(0, 600)
        self.y = 0
        self.step = 3

# when player touch the mask
    def reset(self):
        self.y = 0
        self.x = random.randint(0, 600)


#show mask
def show_mask():
    global check1
    if (score % 5 == 0 and score > 0 and score != check1):
        mask.append(Mask())
        check1 = score
    if (len(mask) != 0):
        for m in mask:
            screen.blit(m.img, (m.x, m.y))
            m.y += m.step
            if (m.y > 450):
                mask.remove(m)

#show score and life
def show_info():
    text1 = f"Score: {score}"
    text2 = f"{life}"
    score_render = font.render(text1, True, (0, 255, 0))
    life_render = font.render(text2, True, (255, 0, 0))
    screen.blit(score_render, (10, 10))
    screen.blit(heart,(700,10))
    screen.blit(life_render, (750,10))

#check if the game is over
def check_over():
    global life, score, check1

    if life > 0:
        if (score % 5 == 0 and score > 0 and score != check1):
            mask.append(Mask())
            check1 = score
        if(len(mask) != 0):
            show_mask()
    else:
        virus.clear()
        return

# movement of player
def player_move():
    global playerX
    playerX += playerStep
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0

if __name__ == '__main__':
    main()