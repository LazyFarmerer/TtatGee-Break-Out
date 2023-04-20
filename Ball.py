import random, pygame
from Game_sys import Game

class Ball:
    li = []
    count = 0
    def __init__(self, win, image, x, y):
        self.__win = win
        self.image = image.convert_alpha()
        self.image = pygame.transform.scale(self.image, Game.alpaca_size)
        self.img_right = self.image
        self.img_left = pygame.transform.flip(self.image, True, False)
        self.img_show = self.image
        self.__img_width, self.__img_height = Game.alpaca_size

        self.radius = self.__img_width // 2
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.center
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # 게임 변수
        self.super_ball = False
        self.is_mouse_click = False
        self.is_active = False
        self.start_speed_x = random.randint(-45, 45)
        self.start_speed_y = -300 # 나중에 스피드 다양하게 만들기
        self.speed_x = self.start_speed_x
        self.speed_y = self.start_speed_y
        self.__up_speed = 1

        self.li.append(self)

    def mouse_click(self, player_rect):
        self.is_mouse_click = True

        self.x = player_rect.centerx
        self.y = player_rect.top - (self.__img_height/2)
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def active(self, is_bool:bool):
        if is_bool is True:
            # 이미 활성화 라면
            if self.is_active is True:
                return

            Ball.count += 1
            self.is_mouse_click = False
            self.is_active = True

            self.speed_x = self.start_speed_x
            self.speed_y = self.start_speed_y
        elif is_bool is False:
            # 이미 비활성화 라면
            if self.is_active is False:
                return

            Ball.count -= 1
            self.super_ball = False
            self.is_mouse_click = False
            self.is_active = False
            self.x, self.y = Game.game_size[0], Game.game_size[1] + self.__img_width

            self.rect.centerx = self.x
            self.rect.centery = self.y

    def __img_animation(self):
        # 좌우 반전
        if 0 < self.speed_x:
            img = self.img_right.copy()
        else:
            img = self.img_left.copy()
        # 슈퍼볼 상태라면
        if self.super_ball is True:
            # 슈퍼볼 이미지 처리
            pixels = pygame.PixelArray(img)
            pixels.replace(pygame.Color(66, 173, 126, 255), pygame.Color(255, 0, 0, 255))
            del pixels

        self.img_show = img

    def speed_up(self):        
        self.speed_x += self.__up_speed if 0 < self.speed_x else -self.__up_speed
        self.speed_y += self.__up_speed if 0 < self.speed_y else -self.__up_speed

    def __move(self, FPS, player_rect):
        # 활성화가 안되어있다면 캐릭터 머리 위에 있음
        if self.is_mouse_click is False:
            self.x = player_rect.centerx
            self.y = player_rect.top - (self.__img_height/2)
            self.rect.centerx = self.x
            self.rect.centery = self.y
            return

        self.x += self.speed_x * (FPS / 1000)
        self.y += self.speed_y * (FPS / 1000)

        # 벽에 튕기기
        if self.x - self.radius <= 0:
            self.speed_x = abs(self.speed_x)
        elif self.x + self.radius >= Game.game_size[0]:
            self.speed_x = -abs(self.speed_x)
        if self.y - self.radius<= 0 :
            self.speed_y = abs(self.speed_y)
        # 바닥과 충돌시
        elif self.y + self.radius >= Game.game_size[1]:
            self.speed_y = -abs(self.speed_y)
            self.active(False) # 비활성화

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def player_hit(self, player_rect):
        self.y = player_rect.top - self.__img_height
        self.speed_y *= -1
        # 부딪힌 위치에 따라 방향 더 꺽임
        self.speed_x += (self.rect.centerx - player_rect.centerx) * 5
    
    def update(self, FPS, player_rect):
        if self.is_active is False:
            return self.is_active

        self.__img_animation()
        self.__move(FPS, player_rect)

        self.__win.blit(self.img_show, (self.x - (self.radius),self.y - (self.radius)))
        return self.is_active

    def show(self, FPS):
        "대기화면에서 보여주기용 함수, 이후 안쓰임"
        if 0 < self.speed_x:
            self.img_show = self.img_right.copy()
        else:
            self.img_show = self.img_left.copy()

        self.x += self.speed_x * (FPS / 1000)
        self.y += self.speed_y * (FPS / 1000)

        if self.x - self.radius <= 0:
            self.speed_x = abs(self.speed_x)
        elif self.x + self.radius >= Game.game_size[0]:
            self.speed_x = -abs(self.speed_x)
        if self.y - self.radius<= 0 :
            self.speed_y = abs(self.speed_y)
        elif self.y + self.radius >= Game.game_size[1]:
            self.speed_y = -abs(self.speed_y)

        self.__win.blit(self.img_show, (self.x - (self.radius),self.y - (self.radius)))