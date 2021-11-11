#导入模块
import pygame as pg
import sys,time,random

#资源的导入
backgroud_img = pg.image.load('forest_2.jpg')
player_img = pg.image.load('player.png')
obstacle_imgs = []
fly_imgs = []
for i in range(8):
    img = pg.image.load('monster_'+str(i+1)+'.png')
    obstacle_imgs.append(img)
for i in range(2):
    img = pg.image.load('bat_'+str(i+1)+'.png')
    fly_imgs.append(img)

#定义玩家类
class Player():
    def __init__(self):
        self.img = pg.transform.scale(player_img, (150, 150)) # 缩放图片，（宽度，高度）
        self.x = 50
        self.y = 100
        self.onfloor = True     #是否在地面上
        self.gravity = 0.2      #重力加速度
        self.vy = 0             #Y方向速度
    def paint(self):
        screen.blit(self.img,(self.x,self.y))
    def move(self):
        self.vy += self.gravity # V = V0 + at
        self.y += self.vy 
        if self.y >= 250:   #模拟落地
            self.vy = 0
            self.y = 250
            self.onfloor = True
        
#定义障碍物类
class Obstacle():
    def __init__(self):
        self.x = 800
        self.y = 250
        self.imgs = obstacle_imgs
        self.passed = False
        self.index = 0
        self.speed = 3
    def choice(self):
        self.index = random.randint(0,7)
        self.speed = random.randint(4,9)
    def paint(self):
        img = pg.transform.scale(self.imgs[self.index], (150, 150))
        screen.blit(img,(self.x,self.y))
    def move(self):
        self.x -= self.speed
        if self.x <= -150:
            self.passed = False
            self.x = 800
            self.choice()
#定义障碍物类
class Fly():
    def __init__(self):
        self.x = 1000
        self.y = 150
        self.imgs = fly_imgs
        self.passed = False
        self.index = 0
        self.speed = 6        
    def choice(self):
        self.index = random.randint(0,1)
        self.speed = random.randint(8,14)
        self.x = random.randint(800,2000)
    def paint(self):
        img = pg.transform.scale(self.imgs[self.index], (100, 100))
        screen.blit(img,(self.x,self.y))
    def move(self):
        self.x -= self.speed
        if self.x <= -100:
            self.passed = False
            self.x = 800
            self.choice()
#创建全局变量
class AllVar():
    player = None
    obstacle = None
    fly = None  
    state = ""
    score = 0
    
    
#处理用户退出、点击操作    
def handleEvent():
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and AllVar.player.onfloor == 1:
                AllVar.player.vy = -11
                AllVar.player.onfloor = 0

# 绘制全部对象的图片
def paintAll():
    #绘制背景
    screen.blit(backgroud_img,(0,0))
    #绘制玩家
    AllVar.player.paint()
    #绘制障碍物
    AllVar.obstacle.paint()
    #绘制飞行物
    AllVar.fly.paint()
    #绘制得分
    screen.blit(game_font.render('score: %d' % AllVar.score, True, [255, 0, 0]), (20, 20))

# 移动全部对象的图片   
def moveAll():
    #绘制玩家
    AllVar.player.move()
    #绘制障碍物
    AllVar.obstacle.move()
    #绘制飞行物
    AllVar.fly.move()
    
#得分检测
def getScore():
    if AllVar.obstacle.x + 150 < AllVar.player.x and AllVar.obstacle.passed == False:
        AllVar.score += 1
        AllVar.obstacle.passed = True
        
#碰撞检测
def hit():
    if AllVar.player.x + 100 >= AllVar.obstacle.x \
    and AllVar.player.x <= AllVar.obstacle.x+150 \
     and AllVar.player.y+100 >= AllVar.obstacle.y:
        print('得分: %d' % AllVar.score)  
        pg.quit()
        sys.exit()
#变量初始化   
AllVar.player = Player()
AllVar.obstacle = Obstacle()
AllVar.fly = Fly()
AllVar.score = 0
#pg模块初始化
pg.init()
game_font = pg.font.Font(None, 50)
#创建、设置游戏窗口
screen = pg.display.set_mode((800,400))
pg.display.set_caption('森林探险')


while True:
    paintAll()
    moveAll()
    handleEvent()
    hit()
    getScore()
    pg.display.update()
    pg.time.delay(10) 
